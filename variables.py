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
    button_position = 101  # vertical position in pixels
    screen_sizes = {"ws": root.winfo_screenwidth(), "hs": root.winfo_screenheight()}
    form = {"version": "v1.1.4", "status": StringVar(value="Ready")}
    popups = {"printer": None, "history": None, "elem": {}}
    icons = {}

    icons_specs = {
        "history": None,
        "folder": None,
        "clear": None,
        "print": None,
        "docx": None,
        "pdf": None,
        "conduct": None,
        "testData": None,
        "testPrnt": None,
        "payauth": None,
        "printConduct": None,
        "printRetainer": None,
    }

    # define the 
    for icon_name in list(icons_specs.keys()):
        icons_specs[icon_name] = Image.open(resource_path("assets\\icons\\" + icon_name + ".png"))

        icons[icon_name] = ctk.CTkImage(
            light_image = None,
            dark_image = icons_specs[icon_name],
            size = icons_specs[icon_name].size,
        )
