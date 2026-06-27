import subprocess
import tkinter as tk
import sys
import os
import json
from tkinter import messagebox

# Path to the Python interpreter in your virtual environment
python_path = r"D:\Project\virtualenv\ytvirtual\Scripts\python.exe"

# Paths to your main scripts
main_youtube_path = r"D:\Project\code\main.py"
main_shorts_path = r"D:\Project\code\mainShorts.py"

# Variables to store process references
youtube_process = None
shorts_process = None

# Function to save the Chrome path to a JSON file
def save_chrome_path(chrome_path_entry):
    chrome_path = chrome_path_entry.get()

    if not chrome_path:
        messagebox.showerror("Error", "Please enter a valid Chrome executable path.")
        return

    # Save the Chrome path to a JSON file
    config = {"chrome_path": chrome_path}

    try:
        with open("config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        messagebox.showinfo("Success", "Chrome path saved successfully.")
        enable_buttons()  # Enable the buttons after saving the config
    except Exception as e:
        None
# Function to load Chrome path from config.json
def load_chrome_path():
    try:
        if os.path.exists("config.json"):
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                chrome_path = config.get("chrome_path", "")
                return chrome_path
        else:
            return None
    except Exception as e:
        print(f"Error loading config.json: {e}")
        return None

# Function to enable the buttons once configuration is completed
def enable_buttons():
    chrome_path = load_chrome_path()
    if chrome_path:
        button_youtube.config(state=tk.NORMAL)
        button_shorts.config(state=tk.NORMAL)
        button_off.config(state=tk.NORMAL)
        print("Chrome path found. Buttons enabled.")
    else:
        print("No valid Chrome path found. Buttons remain disabled.")
        button_youtube.config(state=tk.DISABLED)
        button_shorts.config(state=tk.DISABLED)

# Function to start YouTube
def start_youtube():
    global youtube_process
    youtube_process = subprocess.Popen([python_path, main_youtube_path])
    print("YouTube started.")

# Function to start Shorts
def start_shorts():
    global shorts_process
    shorts_process = subprocess.Popen([python_path, main_shorts_path])
    print("YouTube Shorts started.")

# Function to terminate all processes
def close_all():
    global youtube_process, shorts_process
    if youtube_process is not None:
        youtube_process.terminate()
        youtube_process = None
        print("Terminated YouTube process.")
    if shorts_process is not None:
        shorts_process.terminate()
        shorts_process = None
        print("Terminated Shorts process.")
    root.destroy()
    sys.exit()

# GUI setup
root = tk.Tk()
root.title("YouTube Control")

# Bind the window close event (clicking the "X" button) to `close_all`
root.protocol("WM_DELETE_WINDOW", close_all)

# Check if configuration exists and prompt for it if needed
if not os.path.exists("config.json"):
    # Show configuration input if config.json does not exist
    config_frame = tk.Frame(root)
    config_frame.pack(padx=20, pady=20)

    chrome_path_label = tk.Label(config_frame, text="Enter Chrome Executable Path:")
    chrome_path_label.grid(row=0, column=0, pady=5)

    chrome_path_entry = tk.Entry(config_frame, width=50)
    chrome_path_entry.grid(row=1, column=0, pady=5)

    save_button = tk.Button(config_frame, text="Save Chrome Path", command=lambda: save_chrome_path(chrome_path_entry))
    save_button.grid(row=2, column=0, pady=10)

    cancel_button = tk.Button(config_frame, text="Cancel", command=root.quit)
    cancel_button.grid(row=3, column=0, pady=10)

    root.mainloop()
else:
    # If config.json exists, enable the buttons
    button_youtube = tk.Button(root, text="YouTube", command=start_youtube)
    button_youtube.pack(pady=10)

    button_shorts = tk.Button(root, text="Shorts", command=start_shorts)
    button_shorts.pack(pady=10)

    button_off = tk.Button(root, text="Off", command=close_all)
    button_off.pack(pady=10)

    # Initially disable the buttons until configuration is completed
    button_youtube.config(state=tk.DISABLED)
    button_shorts.config(state=tk.DISABLED)
    button_off.config(state=tk.DISABLED)

    enable_buttons()  # Check the config.json and enable buttons accordingly

    root.mainloop()
#creatred by vSMCA0454