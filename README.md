# Ret.A.G
`RET`ainer `A`greement `G`enerator provides a GUI for AMCAIM staff that allows easy creation of retainer agreements when working with clients 

## Usage
- download the latest build.
- unzip the contents.
- run the executable.

## Build from source files
install dependencies:
- [CTkMessagebox](https://pypi.org/project/CTkMessagebox/)
- [pyinstaller/](https://pypi.org/project/pyinstaller/)
- [customtkinter](https://pypi.org/project/customtkinter/)
- [docx2pdf](https://pypi.org/project/docx2pdf/)
- [python-docx](https://pypi.org/project/python-docx/)

then run the command:
```python -m PyInstaller main.py --onefile -w --icon=assets\logo.ico --name="RetAG"```
