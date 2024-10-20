import tkinter as tk
from tkinter import messagebox, Text, Scrollbar, VERTICAL, RIGHT, Y
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
    global right_frame_visible
    details = json.dumps(resource_details[url], indent=4)
    details_text.delete('1.0', tk.END)  # Clear the existing text
    details_text.insert(tk.END, details)  # Insert new details
    if not right_frame_visible:
        right_frame.pack(side='right', fill='both', expand=True)
        right_frame_visible = True

def toggle_right_panel():
    global right_frame_visible
    if right_frame_visible:
        right_frame.pack_forget()
        right_frame_visible = False
    else:
        right_frame.pack(side='right', fill='both', expand=True)
        right_frame_visible = True

def sort_by_name():
    sorted_resources = sorted(config['resources'], key=lambda x: x['name'])
    display_resources(sorted_resources)

def sort_by_url():
    sorted_resources = sorted(config['resources'], key=lambda x: x['url'])
    display_resources(sorted_resources)

def display_resources(resources):
    for widget in resource_frame.winfo_children():
        widget.destroy()

    # Add table headers to resource frame
    header_frame = tk.Frame(resource_frame, bg=bg_color)
    header_frame.pack(fill='x', pady=5)
    tk.Label(header_frame, text="", width=3, anchor='w', bg=bg_color).pack(side='left', padx=10)  # Placeholder for graphic
    tk.Label(header_frame, text="Name", width=20, anchor='w', bg=bg_color).pack(side='left')
    tk.Label(header_frame, text="URL", width=40, anchor='w', bg=bg_color).pack(side='left')
    tk.Label(header_frame, text="Port", width=10, anchor='w', bg=bg_color).pack(side='left')

    # Add resource entries to resource frame
    for resource in resources:
        frame = tk.Frame(resource_frame, bg=bg_color)
        frame.pack(fill='x', pady=5)
        status_color, details = check_resource(resource['url'], resource['port'])
        status_label = tk.Canvas(frame, width=20, height=20, bg=bg_color, highlightthickness=0)
        circle_id = status_label.create_oval(2, 2, 18, 18, fill=status_color)
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
        resource_details[resource['url']] = details

config = load_config()
root = tk.Tk()
root.title("Resource Status")

status_labels = {}
circle_ids = {}
resource_details = {}  # Dictionary to store detailed data for each resource
last_refresh_time = tk.StringVar()
status_time = tk.StringVar()
last_update = time.time()
right_frame_visible = False

bg_color = root.cget("bg")

# Create a menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Placeholder", command=lambda: messagebox.showinfo("Info", "This is a placeholder."))

# Add sorting options to menu
sort_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Sort", menu=sort_menu)
sort_menu.add_command(label="By Name", command=sort_by_name)
sort_menu.add_command(label="By URL", command=sort_by_url)

# Create main frames
main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(side='top', fill='both', expand=True)

left_frame = tk.Frame(main_frame, bg=bg_color)
left_frame.pack(side='left', fill='both', expand=True)

right_frame = tk.Frame(main_frame, bg=bg_color)

# Add a scrollbar to the left frame using a Canvas
canvas = tk.Canvas(left_frame, bg=bg_color)
scrollbar = Scrollbar(left_frame, orient=VERTICAL, command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=bg_color)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

resource_frame = scrollable_frame

# Initial display of resources
display_resources(config['resources'])

# Add details text box to right frame
details_text = Text(right_frame, bg=bg_color)
details_text.pack(fill='both', expand=True)

# Add status bar at the bottom
status_frame = tk.Frame(root, bd=1, relief=tk.SUNKEN)
status_frame.pack(side='bottom', fill='x')
status_bar = tk.Label(status_frame, textvariable=status_time, anchor='w')
status_bar.pack(side='left')

# Add a button to toggle the right panel
toggle_button = tk.Button(left_frame, text="Toggle Details Panel", command=toggle_right_panel)
toggle_button.pack(pady=10)

update_status()  # Initial call to start the periodic polling
update_time()  # Initial call to start the time update

root.mainloop()
