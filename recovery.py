# This script can be used to delete old rules in case of accidental exits/crashes.

import subprocess
import re
import os
import sys
import cmd
import ctypes

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

def cleanup_ra1n_rules():
    result = subprocess.run(
        ['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=all'],
        capture_output=True,
        text=True
    )

    rules_output = result.stdout
    pattern = re.compile(r'Rule Name:\s+(\d+ra1n\S*)', re.IGNORECASE)
    matches = pattern.findall(rules_output)

    if not matches:
        log("No rules were found/deleted", TextColor.RED, False)

    unique_rules = set(matches)

    for rule in unique_rules:
        log('Deleting rule: "' + str(rule) + '"', TextColor.GREEN, False)
        cmd = ['netsh', 'advfirewall', 'firewall', 'delete', 'rule', 'name=' + rule]
        subprocess.run(cmd, creationflags=subprocess.CREATE_NO_WINDOW)

# start
if os.name != "nt":
    log("You are not running a supported operating system", TextColor.RED, False)
    sys.exit()

if not ctypes.windll.shell32.IsUserAnAdmin():
    log("You need to run universal-lagswitch as administrator", TextColor.RED, False)
    sys.exit()

if __name__ == "__main__":
    log("universal-lagswitch recovery tool", TextColor.PURPLE, False)
    cleanup_ra1n_rules()
