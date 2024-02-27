import os, csv, datetime


## 
def insert(form, isTaxIncluded, isRetainerActive, to_pdf):

    # set up the log directory
    logs_dir = os.getcwd() + "\\logs\\"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    try: 
        f = open(logs_dir + "\\history.csv", "x")
        columns = ['created_by', 'created_date', 'date_on_document', 'client_name', 'application_type', 'application_fee', 'email', 'phone', 'add_taxes']

        for i in range(12):
            columns.append("amount_" + str(i+1))
            columns.append("date_" + str(i+1))

        columns.append("file_format")
        f.write(",".join(columns))
        f.close()

    except Exception as e:
        print(e)

    # things to enter into the new entry
    history_entry = [os.environ['COMPUTERNAME']]
    history_entry.append(str(datetime.datetime.now().strftime("%Y-%b-%d %I:%M %p")))
    history_entry.append(str(form['document_date']))
    history_entry.append(str(form['client_name']))
    history_entry.append(str(form['application_type']))
    history_entry.append(str(form['application_fee']))
    history_entry.append(str(form['email_address']))
    history_entry.append(str(form['phone_number']))
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

    with open(logs_dir + "\\history.csv", "a") as history:
        history_entry = (',').join(history_entry)
        print(history_entry)
        history.write("\n" + history_entry)


#
def retrieve():
    logs_dir = os.getcwd() + "\\logs\\"

    if not os.path.exists(logs_dir):
        print("path does not exist")
        return None
    elif not os.path.exists(logs_dir + "\\history.csv"):
        print("file does not exist")
        return None
    else:
        with open(logs_dir + "\\history.csv", mode='r') as infile:
            return list(csv.DictReader(infile))