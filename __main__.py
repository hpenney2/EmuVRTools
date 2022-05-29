import os
import inquirer
from colors import color

from shared import EVRTheme, EmuVRText
from tools.cuecreator import cuecreator
from tools.netplaylist import netplaylist

version = "0.1.0 Beta"

# Set window title
os.system("TITLE EmuVRTools")

# Set up menu
print(f"{EmuVRText}{color('Tools', fg=12)} {color(f'v{version}', fg=8)}")

while True:
    ans = inquirer.prompt([
        inquirer.List('tool', "Select Tool", choices=[
            ('Create music CUE sheet', 0),
            ('Generate Netplay playlist', 1),
            ('Exit', -1)
        ], carousel=True)
    ],
        theme=EVRTheme())

    if ans is None:
        break

    if ans['tool'] == -1:
        exit(0)
    elif ans['tool'] == 0:
        cuecreator()
    elif ans['tool'] == 1:
        netplaylist()
    print()
