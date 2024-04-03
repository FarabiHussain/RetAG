import os
import datetime
import sys
import win32api
import win32print
import logic_history as history
from docx import Document
from CTkMessagebox import CTkMessagebox as popup
from path_manager import resource_path
from docx2pdf import convert


## initializes the fill info, output and input files
def init(form, isTaxIncluded, is_code_of_conduct):
    date_on_document = datetime.datetime.strptime(form['document_date'], '%d/%m/%Y')
    retainer_filename = 'retainer_one.docx'

    # data needed in both retainers and conducts
    input_data = {
        '[DAY]': date_on_document.strftime("%d"),
        '[MONTH]': date_on_document.strftime("%m"),
        '[YEAR]': date_on_document.strftime("%Y"),
        '[CLIENT1]': form["client_name_1"],
        '[APP_TYPE]': form["application_type"],
    }

    # include client 2 if the name is filled
    if len(form["client_name_2"]) > 0:
        input_data['[CLIENT2]'] = form["client_name_2"]
        retainer_filename = 'retainer_two.docx'

    # set the input and output files as Code of Conduct by default
    input_file = resource_path("assets\\templates\\conduct.docx")
    output_file = "Code of Conduct - " + (form["client_name_1"]) + ".docx"

    # include the following if the document is a retainer agreement
    if not is_code_of_conduct:
        input_data['[DAY]'] = format_day(date_on_document.strftime("%d"))
        input_data['[MONTH]'] = date_on_document.strftime("%B")
        input_data['[PAY_PLAN]'] = format_payments(form['payment_list'], isTaxIncluded)
        input_data['[APP_FEE]'] = format_cents(form["application_fee"])
        input_data['[TAXED]'] = add_taxes(form["application_fee"])
        input_data['[EMAIL1]'] = form["email_address_1"]
        input_data['[PHONE1]'] = format_phone(form["phone_number_1"])

        # include second client's email and phone if it is filled
        if len(form["email_address_2"]) > 0:
            input_data['[EMAIL2]'] = form["email_address_2"]
        elif (len(form["client_name_2"]) > 0):
            input_data['[EMAIL2]'] = form["email_address_1"]

        if len(form["phone_number_2"]) > 0:
            input_data['[PHONE2]'] = format_phone(form["phone_number_2"])
        elif (len(form["client_name_2"]) > 0):
            input_data['[PHONE2]'] = format_phone(form["phone_number_1"])

        # redefine the input file and output filename for Retainer
        input_file = resource_path("assets\\templates\\" + retainer_filename)
        output_file = f"Retainer - {form["client_name_1"]} - {form["application_type"]}.docx"

    return {
        'input_data': input_data, 
        'input_file': input_file, 
        'output_file': output_file
    }


## generate the docx with the input info
def process(form, isTaxIncluded, isOpenOutputActive, to_printer, to_pdf, is_code_of_conduct):

    init_data = None
    doc = None

    # initiate the data and document
    try:
        init_data = init(form, isTaxIncluded, is_code_of_conduct)
        doc = Document(init_data['input_file'])
    except Exception as e:
        popup(title="", message='Exception in init(): ' + str(e), corner_radius=4)
        return False

    # edit the document 
    try:
        for paragraph in doc.paragraphs:
            for key, value in init_data['input_data'].items():
                if key in paragraph.text:
                    for run in paragraph.runs:
                        run.text = run.text.replace(key, value)
    except Exception as e:
        popup(title="", message='Exception while editing document: ' + str(e), corner_radius=4)
        return False

    # add the new retainer to the history csv
    try:
        history.insert(form, isTaxIncluded, to_pdf)
    except Exception as e:
        popup(title="", message='Exception while writing to history: ' + str(e), corner_radius=4)
        return False

    # set up folders and save files, print if needed
    try:
        # set up the output directory
        output_dir = os.getcwd() + "\\output\\"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # save the file to the output folder
        doc.save(output_dir + init_data['output_file'])

        if to_pdf:
            sys.stderr = open(os.devnull, "w")
            convert(output_dir + init_data['output_file'])
            os.remove(output_dir + init_data['output_file'])
            init_data['output_file'] = init_data['output_file'].replace(".docx", ".pdf")

        if to_printer or is_code_of_conduct:
            win32print.SetDefaultPrinter(to_printer)
            win32api.ShellExecute(0, "print", output_dir + init_data['output_file'], None,  ".",  0)

        # open the word file
        if isOpenOutputActive:
            os.startfile(output_dir + init_data['output_file'])

        # return the filename
        return init_data['output_file']
    except Exception as e:
        print('Exception: ' + str(e))
        popup(title="", message='Exception: ' + str(e), corner_radius=4)
        return False


## formats the list of data so that it can be displayed on the output document
def format_payments(payments, isTaxIncluded):
    payments_string = "Payment of CAN $[TAXED] to be paid in " + format_date(payments[0]['date']) + ", after signing the retainer, is non-refundable."

    if (isTaxIncluded == False):
        payments_string.replace('[TAXED]', '[APP_FEE]')

    if (len(payments) > 1):
        payments_string = ""

        for i in range(len(payments)):
            current_payment = payments[i]
            current_amount_taxed = float(current_payment['amount'])

            if (isTaxIncluded):
                current_amount_taxed = add_taxes(current_amount_taxed)

            current_payment_date = format_date(current_payment['date'])
            payments_string += "Payment of CAN $" + str(current_amount_taxed) + " to be made within " + current_payment_date + "."

            if (i < len(payments) - 1):
                payments_string += "\n"

    return payments_string


## format date to `{date + suffix} {full month name} {year}`
def format_date(date_string):
    if date_string == 'advance':
        return date_string

    temp = datetime.datetime.strptime(date_string, '%d/%m/%Y')
    return str(format_day(temp.strftime("%d")) + " " + temp.strftime("%B") + " " + temp.strftime("%Y"))


## add suffix 'th'/'st'/'rd' to days
def format_day(day):
    day = int(day)
    suffix = ""

    if (4 <= day <= 20 or 24 <= day <= 30):
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    return str(day) + suffix


## calculate GST and PST, add it to the fee
def add_taxes(application_fee):
    application_fee = float(application_fee)
    with_taxes = (application_fee) + (application_fee * 12/100)

    return format_cents(with_taxes)


## format phone number to add brackets and hyphens when applicable
def format_phone(number):
    if (len(number) == 10):  
        area = number[0] + number[1] + number[2]
        prefix = number[3] + number[4] + number[5]
        line = number[6] + number[7] + number[8] + number[9]
        return "(" + area + ")" + " " + prefix + "-" + line

    return number


## format fees to 2 decimal places
def format_cents(amount):
    amount = float(amount)
    return str('{:.2f}'.format(amount))
