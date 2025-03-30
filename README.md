# Limiter
If certain conditions are met—such as reaching a set number of keystrokes or mouse scrolls, or exceeding a time limit for app usage—Limiter will automatically close distracting apps to ensure you stay on track. Perfect for anyone looking to reduce distractions and enhance focus while working or studying.


██╗  ██╗██╗      █████╗ ████████╗██╗   ██╗
██║ ██╔╝██║     ██╔══██╗╚══██╔══╝██║   ██║
█████╔╝ ██║     ███████║   ██║   ██║   ██║
██╔═██╗ ██║     ██╔══██║   ██║   ██║   ██║
██║  ██╗███████╗██║  ██║   ██║   ╚██████╔╝
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ 


✦ Project # 4: Limiter  
✦ Author: K1atu  
✦ Motto: "Limit distractions, stay focused!"

## Features
1. **App Monitoring:** Tracks usage time of distracting apps (e.g., Notepad). If the app exceeds the time limit, it is forcefully closed.
2. **Keystroke Monitoring:** Tracks the number of keystrokes. If the keystroke count exceeds the threshold, distracting apps are closed.
3. **Scroll Monitoring:** Monitors mouse scrolls. If scroll activity exceeds the threshold, distracting apps are closed.
4. **Dynamic Monitoring:** Once a distracting app is closed, the script will stop monitoring until the app is reopened.

## Installation

### Prerequisites
You need the following libraries to run this script:

1. `psutil` - For tracking running processes.
2. `pynput` - For monitoring keyboard and mouse inputs.
3. `time` - For controlling time limits and monitoring intervals.
4. `os` - For closing processes.

Install the required libraries using pip:

pip install pynput


## Disclaimer
This tool is intended for personal productivity management and is not for malicious use. Make sure to use it responsibly on your own devices


