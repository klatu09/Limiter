import psutil
import time
import os
from pynput import keyboard, mouse

# List of distracting apps (e.g., games, social media)
distracting_apps = ['chrome.exe', 'steam.exe', 'discord.exe']

# Time limit (in seconds) to close apps after usage limit (60 minutes = 3600 seconds)
time_limit = 60 * 60  # 1 hour

# Track usage of apps
app_usage = {}

# Track keystrokes and mouse scrolls
keystroke_count = 0
scroll_count = 0

def get_current_apps():
    """Get list of running processes."""
    process_list = []
    for process in psutil.process_iter(['pid', 'name']):
        process_list.append(process.info['name'].lower())
    return process_list

def on_press(key):
    """Track keystrokes."""
    global keystroke_count
    keystroke_count += 1

def on_scroll(x, y, dx, dy):
    """Track mouse scrolls (both up and down)."""
    global scroll_count
    if dy != 0:  # Scroll in either direction
        scroll_count += 1

def monitor_apps():
    """Monitor apps and track their usage time."""
    global keystroke_count, scroll_count

    # Start listeners for keyboard and mouse
    listener_keyboard = keyboard.Listener(on_press=on_press)
    listener_mouse = mouse.Listener(on_scroll=on_scroll)

    listener_keyboard.start()
    listener_mouse.start()

    while True:
        active_apps = get_current_apps()
        current_time = time.time()

        for app in distracting_apps:
            if app in active_apps:
                if app not in app_usage:
                    app_usage[app] = current_time
                else:
                    elapsed_time = current_time - app_usage[app]
                    # Close the app if it's been running for more than the time limit
                    if elapsed_time >= time_limit:
                        os.system('taskkill /f /im ' + app)  # Force close the app

        # Check keystrokes and mouse scrolls
        if keystroke_count >= 5000:
            for app in distracting_apps:
                os.system('taskkill /f /im ' + app)  # Force close all distracting apps
            break  # Exit the script after closing apps

        if scroll_count >= 150:
            for app in distracting_apps:
                os.system('taskkill /f /im ' + app)  # Force close all distracting apps
            break  # Exit the script after closing apps

        time.sleep(60)  # Check every minute

# Run the monitoring function
monitor_apps()
