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
import json
import pandas as pd
from tkinter import StringVar
from dateutil import relativedelta as rd
from docx import Document
from CTkMessagebox import CTkMessagebox as popup


##############################################################################################################
############################################## HELPER FUNCTIONS ##############################################
##############################################################################################################


## set the status to reflect which printer is being used, and send the file to be printed
def send_to_device(selected_printer, to_pdf, is_code_of_conduct):
    vars.form["status"].set("printing on device: " + selected_printer.get())
    generate_from_form(selected_printer.get(), to_pdf, is_code_of_conduct)


## generate a dictionary from the form and send it to the doc editor
def generate_from_form(to_printer, to_pdf, is_code_of_conduct):
    pay_list = []

    for i in range(len(vars.form["payment_list"])):
        if (
            len(vars.form["payment_list"][i]["amount"].get()) > 0
            and len(vars.form["payment_list"][i]["date"].get()) > 0
        ):
            pay_list.append(
                {
                    "amount": vars.form["payment_list"][i]["amount"].get(),
                    "date": vars.form["payment_list"][i]["date"].get(),
                }
            )

    fill_info = {
        "client_name_1": vars.form["client_name_1_entry"].get(),
        "email_address_1": vars.form["email_address_1_entry"].get(),
        "phone_number_1": vars.form["phone_number_1_entry"].get(),
        "client_name_2": vars.form["client_name_2_entry"].get(),
        "email_address_2": vars.form["email_address_2_entry"].get(),
        "phone_number_2": vars.form["phone_number_2_entry"].get(),
        "payment_list": pay_list,
        "document_date": vars.form["document_date_entry"].get(),
        "application_type": vars.form["application_type_entry"].get(),
        "application_fee": vars.form["application_fee_entry"].get(),
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


## format retainers with multiple clients to show only their last names in the history window
def set_client_name(client_name):
    client_name_list = client_name.split(";")

    if len(client_name_list) == 2:
        return (client_name_list[0].split(" "))[-1] + " & " + (client_name_list[1].split(" "))[-1]

    return client_name_list[0]


## render the table using the list of dicts passed
def render_table(history_entries):
    radio_var = StringVar(value="")
    radio_btn_text = StringVar(value="")

    for i, entry in enumerate(history_entries):

        # only render columns if the line in the csv is not blank
        if (entry['created_by'] != '' and entry['created_date'] != ''):

            # add the radio button
            ctk.CTkRadioButton(
                vars.popups['elem']['scr_frame'], width=1100/5, text=set_client_name(entry['client_name']), radiobutton_height=15, radiobutton_width=15, command=lambda:select(radio_var), variable=radio_var, value=entry
            ).grid(row=i, column=0, pady=5)

            # columns with data
            for j, info in enumerate(['created_by', 'created_date', 'application_type', 'application_fee']):

                # add some formatting where needed
                label_text = entry[info]
                active_color = 'white'

                # if (info == 'is_active'):
                #     label_text = 'inactive' if entry[info].lower() == 'false' else 'active'
                #     active_color = '#b02525' if entry[info].lower() == 'false' else '#1A8405'
                if (info == 'application_fee'):
                    label_text = '$' + entry[info]

                ctk.CTkLabel(
                    vars.popups['elem']['scr_frame'], text=label_text, text_color=active_color, width=1100/5, fg_color=('transparent' if i%2==0 else '#292929')
                ).grid(row=i, column=(j+1), padx=0, pady=5)


## found it at https://stackoverflow.com/a/63862387/1497139
def singleQuoteToDoubleQuote(singleQuoted):
    cList=list(singleQuoted)
    inDouble=False
    inSingle=False

    for i,c in enumerate(cList):
        if c=="'":
            if not inDouble:
                inSingle=not inSingle
                cList[i]='"'
        elif c=='"':
            inDouble=not inDouble

    doubleQuoted="".join(cList)

    return doubleQuoted


## update the gui when a client is selected
def select(str_var):
    str_var = str_var.get()
    entry = json.loads(singleQuoteToDoubleQuote(str_var))

    # set the button states and colors based on the selected entry
    vars.popups['elem']['import_button'].configure(text="import " + set_client_name(entry['client_name']), fg_color='#383FBC', command=lambda:import_entry(entry))

    # if (entry['is_active'].lower() == 'true'):
    #     vars.popups['elem']['status_button'].configure(state='normal', text='set inactive', fg_color="#b02525", command=lambda:toggle_status(entry))
    # else:
    #     vars.popups['elem']['status_button'].configure(state='normal', text='set active', fg_color="#1A8405", command=lambda:toggle_status(entry))


##############################################################################################################
############################################### BUTTON HANDLERS ##############################################
##############################################################################################################


## add the clicked amount as the total value of the case
def dollars(amount):
    vars.form["application_fee_entry"].delete(0, "end")
    vars.form["application_fee_entry"].insert(0, int(amount))


## sets the `date on document` to be today's date
def today():
    vars.form["document_date_entry"].delete(0, "end")
    vars.form["document_date_entry"].insert(0, dt.datetime.now().strftime("%d/%m/%Y"))
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


## change the position of the `+1month` button
def reposition_plus_month(place_button):
    vars.form["plus_month_btn"].destroy()
    vars.form["plus_month_btn"] = ctk.CTkButton(vars.root, text="+1 month", border_width=0, corner_radius=4, bg_color="#343638", command=add_month, width=60, height=25)

    if place_button:
        vars.form["plus_month_btn"].place(x=568, y=vars.button_position)


## adds 1 month to the previous date in the payments list
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
            title="",
            message="Unable to add month as previous payment date is empty",
            corner_radius=4,
        )

    elif len(vars.form["payment_list"][vars.current_payment - 1]["date"].get()) < 8:
        vars.current_payment -= 1
        vars.button_position -= pixels_to_next_row
        reposition_plus_month(vars.button_position)
        add_month()


## populate the form with dummy data
def test_data():
    vars.form["status"].set("dummy data placed")
    os.system('cls')

    client_qty = random.choice([1,2])
    client_1_gender = random.choice(['male', 'female'])
    client_2_gender = 'male' if client_1_gender == 'female' else 'female'

    client_name_1 = names.get_full_name(gender=client_1_gender)
    client_name_2 = names.get_full_name(gender=client_2_gender)
    application_fee = random.randint(1, 4) * 1000

    vars.form["client_name_1_entry"].delete(0, "end")
    vars.form["email_address_1_entry"].delete(0, "end")
    vars.form["phone_number_1_entry"].delete(0, "end")
    vars.form["client_name_2_entry"].delete(0, "end")
    vars.form["email_address_2_entry"].delete(0, "end")
    vars.form["phone_number_2_entry"].delete(0, "end")
    vars.form["document_date_entry"].delete(0, "end")
    vars.form["application_fee_entry"].delete(0, "end")
    vars.form["application_type_entry"].delete(0, "end")

    vars.form["client_name_1_entry"].insert(0, client_name_1)
    vars.form["email_address_1_entry"].insert(0, client_name_1.replace(" ", "").lower() + "@email.com")
    vars.form["phone_number_1_entry"].insert(0, random.choice(["431", "204"]) + str(random.randint(1000000, 9999999)))

    if (client_qty > 1):
        vars.form["client_name_2_entry"].insert(0, client_name_2)
        vars.form["email_address_2_entry"].insert(0, client_name_2.replace(" ", "").lower() + "@email.com")
        vars.form["phone_number_2_entry"].insert(0, random.choice(["431", "204"]) + str(random.randint(1000000, 9999999)))

    vars.form["document_date_entry"].insert(0, "1/4/2024")
    vars.form["application_fee_entry"].insert(0, application_fee)
    vars.form["application_type_entry"].insert(0, random.choice(["EOI", "MPNP", "PR", "PGWP", "Citizenship"]))

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


## reset the form and variables
def reset():
    vars.form["status"].set("form cleared")
    vars.form = logic_form.reset(vars.form)
    vars.form["include_taxes"].set(True)
    vars.form["open_output"].set(True)
    vars.current_payment = 1
    vars.button_position = 101

    reposition_plus_month(False)


## sets the date to be 'paid in advance' when clients cannot provide a specific date for payment
def advance():
    vars.form["payment_list"][0]["date"].delete(0, "end")
    vars.form["payment_list"][0]["date"].insert(0, "advance")

    if vars.current_payment == 1:
        reposition_plus_month(True)


## open the output folder
def output():
    output_dir = os.getcwd() + "\\output"
    os.startfile(output_dir)


## save the retainer as docx
def docx():
    vars.form["status"].set("writing docx")

    to_printer = False
    to_pdf = False
    is_code_of_conduct = False
    generate_from_form(to_printer, to_pdf, is_code_of_conduct)


## save the retainer as pdf
def pdf():
    vars.form["status"].set("creating pdf")

    to_printer = False
    to_pdf = True
    is_code_of_conduct = False
    generate_from_form(to_printer, to_pdf, is_code_of_conduct)


## print the retainer or code of conduct
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
        vars.popups["printer"].after(201, lambda: vars.popups["printer"].iconbitmap("assets\\icons\\logo.ico"))
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


## print a blank page to test the printer
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


## display the popup containing the history
def history_window():

    vars.popups['elem']['history_entries'] = history.retrieve()

    # there must be at least one entry in the list
    if (len(vars.popups['elem']['history_entries']) > 0):

        # make sure that the popup does not already exist to avoid duplicates
        if (vars.popups['history'] is None or not vars.popups['history'].winfo_exists()): 

            vars.popups['history'] = ctk.CTkToplevel()

            w = 1200
            h = 800
            x = (vars.screen_sizes['ws']/2) - (w/2)
            y = (vars.screen_sizes['hs']/2) - (h/2)

            header_frame = ctk.CTkFrame(vars.popups['history'], width=1123, height=35, fg_color='transparent')
            header_frame.place(x=40, y=755)

            vars.popups['elem']['scr_frame'] = ctk.CTkScrollableFrame(vars.popups['history'], width=1100, height=720)
            vars.popups['elem']['scr_frame'].place(x=40, y=10)
            render_table(vars.popups['elem']['history_entries'])

            # the buttons at the bottom of the popup for operations
            vars.popups['elem']['import_button'] = ctk.CTkButton(header_frame, text='import client', width=200, corner_radius=4, fg_color="#1F1E1E")
            # vars.popups['elem']['status_button'] = ctk.CTkButton(header_frame, text='status toggle', width=100, corner_radius=4, fg_color="#1F1E1E")
            vars.popups['elem']['import_button'].place(x=400, y=2)
            # vars.popups['elem']['status_button'].place(x=605, y=2)

            ## render the popup
            vars.popups['history'].geometry('%dx%d+%d+%d' % (w, h, x, y))
            vars.popups['history'].resizable(False, False)
            vars.popups['history'].after(201, lambda: vars.popups['history'].iconbitmap("assets\\icons\\logo.ico"))
            vars.popups['history'].title("Retainer History")
            vars.popups['history'].after(1, lambda: vars.popups['history'].focus())

        else:
            vars.popups['history'].focus()

    else:
        popup(title="", message='No entries in history', corner_radius=4)


## import the entry into the form
def import_entry(entry):

    client_names = entry['client_name'].split(";")
    client_emails = entry['email'].split(";")
    client_phones = entry['phone'].split(";")

    # set the form entries
    vars.form['document_date_entry'].delete(0, 'end')
    vars.form['document_date_entry'].insert(0, entry['date_on_document'].replace("_", " "))

    vars.form['application_type_entry'].delete(0, 'end')
    vars.form['application_type_entry'].insert(0, entry['application_type'].replace("_", ", "))

    vars.form['application_fee_entry'].delete(0, 'end')
    vars.form['application_fee_entry'].insert(0, entry['application_fee'])

    vars.form['client_name_1_entry'].delete(0, 'end')
    vars.form['client_name_1_entry'].insert(0, client_names[0].replace("_", " "))

    vars.form['email_address_1_entry'].delete(0, 'end')
    vars.form['email_address_1_entry'].insert(0, client_emails[0].replace("_", " "))

    vars.form['phone_number_1_entry'].delete(0, 'end')
    vars.form['phone_number_1_entry'].insert(0, client_phones[0].replace("'", ""))

    vars.form['client_name_2_entry'].delete(0, 'end')
    vars.form['client_name_2_entry'].insert(0, '' if len(client_names) == 1 else client_names[1].replace("_", " "))

    vars.form['email_address_2_entry'].delete(0, 'end')
    vars.form['email_address_2_entry'].insert(0, '' if len(client_emails) == 1 else client_emails[1].replace("_", " "))

    vars.form['phone_number_2_entry'].delete(0, 'end')
    vars.form['phone_number_2_entry'].insert(0, '' if len(client_phones) == 1 else client_phones[1].replace("'", ""))

    vars.form['include_taxes'].set(True)
    # vars.form['is_active'].set(False)

    # set the payments
    for i in range(12):
        vars.form['payment_list'][i]['date'].delete(0, 'end')
        vars.form['payment_list'][i]['date'].insert(0, entry['date_' + str(i + 1)])
        vars.form['payment_list'][i]['amount'].delete(0, 'end')
        vars.form['payment_list'][i]['amount'].insert(0, entry['amount_' + str(i + 1)])

    # set the taxes switch
    if (entry['add_taxes'].lower() == 'true'):
        vars.form['include_taxes'].set(True)
    else:
        vars.form['include_taxes'].set(False)

    # set the active switch
    # if (entry['is_active'].lower() == 'true'):
    #     vars.form['is_active'].set(True)
    # else:
    #     vars.form['is_active'].set(False)

    # close the popup once done
    vars.popups['history'].destroy()


## switch the is_active status for the entry
def toggle_status(entry):
    history_entries = vars.popups['elem']['history_entries']
    file_location = os.getcwd() + "\\write\\history.csv"

    # iterate through the entries to find the row that needs to be overwritten
    for index, current in enumerate(history_entries):

        # once found, write to file and exit the loop
        if (entry['created_by'] == current['created_by'] and entry['created_date'] == current['created_date'] and entry['client_name'] == current['client_name']):
            df = pd.read_csv(file_location)
            df.loc[(index), 'is_active'] = (True if entry['is_active'].lower() == 'false' else False)
            df.to_csv(file_location, index=False) 
            break

    vars.popups['elem']['history_entries'] = history.retrieve()

    # reload the table to display the new change
    vars.popups['elem']['scr_frame'].destroy()
    vars.popups['elem']['scr_frame'] = ctk.CTkScrollableFrame(vars.popups['history'], width=1100, height=720)
    vars.popups['elem']['scr_frame'].place(x=40, y=10)
    render_table(vars.popups['elem']['history_entries'])

