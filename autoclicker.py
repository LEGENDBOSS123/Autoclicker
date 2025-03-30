# python -m nuitka --standalone --macos-app-mode=gui --macos-create-app-bundle --macos-app-name="Autoclicker" autoclicker.py
import AppKit
import time
import threading
import pyautogui
import subprocess
from pynput import keyboard

pyautogui.PAUSE = 0
EXIT_KEY = "Q"
TOGGLE_KEY = "T"
autoclickerOn = False
stop_clicker = False

def get_click_interval():
    try:
        interval = subprocess.run(
            ['osascript', '-e', 'text returned of (display dialog "Enter click interval (seconds):" default answer "1.0")'],
            capture_output=True, text=True).stdout.strip()
        if interval == "":
            log("Autoclicker canceled.")
            AppKit.NSApp().terminate_(None)
            return None
        return float(interval)
    except ValueError:
        log("Invalid input. Autoclicker canceled.")
        return None

def log(msg):
    subprocess.run(["osascript", "-e", f'display notification "{msg}" with title "Autoclicker"'])

def clicker():
    while not stop_clicker:
        if autoclickerOn:
            pyautogui.click()
        time.sleep(autoclickerInterval)

def on_release(key):
    global autoclickerOn, stop_clicker
    try:
        if key.char.upper() == EXIT_KEY:
            stop_clicker = True
            log("Autoclicker terminated.")
            AppKit.NSApp().terminate_(None)
            return False
        elif key.char.upper() == TOGGLE_KEY:
            autoclickerOn = not autoclickerOn
            log("Autoclicker " + ("on" if autoclickerOn else "off") + ".")
    except AttributeError:
        pass

AppKit.NSApplication.sharedApplication()
autoclickerInterval = get_click_interval()

if autoclickerInterval is not None:
    log(f"Autoclicker started and will click every {autoclickerInterval} seconds.\nPress {TOGGLE_KEY} to toggle autoclicker.\nPress {EXIT_KEY} to exit.")

    threading.Thread(target=clicker, daemon=True).start()
    with keyboard.Listener(on_release=on_release) as listener:
        
        AppKit.NSApp().run()
