from docx import Document
import time

## generate the docx with the input info
def generate(fill_info):
    init_data = init(fill_info)
    doc = Document(init_data['input_file'])

    for paragraph in doc.paragraphs:
        print(paragraph.text)

        for key, value in init_data['input_data'].items():
            # if "4.2" in paragraph.text:
            #     paragraph.insert_paragraph_before('-----')

            if key in paragraph.text:
                for run in paragraph.runs:
                    run.text = run.text.replace(key, value)

    doc.save(init_data['output_file'])

##
def init(fill_info):
    input_data = {
        '[CLIENT]': fill_info["client"],
        '[APP_TYPE]': fill_info["application_type"],
        '[APP_FEE]': format_cents(fill_info["application_fee"]),
        '[WITH_TAXES]': add_taxes(fill_info["application_fee"]),
        '[EMAIL]': fill_info["email_address"],
        '[PHONE]': fill_info["phone_number"]
    }

    input_file = "template.docx"
    output_file = "Retainer Agreement - " + (fill_info["client"]) + " - " + fill_info["application_type"] + ".docx"

    return {
        'input_data': input_data, 
        'input_file': input_file, 
        'output_file': output_file
    }


## calculate GST and PST, add it to the fee
def add_taxes(application_fee):
    application_fee = float(application_fee)
    with_taxes = (application_fee) + (application_fee * 12/100)

    return format_cents(with_taxes)

## format fees to 2 decimal places
def format_cents(amount):
    amount = float(amount)
    amount = str('{:.2f}'.format(amount))

    return amount

