import os
import inquirer
from inquirer.errors import ValidationError
from colors import color

import configer
from shared import EVRTheme, EmuVRText


# Extra incompatible systems that might still include unnecessary CRC calculations and get included in the playlist
incompatible_systems = ("GameCube", "Wii")


def is_evr_path(path) -> bool:
    return os.path.exists(os.path.join(path, "Game Scanner", "emuvr_playlist.txt"))


def validate_evr_path(_, path) -> bool:
    normpath = os.path.abspath(path)
    if is_evr_path(normpath):
        return True
    else:
        raise ValidationError('', reason=f'"{color(normpath, fg=8)}" is not a valid EmuVR folder. Make sure you\'ve '
                                         f'ran Game Scanner before.')


def prompt_evr_path():
    ans = inquirer.prompt(
        [
            inquirer.Text('path', message=f"Where is your {EmuVRText} folder?", validate=validate_evr_path),
        ],
        theme=EVRTheme())

    return os.path.abspath(ans['path'])


def netplaylist():
    if configer.config.evrconfig.evrdir.value is None:
        configer.config.evrconfig.evrdir.value = prompt_evr_path()
        configer.save()

    evrdir = configer.config.evrconfig.evrdir.value
    evrplaylist = os.path.join(evrdir, "Game Scanner", "emuvr_playlist.txt")
    print(f"Generating playlist from {color(evrplaylist, fg=8)}...")

    # Create readable playlist table
    with open(evrplaylist, 'r', encoding='utf-8-sig') as file:
        playlistFile = file.read().splitlines()

    playlist = {}
    pathToSystem = {}
    for i in range(0, len(playlistFile), 3):
        name = playlistFile[i + 1]
        crc = playlistFile[i + 2].split("|")[0].strip()

        coreFolder = os.path.join(evrdir, os.path.dirname(playlistFile[i]))

        system = pathToSystem.get(coreFolder, "Unknown")
        coreFile = os.path.join(coreFolder, "emuvr_core.txt")

        if system == "Unknown":
            coreFileAvailable = os.path.exists(coreFile)
            while not coreFileAvailable and coreFolder != evrdir:
                coreFolder = os.path.dirname(coreFolder)
                coreFile = os.path.join(coreFolder, "emuvr_core.txt")
                coreFileAvailable = os.path.exists(coreFile)

            if coreFileAvailable:
                with open(coreFile, 'r') as file:
                    firstLine = file.readline()
                    system = firstLine.split('"')[1]
                    pathToSystem[coreFolder] = system
            else:
                print(f"{color('WARNING:', fg=9)} Could not find core file for {color(name, fg=8)}; game will be "
                      f"uncategorized. Make sure you've ran Game Scanner on this directory before, but if this issue "
                      f"persits, please report it as an issue on GitHub.")

        if (not system.startswith("Music") and not system.startswith("Video")) and (
                crc == "DETECT" or crc == "00000000" or system in incompatible_systems):
            continue

        if playlist.get(system) is None:
            playlist[system] = [[], 0]

        playlist[system][0].append((name, crc))
        if len(crc) > playlist[system][1]:
            playlist[system][1] = len(crc)

    # Write human-readable playlist to file
    with open("evrnetplaylist.txt", 'w') as file:
        writeStr = ""

        for system, gameList in playlist.items():
            writeStr += f"[ {system} ]\n"
            for game in gameList[0]:
                if game[1] == "DETECT" or game[1] == "00000000":  # should only be Music and Videos
                    writeStr += f"{game[0]}\n"
                else:
                    writeStr += f"{game[1]:>{gameList[1]}} | {game[0]}\n"

            writeStr += "\n"

        file.write(writeStr)

    print(f"{color('Successfully created Netplay playlist at', fg=10)} {color(os.path.realpath(file.name), fg=8)}"
          f"{color('!', fg=10)}")

