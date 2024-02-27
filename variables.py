from tkinter import StringVar
import customtkinter as ctk
from PIL import Image
from path_manager import resource_path


## initalize the variables to be used throughout the app
def init():
    global current_payment, button_position, screen_sizes
    global form, root, icons, popups

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.resizable(False, False)

    current_payment = 1
    button_position = 101 # vertical position in pixels
    screen_sizes = {'ws': root.winfo_screenwidth(), 'hs': root.winfo_screenheight()}
    form = {'version': "v0.9.0", 'status': StringVar(value="Ready")}
    popups = {'printer': None, 'history': None}
    icons = {}

    icons_specs = {
        'history': [20,20],
        'folder': [20,20],
        'clear': [20,20],
        'print': [20,20],
        'docx': [20,20],
        'pdf': [20,20],
        'conduct': [20,73],
        'testData': [20,63],
        'testPrnt': [20,36],
        'printConduct': [30,46],
        'printRetainer': [30,46],
    }

    for icon_name in list(icons_specs.keys()):
        h = icons_specs[icon_name][0]
        w = icons_specs[icon_name][1]

        icons[icon_name] = ctk.CTkImage(
            light_image=None,
            dark_image=Image.open(resource_path("assets\\icons\\" + icon_name + ".png")),
            size=(w, h)
        )




