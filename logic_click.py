import os
import customtkinter as ctk
import datetime as dt
import variables as vars
import names
import random
import logic_form
import win32print, win32api
import time
import logic_history as history
from tkinter import StringVar
from dateutil import relativedelta as rd
from docx import Document
from CTkXYFrame import *
from CTkMessagebox import CTkMessagebox as popup


## HELPER: set the status to reflect which printer is being used, and send the file to be printed
def send_to_device(selected_printer, to_pdf, is_code_of_conduct):
    vars.form["status"].set("printing on device: " + selected_printer)
    generate_from_form(selected_printer, to_pdf, is_code_of_conduct)


## HELPER: generate a dictionary from the form and send it to the doc editor
def generate_from_form(to_printer, to_pdf, is_code_of_conduct):
    temp_list = []

    for i in range(len(vars.form["payment_list"])):
        if (
            len(vars.form["payment_list"][i]["amount"].get()) > 0
            and len(vars.form["payment_list"][i]["date"].get()) > 0
        ):
            temp_list.append(
                {
                    "amount": vars.form["payment_list"][i]["amount"].get(),
                    "date": vars.form["payment_list"][i]["date"].get(),
                }
            )

    fill_info = {
        "document_date": vars.form["document_date"].get(),
        "client_name": vars.form["client_name"].get(),
        "application_type": vars.form["application_type"].get(),
        "application_fee": vars.form["application_fee"].get(),
        "email_address": vars.form["email_address"].get(),
        "phone_number": vars.form["phone_number"].get(),
        "payment_list": temp_list,
    }

    isTaxIncluded = vars.form["include_taxes"].get()
    isOpenOutputActive = vars.form["open_output_switch"].get()
    isRetainerActive = vars.form["active_switch"].get()

    response = logic_form.generate(
        fill_info,
        isTaxIncluded,
        isOpenOutputActive,
        isRetainerActive,
        to_printer,
        to_pdf,
        is_code_of_conduct,
    )

    if to_printer == False:
        if response == False:
            vars.form["status"].set("Error")
        else:
            vars.form["status"].set("Agreement created")


## BUTTON: add the clicked amount as the total value of the case
def dollars(amount):
    vars.form["application_fee"].delete(0, "end")
    vars.form["application_fee"].insert(0, int(amount))


## BUTTON: sets the `date on document` to be today's date
def today():
    vars.form["document_date"].delete(0, "end")
    vars.form["document_date"].insert(0, dt.datetime.now().strftime("%d/%m/%Y"))
    vars.form["payment_list"][0]["date"].delete(0, "end")
    vars.form["payment_list"][0]["date"].insert(0, dt.datetime.now().strftime("%d/%m/%Y"))

    if vars.current_payment == 1:
        vars.form["plus_month_btn"] = ctk.CTkButton(
            vars.root,
            text="+1 month",
            border_width=0,
            corner_radius=4,
            bg_color="#343638",
            command=lambda: add_month(),
            width=60,
            height=25,
        )

        vars.form["plus_month_btn"].place(x=568, y=101)


## BUTTON: change the position of the `+1month` button
def reposition_plus_month(place_button):
    vars.form["plus_month_btn"].destroy()

    vars.form["plus_month_btn"] = ctk.CTkButton(
        vars.root,
        text="+1 month",
        border_width=0,
        corner_radius=4,
        bg_color="#343638",
        command=add_month,
        width=60,
        height=25,
    )

    if place_button:
        vars.form["plus_month_btn"].place(x=568, y=vars.button_position)


## BUTTON: adds 1 month to the previous date in the payments list
def add_month():
    pixels_to_next_row = 34

    if (
        vars.current_payment < 12
        and len(vars.form["payment_list"][vars.current_payment - 1]["date"].get()) != 0
    ):

        prev_payment_date = vars.form["payment_list"][vars.current_payment - 1]["date"].get()

        if prev_payment_date == "advance":
            prev_payment_date = dt.datetime.now().strftime("%d/%m/%Y")

        dt_object = dt.datetime.strptime(prev_payment_date, "%d/%m/%Y")
        dt_object = dt_object + rd.relativedelta(months=1)

        vars.form["payment_list"][vars.current_payment]["date"].delete(0, "end")
        vars.form["payment_list"][vars.current_payment]["date"].insert(0, dt_object.strftime("%d/%m/%Y"))

        vars.current_payment += 1

        if vars.current_payment < 12:
            vars.button_position += pixels_to_next_row
            vars.form["plus_month_btn"].place(x=568, y=vars.button_position)
        else:
            vars.form["plus_month_btn"].destroy()

    elif len(vars.form["payment_list"][0]["date"].get()) == 0:
        popup(
            title="Failed",
            message="Unable to add month as previous payment date is empty",
            corner_radius=4,
        )

    elif len(vars.form["payment_list"][vars.current_payment - 1]["date"].get()) < 8:
        vars.current_payment -= 1
        vars.button_position -= pixels_to_next_row
        reposition_plus_month(vars.button_position)
        add_month()


## BUTTON: populate the form with dummy data
def test_data():

    vars.form["status"].set("dummy data placed")

    client_name = names.get_full_name()
    application_fee = random.randint(1, 4) * 1000

    vars.form["document_date"].delete(0, "end")
    vars.form["client_name"].delete(0, "end")
    vars.form["application_type"].delete(0, "end")
    vars.form["application_fee"].delete(0, "end")
    vars.form["email_address"].delete(0, "end")
    vars.form["phone_number"].delete(0, "end")

    vars.form["document_date"].insert(0, "1/3/2024")
    vars.form["client_name"].insert(0, client_name)
    vars.form["application_type"].insert(0, random.choice(["EOI", "MPNP", "PR", "PGWP", "Citizenship"]))
    vars.form["application_fee"].insert(0, application_fee)
    vars.form["email_address"].insert(0, client_name.replace(" ", "").lower() + "@email.com")
    vars.form["phone_number"].insert(0, random.choice(["431", "204"]) + str(random.randint(1000000, 9999999)))

    installments = random.randint(1, 12)
    per_installment = float(application_fee / installments)

    for i in range(12):
        vars.form["payment_list"][i]["date"].delete(0, "end")
        vars.form["payment_list"][i]["amount"].delete(0, "end")

    for i in range(installments):
        m = str((3 + i) % 12 + 1)
        y = str(int((4 + i) / 12) + 2024)

        vars.form["payment_list"][i]["date"].insert(0, ("1/" + m + "/" + y))
        vars.form["payment_list"][i]["amount"].insert(0, "{:.2f}".format((per_installment)))


## BUTTON: reset the form and variables
def reset():
    vars.form["status"].set("form cleared")
    vars.form = logic_form.reset(vars.form)
    vars.form["include_taxes"].set(True)
    vars.form["open_output"].set(True)
    vars.current_payment = 1
    vars.button_position = 101

    reposition_plus_month(False)


## BUTTON: sets the date to be 'paid in advance' when clients cannot provide a specific date for payment
def advance():
    vars.form["payment_list"][0]["date"].delete(0, "end")
    vars.form["payment_list"][0]["date"].insert(0, "advance")

    if vars.current_payment == 1:
        reposition_plus_month(True)


## BUTTON: open the output folder
def output():
    output_dir = os.getcwd() + "\\output"
    os.startfile(output_dir)


## BUTTON: save the retainer as docx
def docx():
    vars.form["status"].set("writing docx")

    to_printer = False
    to_pdf = False
    is_code_of_conduct = False
    generate_from_form(to_printer, to_pdf, is_code_of_conduct)


## BUTTON: save the retainer as pdf
def pdf():
    vars.form["status"].set("creating pdf")

    to_printer = False
    to_pdf = True
    is_code_of_conduct = False
    generate_from_form(to_printer, to_pdf, is_code_of_conduct)


## BUTTON: print the retainer or code of conduct
def print_file(printer_list, to_pdf, is_code_of_conduct):
    to_printer = StringVar(value=win32print.GetDefaultPrinter())
    titlebar = "Print Code of Conduct" if is_code_of_conduct else "Print Retainer"

    if vars.popups["printer"] is None or not vars.popups["printer"].winfo_exists():
        vars.popups["printer"] = ctk.CTkToplevel()

        w = 300
        h = 200
        x = (vars.screen_sizes["ws"] / 2) - (w / 2)
        y = (vars.screen_sizes["hs"] / 2) - (h / 2)

        vars.popups["printer"].geometry("%dx%d+%d+%d" % (w, h, x, y))
        vars.popups["printer"].focus()
        vars.popups["printer"].after(201, lambda: vars.popups["printer"].iconbitmap("assets\\logo.ico"))
        vars.popups["printer"].title(titlebar)
        vars.popups["printer"].resizable(False, False)
        vars.popups["printer"].after(100, lambda: vars.popups["printer"].focus())

        vars.form["frame_printer"] = ctk.CTkFrame(vars.popups["printer"], width=w - 20, height=h - 20)
        vars.form["frame_printer"].place(x=10, y=10)
        vars.form["select_device_label"] = ctk.CTkLabel(vars.popups["printer"], text="Select Device", bg_color="#212121", fg_color="#212121")
        vars.form["select_device_label"].place(x=110, y=30)
        vars.form["printer_dropdown"] = ctk.CTkComboBox(vars.popups["printer"], values=printer_list, border_width=0, corner_radius=4, fg_color="#313131", variable=to_printer)
        vars.form["printer_dropdown"].place(x=80, y=65)

        vars.form["print_on_device_btn"] = ctk.CTkButton(
            vars.popups["printer"],
            text="",
            corner_radius=4,
            command=lambda: send_to_device(to_printer, to_pdf, is_code_of_conduct),
            width=60,
            height=40,
            image=(
                vars.icons["printConduct"]
                if is_code_of_conduct
                else vars.icons["printRetainer"]
            ),
            border_width=0,
            fg_color=("#1A8405" if is_code_of_conduct else "#e07b00"),
        )

        vars.form["print_on_device_btn"].place(x=80, y=110)

        vars.form["test_print_btn"] = ctk.CTkButton(
            vars.popups["printer"],
            text="",
            image=vars.icons["testPrnt"],
            border_width=1,
            corner_radius=4,
            fg_color="#1F1E1E",
            command=lambda: print_test(to_printer),
            width=60,
            height=40,
        )

        vars.form["test_print_btn"].place(x=160, y=110)

    else:
        vars.popups["printer"].focus()


## BUTTON: print the retainer or code of conduct
def print_test(to_printer):
    vars.form["status"].set("printing test")

    # defining the file path
    file_path = os.getcwd() + "\\assets\\test.docx"

    # delete any file called test.docx in case it already exists and has contents
    if os.path.exists(file_path):
        os.remove(file_path)

    # create a new document with nothing in it
    document = Document()
    document.save(file_path)

    # print the blank document
    win32print.SetDefaultPrinter(to_printer.get())
    win32api.ShellExecute(0, "print", file_path, None, ".", 0)

    # add a delay so that the print command has time to find the file, then remove the document
    time.sleep(2)
    if os.path.exists(file_path):
        os.remove(file_path)


## BUTTON: display the popup containing the history
def history_window():
    if (vars.popups['history'] is None or not vars.popups['history'].winfo_exists()): 
        vars.popups['history'] = ctk.CTkToplevel()

        w = 1200
        h = 800
        x = (vars.screen_sizes['ws']/2) - (w/2)
        y = (vars.screen_sizes['hs']/2) - (h/2) + 40
        column_x_padding = ((w-(w*0.05))/7)*0.2


        scr_frame = ctk.CTkScrollableFrame(vars.popups['history'], width=w-(w*0.05), height=h-(h*0.1))
        scr_frame.place(x=20, y=60)

        header_frame = ctk.CTkFrame(vars.popups['history'], width=w-(w*0.05), height=35, fg_color='#1F1E1E')
        header_frame.place(x=20, y=20)

        ctk.CTkLabel(header_frame, text='created_by').grid(row=0, column=0, padx=column_x_padding, pady=5)
        ctk.CTkLabel(header_frame, text='created_date').grid(row=0, column=1, padx=column_x_padding, pady=5)
        ctk.CTkLabel(header_frame, text='client_name').grid(row=0, column=2, padx=column_x_padding, pady=5)
        ctk.CTkLabel(header_frame, text='application_type').grid(row=0, column=3, padx=column_x_padding, pady=5)
        ctk.CTkLabel(header_frame, text='application_fee').grid(row=0, column=4, padx=column_x_padding, pady=5)
        ctk.CTkLabel(header_frame, text='is_active').grid(row=0, column=5, padx=column_x_padding, pady=5)

        # render rows for each hisotry entry
        history_entries = history.retrieve()

        for i, entry in enumerate(history_entries):

            # only render columns if the line in the csv is not blank
            if (entry['created_by'] != '' and entry['created_date'] != ''):
                for j, info in enumerate(['created_by', 'created_date', 'client_name', 'application_type', 'application_fee', 'is_active']):
                    ctk.CTkLabel(scr_frame, text=entry[info]).grid(row=i, column=j, padx=column_x_padding, pady=5)

                # add the import button
                ctk.CTkButton(scr_frame, text='import', width=40, corner_radius=4, command=import_entry).grid(row=i, column=j+1, padx=column_x_padding, pady=5)

                # add the active toggle
                b_label = ('active' if entry['is_active'].lower() == 'false' else 'inactive')
                b_color = ('#1A8405' if entry['is_active'].lower() == 'false' else '#313131')
                ctk.CTkButton(scr_frame, text=('set ' + b_label), fg_color=b_color, width=40, corner_radius=4).grid(row=i, column=j+2, padx=column_x_padding, pady=5)

        vars.popups['history'].geometry('%dx%d+%d+%d' % (w, h, x, y))
        vars.popups['history'].resizable(False, False)
        vars.popups['history'].after(201, lambda: vars.popups['history'].iconbitmap("assets\\logo.ico"))
        vars.popups['history'].title("Retainer History")
        vars.popups['history'].after(1, lambda: vars.popups['history'].focus())

    else:
        vars.popups['history'].focus()


def import_entry():
    pass