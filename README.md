# Ret.A.G
`RET`ainer `A`greement `G`enerator provides a GUI for AMCAIM staff that allows easy creation of retainer agreements when working with clients.

## Usage
- download the latest build.
- unzip the contents.
- run the executable.

## Build using script (recommended):
### Run `builder.py` with optional flags:
- no flags will build the exe with the next minor build number.
- `--no-selector` to skip version selector and automatically build using the next minor build number.
- `--deps` to install dependencies.

## Build manually:
1. run ```pip install CTkMessagebox pyinstaller customtkinter docx2pdf python-docx python-dateutil``` to install dependencies:
    - [CTkMessagebox](https://pypi.org/project/CTkMessagebox/)
    - [pyinstaller](https://pypi.org/project/pyinstaller/)
    - [customtkinter](https://pypi.org/project/customtkinter/)
    - [docx2pdf](https://pypi.org/project/docx2pdf/)
    - [python-docx](https://pypi.org/project/python-docx/)
    - [python-dateutil](https://pypi.org/project/python-dateutil/)

2. run ```python -m PyInstaller main.py --onefile -w --icon=assets\icons\logo.ico --name="RetAG"```
