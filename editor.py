from docx import Document
from CTkMessagebox import CTkMessagebox as popup
from path_manager import resource_path
from docx2pdf import convert
import datetime, os, sys, win32api, win32print


## generate the docx with the input info
def process(form, include_taxes, toPrinter, toPdf):
    try:
        init_data = init(form, include_taxes)
        doc = Document(init_data['input_file'])

        for paragraph in doc.paragraphs:
            for key, value in init_data['input_data'].items():
                if key in paragraph.text:
                    for run in paragraph.runs:
                        run.text = run.text.replace(key, value)

        output_dir = os.getcwd() + "\\output\\"

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # save the file to the output folder
        doc.save(output_dir + init_data['output_file'])

        if toPdf:
            sys.stderr = open(os.devnull, "w")
            convert(output_dir + init_data['output_file'])
            os.remove(output_dir + init_data['output_file'])
            init_data['output_file'] = init_data['output_file'].replace(".docx", ".pdf")

        if toPrinter:
            win32print.SetDefaultPrinter(toPrinter)
            win32api.ShellExecute(0, "print", init_data['output_file'], None,  ".",  0)

        # open the word file
        os.startfile(output_dir + init_data['output_file'])

        # return the filename
        return init_data['output_file']

    except Exception as e:
        print(e)
        popup(title="Failed", message=e, corner_radius=4)
        return False


## initializes the fill info, output and input files
def init(form, include_taxes):
    today = datetime.datetime.now()
    payment_plan = format_payments(form['payment_list'], include_taxes)

    input_data = {
        '[PAY_PLAN]': payment_plan,
        '[DAY]': format_day(today.strftime("%d")),
        '[MONTH]': today.strftime("%B"),
        '[YEAR]': today.strftime("%Y"),
        '[CLIENT]': form["client"],
        '[APP_TYPE]': form["application_type"],
        '[APP_FEE]': format_cents(form["application_fee"]),
        '[TAXED]': add_taxes(form["application_fee"]),
        '[EMAIL]': form["email_address"],
        '[PHONE]': format_phone(form["phone_number"])
    }

    input_file = resource_path("assets\\template.docx")
    output_file = "Retainer Agreement - " + (form["client"])
    output_file += ".docx"

    return {
        'input_data': input_data, 
        'input_file': input_file, 
        'output_file': output_file
    }


## formats the list of data so that it can be displayed on the output document
def format_payments(payments, include_taxes):
    payments_string = "Payment of CAN $[TAXED] to be paid in " + format_date(payments[0]['date']) + ", after signing the retainer, is non-refundable."

    if (len(payments) > 1):
        payments_string = ""

        for i in range(len(payments)):
            current_payment = payments[i]
            current_amount_taxed = float(current_payment['amount'])

            if (include_taxes):
                current_amount_taxed += float(current_payment['amount']) * 0.12

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
    amount = str('{:.2f}'.format(amount))

    return amount
