from tkinter import StringVar
import form_logic, customtkinter as ctk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

form = {}
root = ctk.CTk()

##
def handle_click_generate():

    temp_list = []

    for i in range(len(form['payment_list'])):
        if len(form['payment_list'][i]['amount'].get()) > 0 and len(form['payment_list'][i]['date'].get()) > 0:
            temp_list.append({
                'amount': form['payment_list'][i]['amount'].get(),
                'date': form['payment_list'][i]['date'].get()
            })

    print(temp_list)

    fill_info = {
        "client": form['client_name'].get(),
        "application_type": form['application_type'].get(),
        "application_fee": form['application_fee'].get(),
        "email_address": form['email_address'].get(),
        "phone_number": form['phone_number'].get(),
        "payment_list": temp_list
    }

    form_logic.generate(fill_info)


##
def handle_click_reset():
    global form
    form = form_logic.reset(form)


##
def place_form_components():
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

    y_offset = 3
    for i in range(len(form['payment_list'])):
        curr_payment = form['payment_list'][i]
        curr_payment['serial'] = ctk.CTkLabel(form['frame_payments'], text=(str(i + 1) + "."))

        curr_payment['serial'].place(x=x_offset + 5, y=y_offset + 10)
        curr_payment['amount'].place(x=x_offset + 30, y=y_offset + 10)
        curr_payment['date'].place(x=x_offset + 130, y=y_offset + 10)
        y_offset += 35

    form['clear_btn'].place(x=660, y=370)
    form['pdf_btn'].place(x=660, y=410)
    form['docx_btn'].place(x=660, y=450)


##
def autofill_first_amount(var, index, mode):
    global form
    amount_input = form['autofill_amount'].get()
    (form['payment_list'][0]['amount']).delete(0, 'end')
    (form['payment_list'][0]['amount']).insert(0, amount_input)


##
def autofill_first_date(var, index, mode):
    global form
    date_input = form['document_date'].get()
    (form['payment_list'][0]['date']).delete(0, 'end')
    (form['payment_list'][0]['date']).insert(0, date_input)


##
def autoformat_doc_date(var, index, mode):
    global form, root

    doc_date = form['document_date'].get()

    for i in range(len(doc_date)):
        if (doc_date[i].isdigit() or doc_date[i] == '/'):
            pass
        else:
            form['document_date'].delete(0, 'end')
            form['document_date'].insert(0, doc_date[0:-1])


##
def render_form():
    global root
    root.geometry("800x500")
    root.iconbitmap("./assets/logo.ico")
    root.title("AMCAIM Retainer Agreement Generator")

    global form
    form['autofill_amount'] = StringVar()
    form['autofill_amount'].trace_add('write', autofill_first_amount)
    form['autofill_date'] = StringVar()
    form['autofill_date'].trace_add('write', autofill_first_date)

    ## left frame
    form['frame_info'] = ctk.CTkFrame(master=root, width=300, height=440)
    current_frame = form['frame_info']

    form['client_info_label'] = ctk.CTkLabel(root, text="Client Information")
    form['document_date_label'] = ctk.CTkLabel(current_frame, text="Date on Document")
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

    # form['document_date'].insert(0, '7/2/2024')
    form['client_name'].insert(0, 'John Doe')
    form['application_type'].insert(0, 'Application')
    # form['application_fee'].insert(0, '100')
    form['email_address'].insert(0, 'e@mail.com')
    form['phone_number'].insert(0, '0123456789')

    ## right frame
    form['frame_payments'] = ctk.CTkFrame(master=root, width=300, height=440)
    current_frame = form['frame_payments']

    form['payment_instructions_label'] = ctk.CTkLabel(root, text="Payment Instructions")
    form['amount_label'] = ctk.CTkLabel(current_frame, text="Amount")
    form['date_label'] = ctk.CTkLabel(current_frame, text="Date")
    form['amount'] = ctk.CTkEntry(current_frame, placeholder_text="Amount", width=280, border_width=0, corner_radius=4)
    form['date'] = ctk.CTkEntry(current_frame, placeholder_text="Date", width=280, border_width=0, corner_radius=4)

    form['payment_list'] = []
    form['payment_list'].append({
        'amount': ctk.CTkEntry(current_frame, placeholder_text="$", width=90, border_width=0, corner_radius=4),
        'date': ctk.CTkEntry(current_frame, placeholder_text="DD/MM/YYYY", width=150, border_width=0, corner_radius=4)
    })

    for _ in range(11):
        form['payment_list'].append({
            'amount': ctk.CTkEntry(current_frame, placeholder_text="$", width=90, border_width=0, corner_radius=4),
            'date': ctk.CTkEntry(current_frame, placeholder_text="DD/MM/YYYY", width=150, border_width=0, corner_radius=4)
        })

    ## buttons
    form['docx_btn'] = ctk.CTkButton(master=root, text="Save DOCX", border_width=0, corner_radius=4, fg_color="#383FBC", command=handle_click_generate, width=120)
    form['pdf_btn'] = ctk.CTkButton(master=root, text="Save PDF", border_width=0, corner_radius=4, fg_color="#D02222", command=handle_click_generate, width=120)
    form['clear_btn'] = ctk.CTkButton(master=root, text="Reset Form", border_width=0, corner_radius=4, fg_color="orange", text_color="#783100", command=handle_click_reset, width=120)

    place_form_components()

    root.mainloop()













# form['payment_plan'] = ctk.CTkTextbox(form['frame_info'], width=280, height=80, border_width=0, corner_radius=4)
# form['payment_plan_label'].place(x=x_offset, y=y_offset + 10)
# form['payment_plan'].place(x=x_offset, y=y_offset + 40)
# form['payment_plan'].insert("end", "Payment of CAN $[TAXED] after signing the retainer and is non-refundable.")
# y_offset += 130