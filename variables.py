from tkinter import StringVar
import customtkinter as ctk
import tkinter as tk

from path_manager import resource_path


def init():
    global current_payment
    global button_position
    global form
    global root
    global screen_sizes
    global icons
    global popups

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

    icon_list = ['history', 'folder', 'clear', 'print', 'docx', 'pdf', 'conduct', 'testData', 'testPrnt', 'printConduct', 'printRetainer']
    for index, icon_name in enumerate(icon_list):
        icons[icon_name] = tk.PhotoImage(file=resource_path("assets\\icons\\" + icon_list[index] + ".png"))




