# Ret.A.G
`RET`ainer `A`greement `G`enerator provides a GUI for AMCAIM staff that allows easy creation of retainer agreements when working with clients.

## Usage
- download the latest build.
- unzip the contents.
- run the executable.

## Build using script (recommended):
### Run `build_app_main.py` with optional flags:
- no flags will build the exe with the next minor build number.
- `--selector` to show version selector in the terminal.
- `--deps` to install dependencies.

## Build manually:
1. run ```pip install CTkMessagebox pyinstaller customtkinter docx2pdf python-docx python-dateutil``` install dependencies:
    - [CTkMessagebox](https://pypi.org/project/CTkMessagebox/)
    - [pyinstaller](https://pypi.org/project/pyinstaller/)
    - [customtkinter](https://pypi.org/project/customtkinter/)
    - [docx2pdf](https://pypi.org/project/docx2pdf/)
    - [python-docx](https://pypi.org/project/python-docx/)
    - [python-dateutil](https://pypi.org/project/python-dateutil/)

2. run ```python -m PyInstaller main.py --onefile -w --icon=assets\logo.ico --name="RetAG"```
