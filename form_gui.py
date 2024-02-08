from tkinter import BooleanVar, StringVar
from path_manager import resource_path
import form_logic, customtkinter as ctk, datetime as dt, win32print, os, win32api, win32print
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

form = {}
root = ctk.CTk()
root.resizable(False, False)
status_string = StringVar(value="Ready")
printer_selected = StringVar(value=win32print.GetDefaultPrinter())
printer_list = []

##
def handle_click_docx():
    global status_string
    status_string.set('writing docx')

    toPrinter = False
    handle_generate(toPrinter)


##
def handle_click_print():
    global status_string

    status_string.set('printing on device: ' + printer_selected.get())
    handle_generate(printer_selected.get())


##
def handle_click_output_folder():
    output_dir = (os.getcwd() + "\\output")
    os.startfile(output_dir)


##
def handle_generate(toPrinter):

    temp_list = []
    global form, status_string

    for i in range(len(form['payment_list'])):
        if len(form['payment_list'][i]['amount'].get()) > 0 and len(form['payment_list'][i]['date'].get()) > 0:
            temp_list.append({
                'amount': form['payment_list'][i]['amount'].get(),
                'date': form['payment_list'][i]['date'].get()
            })

    fill_info = {
        "client": form['client_name'].get(),
        "application_type": form['application_type'].get(),
        "application_fee": form['application_fee'].get(),
        "email_address": form['email_address'].get(),
        "phone_number": form['phone_number'].get(),
        "payment_list": temp_list,
    }

    response = form_logic.generate(fill_info, form['include_taxes'].get(), toPrinter)

    if toPrinter == False:
        if response == False:
            status_string.set("Error")
        else:
            status_string.set("Agreement created")


##
def handle_click_reset():
    global form, status_string
    status_string.set("form cleared")
    form = form_logic.reset(form)


##
def handle_click_today():
    global form
    form['document_date'].delete(0, "end")
    form['document_date'].insert(0, dt.datetime.now().strftime("%d/%m/%Y"))


##
def handle_click_test_print():
    global form, status_string, printer_selected
    status_string.set("printing test")

    win32print.SetDefaultPrinter(printer_selected.get())
    win32api.ShellExecute(0, "print", os.getcwd() + '\\assets\\test.docx', None,  ".",  0)


##
def handle_click_test_data():
    global form, status_string
    status_string.set("dummy data placed")

    form['document_date'].delete(0, 'end')
    form['client_name'].delete(0, 'end')
    form['application_type'].delete(0, 'end')
    form['application_fee'].delete(0, 'end')
    form['email_address'].delete(0, 'end')
    form['phone_number'].delete(0, 'end')

    form['payment_list'][0]['date'].delete(0, 'end')
    form['payment_list'][1]['amount'].delete(0, 'end')
    form['payment_list'][1]['date'].delete(0, 'end')

    form['document_date'].insert(0, '15/2/2024')
    form['client_name'].insert(0, 'John Doe')
    form['application_type'].insert(0, 'Application')
    form['application_fee'].insert(0, '100')
    form['email_address'].insert(0, 'email@dummy.com')
    form['phone_number'].insert(0, '0123456789')

    form['payment_list'][0]['date'].insert(0, '15/2/2024')
    form['payment_list'][1]['amount'].insert(0, '100')
    form['payment_list'][1]['date'].insert(0, '15/3/2024')


##
def autofill_first_amount(var, index, mode):
    global form
    amount_input = form['autofill_amount'].get()
    (form['payment_list'][0]['amount']).delete(0, 'end')
    (form['payment_list'][0]['amount']).insert(0, amount_input)


##
def autofill_first_date(var, index, mode):
    global form

    doc_date = form['document_date'].get()

    for i in range(len(doc_date)):
        if (doc_date[i].isdigit() or doc_date[i] == '/'):
            pass
        else:
            form['document_date'].delete(0, 'end')
            form['document_date'].insert(0, doc_date[0:-1])
            (form['payment_list'][0]['date']).delete(0, 'end')
            (form['payment_list'][0]['date']).insert(0, doc_date)


##
def render_form():
    global form

    x_offset = 10
    y_offset = 0

    form['frame_info'].place(x=20, y=40)
    form['client_info_label'].place(x=120, y=10)

    labels = ['document_date_label', 'client_name_label', 'application_type_label', 'application_fee_label', 'email_address_label', 'phone_number_label']
    entries = ['document_date', 'client_name', 'application_type', 'application_fee', 'email_address', 'phone_number']

    for i in range(len(labels)):
        form[labels[i]].place(x=x_offset, y=y_offset + 10)
        form[entries[i]].place(x=x_offset, y=y_offset + 40)
        y_offset += 70

    form['frame_payments'].place(x=340, y=40)
    form['payment_instructions_label'].place(x=430, y=10)
    form['amount_label'].place(x=40, y=0)
    form['date_label'].place(x=140, y=0)

    y_offset = 15
    for i in range(len(form['payment_list'])):
        curr_payment = form['payment_list'][i]
        curr_payment['serial'] = ctk.CTkLabel(form['frame_payments'], text=(str(i + 1) + "."))

        curr_payment['serial'].place(x=x_offset + 5, y=y_offset + 11)
        curr_payment['amount'].place(x=x_offset + 30, y=y_offset + 10)
        curr_payment['date'].place(x=x_offset + 130, y=y_offset + 10)
        y_offset += 34


    form['today_btn'].place(x=250, y=50)
    y_offset = 40
    form['tax_switch'].place(x=660, y=y_offset)
    y_offset += 210
    form['test_print_btn'].place(x=660, y=y_offset)
    y_offset += 40
    form['test_data_btn'].place(x=660, y=y_offset)
    y_offset += 40
    form['output_btn'].place(x=660, y=y_offset)
    y_offset += 40
    form['clear_btn'].place(x=660, y=y_offset)
    y_offset += 40
    form['printer_dropdown'].place(x=660, y=y_offset)
    y_offset += 40
    form['print_btn'].place(x=660, y=y_offset)
    y_offset += 40
    form['docx_btn'].place(x=660, y=y_offset)

    form['frame_status'].place(x=20, y=490)
    form['status_label'].place(x=10, y=1)


##
def init_form():
    global root, printer_list, form

    printer_list = [printer[2] for printer in win32print.EnumPrinters(2) if 'PDF' not in printer[2]]

    root.geometry("800x540")
    root.iconbitmap(resource_path("assets\\logo.ico"))
    root.title("AMCAIM Retainer Agreement Generator")

    form['autofill_amount'] = StringVar()
    form['autofill_amount'].trace_add('write', autofill_first_amount)
    form['autofill_date'] = StringVar()
    form['autofill_date'].trace_add('write', autofill_first_date)
    form['include_taxes'] = BooleanVar(value=True)

    ## left frame
    form['frame_info'] = ctk.CTkFrame(master=root, width=300, height=440)
    current_frame = form['frame_info']

    form['client_info_label'] = ctk.CTkLabel(root, text="Client Information")
    form['document_date_label'] = ctk.CTkLabel(current_frame, text="Date on Document (DD/MM/YYYY)")
    form['client_name_label'] = ctk.CTkLabel(current_frame, text="Client name")
    form['application_type_label'] = ctk.CTkLabel(current_frame, text="Application type")
    form['application_fee_label'] = ctk.CTkLabel(current_frame, text="Application Fee")
    form['email_address_label'] = ctk.CTkLabel(current_frame, text="Email address")
    form['phone_number_label'] = ctk.CTkLabel(current_frame, text="Phone number")

    form['document_date'] = ctk.CTkEntry(current_frame, width=280, border_width=0, corner_radius=4, placeholder_text='DD/MM/YYYY', textvariable=form['autofill_date'])
    form['client_name'] = ctk.CTkEntry(current_frame, width=280, border_width=0, corner_radius=4)
    form['application_type'] = ctk.CTkEntry(current_frame, width=280, border_width=0, corner_radius=4)
    form['application_fee'] = ctk.CTkEntry(current_frame, width=280, border_width=0, corner_radius=4, textvariable=form['autofill_amount'])
    form['email_address'] = ctk.CTkEntry(current_frame, width=280, border_width=0, corner_radius=4)
    form['phone_number'] = ctk.CTkEntry(current_frame, width=280, border_width=0, corner_radius=4)

    ## right frame
    form['frame_payments'] = ctk.CTkFrame(master=root, width=300, height=440)
    current_frame = form['frame_payments']

    form['payment_instructions_label'] = ctk.CTkLabel(root, text="Payment Instructions")
    form['amount_label'] = ctk.CTkLabel(current_frame, text="Amount")
    form['date_label'] = ctk.CTkLabel(current_frame, text="Date (DD/MM/YYYY)")

    form['payment_list'] = []
    for _ in range(12):
        form['payment_list'].append({
            'amount': ctk.CTkEntry(current_frame, width=90, border_width=0, corner_radius=4),
            'date': ctk.CTkEntry(current_frame, width=150, border_width=0, corner_radius=4)
        })

    ## buttons
    form['tax_switch'] = ctk.CTkSwitch(master=root, text="Add Taxes", border_width=0, corner_radius=4, onvalue=True, offvalue=False, variable=form['include_taxes'])
    form['test_print_btn'] = ctk.CTkButton(master=root, text="Test Print", border_width=0, corner_radius=4, fg_color='#1F1E1E', text_color="#2A2A2A", command=handle_click_test_print, width=120)
    form['test_data_btn'] = ctk.CTkButton(master=root, text="Test Data", border_width=0, corner_radius=4, fg_color='#1F1E1E', text_color="#2A2A2A", command=handle_click_test_data, width=120)
    form['printer_dropdown'] = ctk.CTkComboBox(master=root, values=printer_list, border_width=0, corner_radius=4, fg_color='#313131', variable=printer_selected, width=120)
    form['output_btn'] = ctk.CTkButton(master=root, text="Output Folder", border_width=0, corner_radius=4, fg_color='#313131', command=handle_click_output_folder, width=120)
    form['docx_btn'] = ctk.CTkButton(master=root, text="Save DOCX", border_width=0, corner_radius=4, fg_color="#383FBC", command=handle_click_docx, width=120)
    form['clear_btn'] = ctk.CTkButton(master=root, text="Clear Form", border_width=0, corner_radius=4, fg_color='#313131', command=handle_click_reset, width=120)
    form['print_btn'] = ctk.CTkButton(master=root, text="Print", border_width=0, corner_radius=4, fg_color="#e07b00", text_color="black", command=handle_click_print, width=120)
    form['today_btn'] = ctk.CTkButton(master=root, text="today", border_width=0, corner_radius=4, fg_color="#383FBC", bg_color='transparent', command=handle_click_today, width=60, height=25)

    form['frame_status'] = ctk.CTkFrame(master=root, width=620, height=30)
    current_frame = form['frame_status']

    form['status_label'] = ctk.CTkLabel(current_frame, textvariable=status_string)

    render_form()

    root.mainloop()
