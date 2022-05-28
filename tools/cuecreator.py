import os
import os.path
import inquirer
import inquirer.errors
from colors import color
from pathvalidate import is_valid_filename

import configer
from shared import EVRTheme


def validateCUEname(_, name: str) -> bool:
    if is_valid_filename(name):
        return True
    else:
        raise inquirer.errors.ValidationError('', reason=f'"{name}" is not a valid filename.')


def newPreset():
    ans = inquirer.prompt(
        [
            inquirer.Path('path', message=f"What directory contains your {color('.ogg', fg=8)} files?",
                          path_type=inquirer.Path.DIRECTORY,
                          exists=True, normalize_to_absolute_path=True),
            inquirer.Text('name', message="What do you want to name this? "
                                          "(this will also be the name of the CUE sheet)", validate=validateCUEname),
            inquirer.Confirm('save', message="Do you want to save this as a preset?", default=False),
        ],
        theme=EVRTheme())

    ans['path'] = os.path.abspath(ans['path'])

    if ans['save']:
        newValue = configer.config.evrconfig.cuecreator.presets.value + [[ans['name'], ans['path']]]
        configer.config.evrconfig.cuecreator.presets.set(newValue)
        configer.save()

    return ans['name'], ans['path']


def confirmOverwrite(existing) -> bool:
    ans = inquirer.prompt(
        [
            inquirer.Confirm('overwrite', message=f"A CUE sheet already exists at {color(existing, fg=8)}. Overwrite?",
                             default=False)
        ],
        theme=EVRTheme())

    return ans['overwrite']


trackFormat = """FILE "{0}" OGG
  TRACK {1:02d} AUDIO
    INDEX 00 00:00:00"""


def cuecreator():
    name = None
    path = None

    presets = configer.config.evrconfig.cuecreator.presets
    if len(presets.value) != 0:
        ans = inquirer.prompt(
            [inquirer.List('preset', "Which preset do you want to use?",
                           choices=[(pset[0], i) for i, pset in enumerate(presets.value)] + [
                               (f"{color('Other', fg=8)}", -1)],
                           carousel=True)],
            theme=EVRTheme())
        name, path = presets.value[ans['preset']] if ans['preset'] != -1 else newPreset()
    else:
        name, path = newPreset()

    print(f"Generating audio CUE sheet for {color(path, fg=8)}")

    cue = ""
    existingCueFile = None
    trackNum = 0
    for file in sorted(os.listdir(path), key=str.casefold):
        if trackNum >= 99:
            print(f"{color('Reached track limit (99); unable to add more tracks.', fg=9)} "
                  f"You may need to split your audio into multiple discs if you would like to add more.")
            break

        if file.endswith(".ogg"):
            trackNum += 1
            if cue != "":
                cue += "\n"
            cue += trackFormat.format(file, trackNum)
            print(f"Added {color(file, fg=10)} as track {color(str(trackNum), fg=1)}")
        elif file.lower() == name.lower() + ".cue":
            existingCueFile = file

    print("\nCUE sheet ready!")
    if existingCueFile:
        if not confirmOverwrite(os.path.join(path, existingCueFile)):
            print(f"{color('Cancelled.', fg=9)}")
            return

    with open(os.path.join(path, name + ".cue"), 'wb') as f:
        f.write(cue.encode('utf-8'))

    print(f"{color('Successfully created CUE sheet at', fg=10)} {color(os.path.join(path, name + '.cue'), fg=8)}"
          f"{color('!', fg=10)}")

