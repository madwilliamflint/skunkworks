import tkinter as tk
from tkinter import messagebox, Toplevel, Text
import requests
import time
import json

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def check_resource(url, port):
    try:
        response = requests.get(url, timeout=5)
        status = 'green' if response.status_code == 200 else 'red'
        details = {
            "url": url,
            "port": port,
            "response_time": f"{response.elapsed.total_seconds()}s",
            "status_code": response.status_code,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        status = 'red'
        details = {
            "url": url,
            "port": port,
            "error": str(e),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    return status, details

def update_status():
    global last_update
    for resource in config['resources']:
        status_color, details = check_resource(resource['url'], resource['port'])
        status_labels[resource['url']].itemconfig(circle_ids[resource['url']], fill=status_color)
        resource_details[resource['url']] = details  # Store the detailed data
    last_update = time.time()
    last_refresh_time.set(time.strftime("%H:%M:%S", time.localtime(last_update)))
    root.after(config['refresh_delay'], update_status)

def update_time():
    elapsed_time = int(time.time() - last_update)
    status_time.set(f"Last refresh: {elapsed_time} seconds ago")
    root.after(1000, update_time)

def show_details(url):
    global detail_window, text
    details = json.dumps(resource_details[url], indent=4)
    if 'detail_window' in globals() and detail_window.winfo_exists():
        detail_window.lift()  # Bring the window to the front
        text.delete('1.0', tk.END)  # Clear the existing text
        text.insert(tk.END, details)  # Insert new details
    else:
        detail_window = Toplevel(root)
        detail_window.title("Resource Details")
        text = Text(detail_window)
        text.insert(tk.END, details)
        text.pack()

config = load_config()
root = tk.Tk()
root.title("Resource Status")

status_labels = {}
circle_ids = {}
resource_details = {}  # Dictionary to store detailed data for each resource
last_refresh_time = tk.StringVar()
status_time = tk.StringVar()
last_update = time.time()

bg_color = root.cget("bg")

# Add table headers and shift them right
header_frame = tk.Frame(root, bg=bg_color)
header_frame.pack(fill='x', pady=5)
tk.Label(header_frame, text="", width=3, anchor='w', bg=bg_color).pack(side='left', padx=10)  # Placeholder for graphic
tk.Label(header_frame, text="Name", width=20, anchor='w', bg=bg_color).pack(side='left')
tk.Label(header_frame, text="URL", width=40, anchor='w', bg=bg_color).pack(side='left')
tk.Label(header_frame, text="Port", width=10, anchor='w', bg=bg_color).pack(side='left')

# Add resource entries
for resource in config['resources']:
    frame = tk.Frame(root, bg=bg_color)
    frame.pack(fill='x', pady=5)
    status_label = tk.Canvas(frame, width=20, height=20, bg=bg_color, highlightthickness=0)
    circle_id = status_label.create_oval(2, 2, 18, 18, fill='grey')
    status_label.pack(side='left', padx=10)  # Margin around the indicator
    name_label = tk.Label(frame, text=resource['name'], width=20, anchor='w', bg=bg_color, cursor="hand2")
    name_label.pack(side='left')
    name_label.bind("<Button-1>", lambda e, url=resource['url']: show_details(url))
    url_label = tk.Label(frame, text=resource['url'], width=40, anchor='w', bg=bg_color)
    url_label.pack(side='left')
    port_label = tk.Label(frame, text=f"Port: {resource['port']}", width=10, anchor='w', bg=bg_color)
    port_label.pack(side='left')
    status_labels[resource['url']] = status_label
    circle_ids[resource['url']] = circle_id

button = tk.Button(root, text='Check Status', command=update_status)
button.pack(pady=10)

refresh_label = tk.Label(root, textvariable=status_time, bg=bg_color)
refresh_label.pack(pady=10)

update_status()  # Initial call to start the periodic polling
update_time()  # Initial call to start the time update

root.mainloop()
