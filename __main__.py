import os
import inquirer
from colors import color

from shared import EVRTheme
from tools.cuecreator import cuecreator

version = "0.1.0"

# Set window title
os.system("TITLE EmuVRTools")

# Set up menu
print(f"{color('Emu', fg=14)}{color('VR', fg=13)}{color('Tools', fg=12)} {color(f'v{version}', fg=8)}")

while True:
    ans = inquirer.prompt([
        inquirer.List('tool', "Select Tool", choices=[
            ('Create music CUE sheet', 0),
            ('Generate Netplay game list', 1),
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
    print()
