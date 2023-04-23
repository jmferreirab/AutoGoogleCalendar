# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.
from autogooglecalendar.quickstart import create_service
import datetime
import locale

def create_event(summary, description, start_time: datetime.datetime|str, end_time: datetime.datetime|str = None):

    if not start_time:
        return "Received NoneType time string"

    try:
        if isinstance(start_time, str):
            start_time = convert_spanish_datetime_string(start_time)
        if isinstance(end_time, str):
            end_time = convert_spanish_datetime_string(end_time)

        if not end_time:
            end_time = start_time + datetime.timedelta(hours=1)

        start_time = start_time.isoformat()
        end_time = end_time.isoformat()

        event = {
        'summary': summary,
        'description': description,
        'start': {
            # 'dateTime': '2015-05-28T09:00:00-07:00',
            'dateTime': start_time,
            'timeZone': 'America/Bogota',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Bogota',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 1 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
        }

        service = create_service()
        event = service.events().insert(calendarId='primary', body=event).execute()
        msg = f"Event created: \n{event.get('htmlLink')}. \n\nStart: {event.get('start')['dateTime']}. \n\nDescription: {event.get('description')}"
        
        
    except Exception as ex:
        ex_part = str(ex)
        msg = "Failed to create event. Ex: " + ex_part
    
    print(msg)
    return msg

def test_auth_scope():
    service = create_service()
    calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
    print(calendar_list_entry)


def convert_time_string_regex():

    import re
    ex = '26 de Abril 2023 a las 6:00 p.m'
    ex = ex.lower()
    months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    english_months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    month_dict = dict(zip(months, english_months))

    pattern=f"{'|'.join(months)}"
    match_month = re.findall(pattern, string=ex)
    print(match_month)



def convert_spanish_datetime_string(datetime_string:str = '26 de Abril 2023 a las 6:00 p.m.'):
    """ 
        Try with MM/DD HH:MM or DD ...
        Otherwise try with MMMM YYYY ... H:MM tt
        Otherwise return a string with an error
    """
    try:
        # Try to parse the input string as "MM/DD HH:MM"
        dt = datetime.datetime.strptime(datetime_string, '%m/%d %H:%M')
        # Add the current year and set seconds to 0
        dt = dt.replace(year=datetime.datetime.now().year, second=0)
    except ValueError:
        try:
            # Set the locale to Spanish
            locale.setlocale(locale.LC_ALL, 'es_mx') # '22 de abril 2023 a las 06:14 p. m.'
            datetime_string = datetime_string.replace("p.m.", "p. m.")
            dt = datetime.datetime.strptime(datetime_string, '%d de %B %Y a las %I:%M %p')
        except ValueError:
            # Return an error message if neither format is recognized
            dt = None
    return dt



def create_event_in_ten_minutes():
    st = datetime.datetime.now() + datetime.timedelta(minutes=11)
    print(st)

    create_event(summary="Test",description="Test", start_time=st)

if __name__ == "__main__":
    summary = 'test'
    description = 'test'
    start_time = '26 de Abril 2023 a las 6:00 p.m.'
    create_event(summary, description, start_time)

