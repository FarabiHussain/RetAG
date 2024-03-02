import os, csv, datetime


## write a newly created retainer information into the history
def insert(form, isTaxIncluded, isRetainerActive, to_pdf):

    # set up the write directory
    history_dir = os.getcwd() + "\\write\\"
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)

    try: 
        f = open(history_dir + "\\history.csv", "x")
        columns = ['created_by', 'created_date', 'date_on_document', 'client_name', 'application_type', 'application_fee', 'email', 'phone', 'add_taxes', 'is_active']

        for i in range(12):
            columns.append("amount_" + str(i+1))
            columns.append("date_" + str(i+1))

        columns.append("file_format")
        f.write(",".join(columns))
        f.close()

    except Exception as e:
        print(e)

    client_names = []
    client_emails = []
    client_phones = []

    # populate the arrays above if data was entered into the form
    for info_type in ['client_name_', 'email_address_', 'phone_number_']:
        for index in range(2):

            client_no = str(index + 1)

            if len(form[info_type + client_no]) > 0:
                if (info_type == 'client_name_'):
                    client_names.append(form[info_type + client_no])
                elif (info_type == 'email_address_'):
                    client_emails.append(form[info_type + client_no])
                elif (info_type == 'phone_number_'):
                    client_phones.append(form[info_type + client_no])

    # things to enter into the new entry
    history_entry = [os.environ['COMPUTERNAME']]
    history_entry.append(str(datetime.datetime.now().strftime("%Y-%b-%d %I:%M %p")))
    history_entry.append(str(form['document_date']))
    history_entry.append((";").join(client_names))
    history_entry.append(str(form['application_type']))
    history_entry.append(str(form['application_fee']))
    history_entry.append((";").join(client_emails))
    history_entry.append((";").join(client_phones))
    history_entry.append(str(isTaxIncluded).title())

    for i in range(12):
        if (i < len(form['payment_list'])): 
            current_payment = form['payment_list'][i]
            history_entry.append(str(float(current_payment['amount'])))
            history_entry.append(str(current_payment['date']))
        else:
            history_entry.append("")
            history_entry.append("")

    history_entry.append("PDF" if to_pdf else "DOCX")
    history_entry.append(str(isRetainerActive).title())

    with open(history_dir + "\\history.csv", "a") as history:
        history_entry = (',').join(history_entry)
        print(history_entry)
        history.write("\n" + history_entry)


## read the csv and return as a list
def retrieve():
    history_dir = os.getcwd() + "\\write\\"

    if not os.path.exists(history_dir):
        print("path does not exist")
        return None
    elif not os.path.exists(history_dir + "\\history.csv"):
        print("file does not exist")
        return None
    else:
        with open(history_dir + "\\history.csv", mode='r') as infile:
            return list(csv.DictReader(infile))