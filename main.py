from subprocess import check_call
import win32print
import variables as vars
import customtkinter as ctk
import logic_click as click
import logic_form as logic
import variables as vars
from tkinter import BooleanVar, StringVar
from path_manager import resource_path


## initialize the form components
def init_form():

    # populate the list of printers
    printer_list = [printer[2] for printer in win32print.EnumPrinters(2)]

    # calculate x and y coordinates for the Tk root window
    w = 800
    h = 540
    x = (vars.screen_sizes['ws']/2) - (w/2)
    y = (vars.screen_sizes['hs']/2) - (h/2)

    vars.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    try:
        vars.root.iconbitmap(resource_path("assets\\icons\\logo.ico"))
    except Exception as e:
        pass

    vars.root.title("AMCAIM RetAG (" + vars.form['version'] + ")")

    # string, boolean variables and tracers
    vars.form['autofill_amount'] = StringVar()
    vars.form['autofill_date'] = StringVar()
    vars.form['autofill_amount'].trace_add('write', logic.autofill_amount)
    vars.form['autofill_date'].trace_add('write', logic.autofill_date)
    vars.form['include_taxes'] = BooleanVar(value=True)
    vars.form['open_output'] = BooleanVar(value=True)
    vars.form['is_active'] = BooleanVar(value=False)

    # frame containing the client information
    vars.form['frame_info'] = ctk.CTkTabview(vars.root, width=300, height=240)
    vars.form['frame_info'].add("Client 1")
    vars.form['frame_info'].set("Client 1")
    vars.form['frame_info'].add("Client 2")

    # labels and fields for both clients
    for i in range(2):
        client_no = str(i+1)
        vars.form['client_name_' + client_no + '_label'] = ctk.CTkLabel(vars.form['frame_info'].tab("Client " + client_no), text="Client " + client_no + " name")
        vars.form['email_address_' + client_no + '_label'] = ctk.CTkLabel(vars.form['frame_info'].tab("Client " + client_no), text="Email address")
        vars.form['phone_number_' + client_no + '_label'] = ctk.CTkLabel(vars.form['frame_info'].tab("Client " + client_no), text="Phone number")
        vars.form['client_name_' + client_no + '_entry'] = ctk.CTkEntry(vars.form['frame_info'].tab("Client " + client_no), width=270, border_width=0, corner_radius=4)
        vars.form['email_address_' + client_no + '_entry'] = ctk.CTkEntry(vars.form['frame_info'].tab("Client " + client_no), width=270, border_width=0, corner_radius=4)
        vars.form['phone_number_' + client_no + '_entry'] = ctk.CTkEntry(vars.form['frame_info'].tab("Client " + client_no), width=270, border_width=0, corner_radius=4)

    # common fields and labels
    vars.form['frame_application'] = ctk.CTkFrame(vars.root, width=300, height=200)
    vars.form['application_type_label'] = ctk.CTkLabel(vars.form['frame_application'], text="Application type")
    vars.form['application_fee_label'] = ctk.CTkLabel(vars.form['frame_application'], text="Application fee")
    vars.form['document_date_label'] = ctk.CTkLabel(vars.form['frame_application'], text="Date on document (DD/MM/YYYY)")
    vars.form['application_type_entry'] = ctk.CTkEntry(vars.form['frame_application'], width=280, border_width=0, corner_radius=4)
    vars.form['application_fee_entry'] = ctk.CTkEntry(vars.form['frame_application'], width=280, border_width=0, corner_radius=4, textvariable=vars.form['autofill_amount'])
    vars.form['document_date_entry'] = ctk.CTkEntry(vars.form['frame_application'], width=280, border_width=0, corner_radius=4, placeholder_text='DD/MM/YYYY', textvariable=vars.form['autofill_date'])

    # frame containing the payment plan
    vars.form['frame_payments'] = ctk.CTkFrame(vars.root, width=300, height=440)
    vars.form['payment_instructions_label'] = ctk.CTkLabel(vars.root, text="Payment Instructions")
    vars.form['amount_label'] = ctk.CTkLabel(vars.form['frame_payments'], text="Amount")
    vars.form['date_label'] = ctk.CTkLabel(vars.form['frame_payments'], text="Date (DD/MM/YYYY)")
    vars.form['payment_list'] = []

    for _ in range(12):
        vars.form['payment_list'].append({
            'amount': ctk.CTkEntry(vars.form['frame_payments'], width=90, border_width=0, corner_radius=4),
            'date': ctk.CTkEntry(vars.form['frame_payments'], width=150, border_width=0, corner_radius=4)
        })

    # frame that displays the current status of the app
    vars.form['frame_status'] = ctk.CTkFrame(vars.root, width=620, height=30)
    vars.form['status_label'] = ctk.CTkLabel(vars.form['frame_status'], textvariable=vars.form['status'])

    ## buttons
    vars.form['today_btn'] = ctk.CTkButton(vars.root, text="today", border_width=0, corner_radius=4, bg_color='#212121', command=click.today(), width=60, height=25)
    vars.form['500_btn'] = ctk.CTkButton(vars.root, text="$500", border_width=0, corner_radius=4, bg_color='#212121', command=lambda:click.dollars(500), width=60, height=25)
    vars.form['1000_btn'] = ctk.CTkButton(vars.root, text="$1000", border_width=0, corner_radius=4, bg_color='#212121', command=lambda:click.dollars(1000), width=60, height=25)
    vars.form['plus_month_btn'] = ctk.CTkButton(vars.root, text="+1 month", border_width=0, corner_radius=4, bg_color='#343638', command=lambda:click.add_month(), width=60, height=25)
    vars.form['advance_btn'] = ctk.CTkButton(vars.root, text="advance", border_width=0, corner_radius=4, bg_color='#343638', command=lambda:click.advance(), width=60, height=25)
    vars.form['test_data_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['testData'], border_width=1, corner_radius=4, fg_color='#1F1E1E', command=lambda:click.test_data(), width=120, height=36)
    vars.form['send_to_auth_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['payauth'], border_width=0, corner_radius=4, fg_color='#7f48ba', command=lambda:click.open_payAuth(), width=120, height=36)
    vars.form['clear_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['clear'], border_width=0, corner_radius=4, fg_color='#313131', command=lambda:click.reset(), width=36, height=36)
    vars.form['output_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['folder'], border_width=0, corner_radius=4, fg_color='#313131', command=lambda:click.output(), width=36, height=36)
    vars.form['print_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['print'], border_width=0, corner_radius=4, fg_color="#e07b00", text_color="black", command=lambda:click.print_file(printer_list, False, False), width=36, height=36)
    vars.form['docx_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['docx'], border_width=0, corner_radius=4, fg_color="#383FBC", command=lambda:click.docx(), width=36, height=36)
    vars.form['pdf_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['pdf'], border_width=0, corner_radius=4, fg_color="#b02525", command=lambda:click.pdf(), width=36, height=36)
    vars.form['conduct_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['conduct'], border_width=0, corner_radius=4, fg_color="#1A8405", command=lambda:click.code_of_conduct_docx(), width=120, height=36)
    vars.form['history_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['history'], border_width=0, corner_radius=4, fg_color='#313131', command=lambda:click.history_window(), width=36, height=36)

    ## switches
    vars.form['tax_switch'] = ctk.CTkSwitch(vars.root, text="Add Taxes", border_width=0, corner_radius=4, onvalue=True, offvalue=False, variable=vars.form['include_taxes'])
    vars.form['open_output_switch'] = ctk.CTkSwitch(vars.root, text="Open Output", border_width=0, corner_radius=4, onvalue=True, offvalue=False, variable=vars.form['open_output'])


## render the form components
def render_form():
    x_offset = 10
    y_offset = 0

    vars.form['frame_info'].place(x=20, y=22)
    vars.form['frame_application'].place(x=20, y=280)
    vars.form['frame_payments'].place(x=340, y=40)
    vars.form['payment_instructions_label'].place(x=430, y=10)
    vars.form['amount_label'].place(x=40, y=0)
    vars.form['date_label'].place(x=140, y=0)

    y_offset = 15
    for i in range(len(vars.form['payment_list'])):
        curr_payment = vars.form['payment_list'][i]
        curr_payment['serial'] = ctk.CTkLabel(vars.form['frame_payments'], text=(str(i + 1) + "."))
        curr_payment['serial'].place(x=x_offset + 5, y=y_offset + 11)
        curr_payment['amount'].place(x=x_offset + 30, y=y_offset + 10)
        curr_payment['date'].place(x=x_offset + 130, y=y_offset + 10)
        y_offset += 34

    # render the application info section
    vars.form['today_btn'].place(x=250, y=288)
    vars.form['document_date_label'].place(x=10, y=10)
    vars.form['application_type_label'].place(x=10, y=70)
    vars.form['application_fee_label'].place(x=10, y=130)
    vars.form['document_date_entry'].place(x=10, y=35)
    vars.form['application_type_entry'].place(x=10, y=95)
    vars.form['application_fee_entry'].place(x=10, y=155)

    # buttons for gui text
    vars.form['advance_btn'].place(x=568, y=67)
    vars.form['500_btn'].place(x=180, y=408)
    vars.form['1000_btn'].place(x=250, y=408)

    # render the client 1 & 2 info section
    for i in range(2):
        vars.form['client_name_' + str(i+1) + '_label'].place(x=10, y=0)
        vars.form['email_address_' + str(i+1) + '_label'].place(x=10, y=60)
        vars.form['phone_number_' + str(i+1) + '_label'].place(x=10, y=120)
        vars.form['client_name_' + str(i+1) + '_entry'].place(x=10, y=25)
        vars.form['email_address_' + str(i+1) + '_entry'].place(x=10, y=85)
        vars.form['phone_number_' + str(i+1) + '_entry'].place(x=10, y=145)

    # buttons on the rightmost side of the GUI
    y_offset = 40
    vars.form['tax_switch'].place(x=660, y=y_offset)
    y_offset += 40
    vars.form['open_output_switch'].place(x=660, y=y_offset)
    # y_offset += 40
    # vars.form['active_switch'].place(x=660, y=y_offset)
    y_offset += 40

    # buffer
    buffer = 316

    y_offset += (buffer - y_offset)
    vars.form['test_data_btn'].place(x=660, y=y_offset)
    # y_offset += 42
    y_offset += 42
    vars.form['history_btn'].place(x=660, y=y_offset)
    vars.form['output_btn'].place(x=702, y=y_offset)
    vars.form['clear_btn'].place(x=744, y=y_offset)
    y_offset += 42
    vars.form['print_btn'].place(x=660, y=y_offset)
    vars.form['docx_btn'].place(x=702, y=y_offset)
    vars.form['pdf_btn'].place(x=744, y=y_offset)
    y_offset += 42
    vars.form['send_to_auth_btn'].place(x=660, y=y_offset)
    y_offset += 42
    vars.form['conduct_btn'].place(x=660, y=y_offset)

    # frame
    vars.form['frame_status'].place(x=20, y=490)
    vars.form['status_label'].place(x=10, y=1)

    vars.root.mainloop()


vars.init()
init_form()
render_form()
