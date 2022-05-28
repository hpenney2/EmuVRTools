<p align="center" style="margin-bottom: 0px !important;">
  <img width="200" src="logo.png" alt="EmuVRTools Logo" align="center">
</p>
<h1 align="center" style="margin-top: 0px;">EmuVRTools</h1>
A collection of tools designed for use with EmuVR.

If you have any questions or ideas for new tools, please submit an issue or ping me on Discord! (@hp)  
Additionally, if you would like to add existing tools to the repo, please submit an issue and/or a pull request.

<sup>***EmuVRTools is not associated with EmuVR.***</sup>

### Installation
Download the latest standalone `.exe` release from [the GitHub releases page](https://github.com/hpenney2/EmuVRTools/releases) and run it!

If you don't want to use the executable and have Python installed,
you can also download and extract the latest stable source `.zip` from the releases page and refer to the [Installing from source](#installing-from-source) section.

### Installing from source
**Requirements:**
- Python 3.9 or later
- Pipenv (`pip install pipenv`)
- The extracted source code (clone the repo or download and extract the latest source `.zip` from the releases page)

1. In a terminal/command prompt, ensure that you are in the source directory and run `pipenv install` to install dependencies.
2. Run `pipenv run python __main__.py` to start EmuVRTools.

Additionally, if you would like to build an executeable from source:
1. Run `pipenv install --dev` to install all dependencies.
2. Run `pipenv run python build.py` to build the `.exe` with `pyinstaller`. This may take a while.
3. After it finishes, the `dist` directory will contain the built `.exe` and the `EmuVRTools.spec` file.