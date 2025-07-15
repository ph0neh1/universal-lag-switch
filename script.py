# Lagswitch for any game/application by ph0neh1

import keyboard
import subprocess
import os
import sys
import ctypes
import psutil
import time
import cmd
import random

# Variables
pid = None
keybind = None
rule_name = None
SwitchBool = False

#Colors
class TextColor:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"

#Funcitions
def log(message, color, raw):
    if color in vars(TextColor).values():
        formatted = "[" + color + "universal-lagswitch" + TextColor.RESET + "] " + message
        if raw:
            return formatted
        else:
            print(formatted)
    else:
        print("[universal-lagswitch] " + message)

def updatefirewall(action):
    if action == "block":
        cmd = ['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name=' + rule_name, 'dir=out', 'action=block', 'program=' + psutil.Process(pid).exe()]
    else:
        cmd = ['netsh', 'advfirewall', 'firewall', 'delete', 'rule', 'name=' + rule_name]
    subprocess.run(cmd, creationflags=subprocess.CREATE_NO_WINDOW)


# If operating system is Windows | If running as Admin
if os.name != "nt":
    log("You are not running a supported operating system", TextColor.RED, False)
    sys.exit()

if not ctypes.windll.shell32.IsUserAnAdmin():
    log("You need to run universal-lagswitch as administrator", TextColor.RED, False)
    sys.exit()

# Aqquiring/Validating PID
pid = input(log("Please input PID:", TextColor.PURPLE, True) + " ")

try:
    pid = int(pid)
except ValueError:
    log('"' + str(pid) + '"' + " is not a number", TextColor.RED, False)
    sys.exit()

if not psutil.pid_exists(pid):
    log(str(pid) + " is not a valid PID", TextColor.RED, False)
    sys.exit()

#Getting keybind
log("You will now be prompted to set a keybind for the lagswitch", TextColor.GREEN, False)
log("Press any key...", TextColor.PURPLE, False)

while True:
    event = keyboard.read_event(suppress=True)
    if event.event_type == keyboard.KEY_DOWN:
        keybind = event.name
        break

# clears terminal and creates rule name
os.system('cls||clear')
rule_name = str(pid) + "ra1n"

# Waiting for inputs
log("universal-lagswitch is now running!", TextColor.YELLOW, False)
log('Your keybind is "' + keybind + '"', TextColor.YELLOW, False)
log('Before exiting make sure lagswitch is OFF!', TextColor.RED, False)

while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        if keybind == event.name and SwitchBool == False:
            updatefirewall('block')
            log("Blocked " + str(pid), TextColor.BLUE, False)
            SwitchBool = True
        else:
            if keybind == event.name:
                updatefirewall('unblock')
                log("Unblocked " + str(pid), TextColor.BLUE, False)
                SwitchBool = False
