import psutil
import time
import os
from pynput import keyboard, mouse

# Configuration
distracting_apps = ['notepad.exe']  # List of apps to monitor
time_limit = 60 * 30  # Time limit in seconds (30 minutes)
keystroke_threshold = 10  # Number of keystrokes before closing apps
scroll_threshold = 5  # Number of scrolls before closing apps

# Track usage of apps
app_usage = {}
keystroke_count = 0
scroll_count = 0
is_dormant = False  # State to track if the script is dormant

def get_current_apps():
    """Get list of running processes."""
    try:
        process_list = [process.info['name'].lower() for process in psutil.process_iter(['name'])]
        return process_list
    except Exception as e:
        print(f"Error retrieving current apps: {e}")
        return []

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
    global keystroke_count, scroll_count, is_dormant

    # Start listeners for keyboard and mouse
    listener_keyboard = keyboard.Listener(on_press=on_press)
    listener_mouse = mouse.Listener(on_scroll=on_scroll)

    listener_keyboard.start()
    listener_mouse.start()

    print("Monitoring started. Press Ctrl+C to stop.")

    try:
        while True:
            if is_dormant:
                # Check if any distracting app is opened to wake up the monitor
                active_apps = get_current_apps()
                if any(app in active_apps for app in distracting_apps):
                    print("Waking up monitoring due to opening a distracting app.")
                    is_dormant = False
                time.sleep(1)  # Sleep while dormant
                continue

            active_apps = get_current_apps()
            current_time = time.time()

            for app in distracting_apps:
                if app in active_apps:
                    if app not in app_usage:
                        # App just opened, start tracking
                        app_usage[app] = current_time
                        print(f"Started monitoring {app}.")
                    else:
                        # Track how long the app has been open
                        elapsed_time = current_time - app_usage[app]
                        # Close the app if it exceeds the time limit
                        if elapsed_time >= time_limit:
                            os.system(f'taskkill /f /im {app}')  # Force close the app
                            print(f"{app} closed due to time limit.")
                            del app_usage[app]  # Stop monitoring this app until it's opened again
                            is_dormant = True  # Go dormant after closing the app
                    break  # Exit after checking one app to avoid redundant checks

            # Check keystrokes and mouse scrolls
            if keystroke_count >= keystroke_threshold or scroll_count >= scroll_threshold:
                for app in distracting_apps:
                    os.system(f'taskkill /f /im {app}')  # Force close all distracting apps
                    print(f"{app} closed due to excessive usage.")
                app_usage.clear()  # Clear all app usage tracking after closing
                keystroke_count = 0  # Reset counts after closing
                scroll_count = 0
                is_dormant = True  # Go dormant after closing the apps

            # Check every 1 second to avoid infinite looping
            time.sleep(1)

    except KeyboardInterrupt:
        print("Monitoring stopped.")
    finally:
        listener_keyboard.stop()
        listener_mouse.stop()

# Run the monitoring function
monitor_apps()