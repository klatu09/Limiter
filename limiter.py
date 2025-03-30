import psutil
import time
import os
from pynput import keyboard, mouse

# List of apps 
distracting_apps = ['notepad.exe']
# Path to the executable to reopen (example for notepad, adjust for other apps)
app_paths = {
    'notepad.exe': 'C:\\Windows\\System32\\notepad.exe'  # Update path as needed
}

# Time limit (in seconds) to close apps after usage limit (60 minutes = 3600 seconds)
time_limit = 60 * 30  # 30 minutes
grace_period = 10  # Seconds to wait after app is closed before checking again

# Track usage of apps
app_usage = {}
app_closed_time = {}

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

        # Check if any distracting app is currently running
        for app in distracting_apps:
            if app in active_apps:
                if app not in app_usage:
                    # App just opened, start tracking
                    app_usage[app] = current_time
                    if app in app_closed_time and (current_time - app_closed_time[app]) > grace_period:
                        # If app was previously closed, it should now be monitored again
                        print(f"Restarted monitoring {app}.")
                else:
                    # Track how long the app has been open
                    elapsed_time = current_time - app_usage[app]
                    # Close the app if it exceeds the time limit
                    if elapsed_time >= time_limit:
                        os.system('taskkill /f /im ' + app)  # Force close the app
                        # Log when it was closed
                        app_closed_time[app] = current_time

        # If the app is closed, restart it automatically after the grace period
        for app in distracting_apps:
            if app not in active_apps:  # If the app is closed
                if app not in app_closed_time or (current_time - app_closed_time[app]) > grace_period:
                    print(f"{app} is closed. Restarting...")
                    if app in app_paths:  # Ensure the path is defined for the app
                        os.system(f'"{app_paths[app]}"')  # Open the app again

        # Check keystrokes and mouse scrolls (no break, so the script keeps running)
        if keystroke_count >= 10:
            for app in distracting_apps:
                os.system('taskkill /f /im ' + app)  # Force close all distracting apps

        if scroll_count >= 5:
            for app in distracting_apps:
                os.system('taskkill /f /im ' + app)  # Force close all distracting apps

        time.sleep(0.1)  # Check every 0.1 seconds

# Run the monitoring function
monitor_apps()
