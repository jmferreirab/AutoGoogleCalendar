from __future__ import print_function

import datetime
import os.path
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar']
TOKEN_PATH = './resources/token.json'
CREDENTIALS_PATH = './resources/credentials.json'


def create_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    try:
        # service = build('calendar', 'v3', credentials=creds)
        service = build("calendar", "v3", credentials=creds,  static_discovery=False)
        return service
    except Exception:
        logging.exception("There was an error connecting to the calendar service", exc_info=True)
        quit()

def get_latest_events():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    

    try:
        service = create_service()

        # Call the Calendar API
        now = datetime.datetime.utcnow()  # 'Z' indicates UTC time
        ten_days_ago = now - datetime.timedelta(days=10)
        ten_days_ago = ten_days_ago.isoformat() + 'Z'
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary',
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    get_latest_events()