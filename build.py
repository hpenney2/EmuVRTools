import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=EmuVRTools',
    '--onefile',
    '--icon=logo.ico',
    '__main__.py'
])
