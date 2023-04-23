import tkinter as tk
from tkinter import font
from autogooglecalendar.create_event import create_event

def send_request():
    summary = summary_entry.get()
    description = description_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()

    if start_time:
        if end_time == "":
            result = create_event(summary, description, start_time)
        else:
            result = create_event(summary, description, start_time, end_time)

        # # Update the result label
        # result_label.config(text=str(result))
        # Update the result text widget
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, str(result))

    else:
        # result_label.config(text="Start time is required to send a request")

        # Update the result text widget
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "Start time is required to send a request.")


dark_bg = '#2b2b2b'
dark_fg = '#dcdcdc'


def center_window(root, root_w, root_h):
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate x and y coordinates for centering
    x = (screen_width / 2) - (root_w / 2)
    y = (screen_height / 2) - (root_h / 2)
    
    # Set geometry
    root.geometry(f'{root_w}x{root_h}+{int(x)}+{int(y)}')


root = tk.Tk()
root.title("Create appointment")
center_window(root, 500, 900)
root.minsize(width=500, height=900) 
root.config(bg=dark_bg)

# Set the default font size to 20 pixels
default_font = font.nametofont("TkDefaultFont")
default_font.config(size=15)

main_frame = tk.Frame(root)
main_frame.pack(padx=40, pady=40)
main_frame.config(bg=dark_bg)

summary_label = tk.Label(main_frame, text="Summary:", bg=dark_bg, fg=dark_fg, width=50, font=default_font)
summary_entry = tk.Entry(main_frame, bg=dark_bg, fg=dark_fg, width=50, font=default_font)
description_label = tk.Label(main_frame, text="Description:", bg=dark_bg, fg=dark_fg, width=50, font=default_font)
description_entry = tk.Entry(main_frame, bg=dark_bg, fg=dark_fg, width=50, font=default_font)
start_time_label = tk.Label(main_frame, text="Start Time:", bg=dark_bg, fg=dark_fg, width=50, font=default_font)
start_time_entry = tk.Entry(main_frame, bg=dark_bg, fg=dark_fg, width=50, font=default_font)
end_time_label = tk.Label(main_frame, text="End Time:", bg=dark_bg, fg=dark_fg, width=50, font=default_font)
end_time_entry = tk.Entry(main_frame, bg=dark_bg, fg=dark_fg, width=50, font=default_font)
send_button = tk.Button(main_frame, text="Send Request", command=send_request, bg=dark_bg, fg=dark_fg, width=50, font=default_font)

summary_label.pack(padx=20, pady=5)
summary_entry.pack(padx=20, pady=5)
description_label.pack(padx=20, pady=5)
description_entry.pack(padx=20, pady=5)
start_time_label.pack(padx=20, pady=5)
start_time_entry.pack(padx=20, pady=5)
end_time_label.pack(padx=20, pady=5)
end_time_entry.pack(padx=20, pady=5)
send_button.pack(padx=20, pady=25)

# Add a label to display the result
result_label = tk.Label(main_frame, text="", bg=dark_bg, fg=dark_fg, width=50, font=default_font)
result_label.pack(padx=20, pady=50)

# Add a text widget and a scrollbar to display the result
result_text = tk.Text(main_frame, height=8, bg=dark_bg, fg=dark_fg, width=50, font=default_font)
result_scrollbar = tk.Scrollbar(main_frame, command=result_text.yview)
result_text.config(yscrollcommand=result_scrollbar.set)

result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()