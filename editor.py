from docx import Document
import datetime, os


## generate the docx with the input info
def generate(form):

    try:
        init_data = init(form)
        doc = Document(init_data['input_file'])

        for paragraph in doc.paragraphs:
            for key, value in init_data['input_data'].items():
                if key in paragraph.text:
                    for run in paragraph.runs:
                        run.text = run.text.replace(key, value)

        doc.save(init_data['output_file'])
        os.startfile(init_data['output_file'])
        print("[" + str(datetime.datetime.now()) + "]\t" + init_data['output_file'])

        return True

    except Exception as e:
        print(e)
        return False


## initializes the fill info, output and input files
def init(form):
    today = datetime.datetime.now()
    payment_plan = format_payments(form['payment_list'])

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

    input_file = "./assets/template.docx"
    output_file = "Retainer Agreement - " + (form["client"])
    output_file += ".docx"

    return {
        'input_data': input_data, 
        'input_file': input_file, 
        'output_file': output_file
    }


##
def format_payments(payments):
    payments_string = "Payment of CAN $[TAXED] after signing the retainer and is non-refundable."

    if (len(payments) > 1):
        payment_plan = ""

        for i in range(len(payments)):
            current_payment = payments[i]
            current_amount_taxed = float(current_payment['amount']) + (float(current_payment['amount']) * 0.12)
            current_payment_date = format_date(current_payment['date'])
            payment_plan += "Payment of CAN $" + str(current_payment['amount']) + " on " + str(current_payment['date']) + ".\n"

    return payments_string


##
def format_date(date_string):
    temp = datetime.strptime(date_string, '/%d/%m/%Y')
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
