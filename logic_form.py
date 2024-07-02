import editor
import re
import variables as vars
from CTkMessagebox import CTkMessagebox as popup


## validates the form
def validate(fill_info):
    valid_date_regex = '^[0-3]{0,1}[0-9]{1}' + '/' + '[0-2]{0,1}[0-9]{1}' + '/' + '20[0-9]{1}[0-9]{1}$'

    for key, _ in fill_info.items():

        if (key == 'application_type'):
            for curr_char in ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]:
                if (curr_char in fill_info[key]):
                    popup(icon="cancel", title="Error", message=f"The character '{curr_char}' is not allowed\nin the application type field", corner_radius=4)
                    return False

        if (("_2" not in key) and len(fill_info[key]) < 1):
            popup(icon="cancel", title="Error", message="Payment, application, and at least Client 1 information needs to be filled", corner_radius=4)
            return False

        if (key == "email_address_1") and ("@" not in fill_info[key]) and ("." not in fill_info[key]):
            popup(icon="cancel", title="Error", message="Invalid email address in Client 1", corner_radius=4)
            return False

        if (key == "payment_list"):
            for index in range(len(fill_info['payment_list'])):
                current_pay = fill_info['payment_list'][index]

                if (len(current_pay['amount']) == 0 and len(current_pay['date']) == 0):
                    popup(icon="cancel", title="Error", message="Payment " + str(index + 1) + " contains empty field(s)", corner_radius=4)
                    return False

                if (re.match('^[0-9]*$', current_pay['amount']) == False):
                    popup(icon="cancel", title="Error", message="Invalid amount in payment #" + str(index + 1), corner_radius=4)
                    return False

                if (current_pay['date'] == "advance"):
                    if (index != 0):
                        popup(icon="cancel", title="Error", message="'advance' date only allowed on the first payments", corner_radius=4)
                        return False

                if (re.match(valid_date_regex, current_pay['date']) == None):
                    err_message = "Invalid date in payment #" + str(index + 1)

                    if ((current_pay['date'] == "advance") and (index == 0)) == False:
                        err_message = "'advance' date only allowed on the first payments" 
                    else:
                        continue

                    popup(icon="cancel", title="Error", message=err_message, corner_radius=4)
                    return False

    return True


## runs the editor and displays message
def generate(fill_info, isTaxIncluded, isOpenOutputActive, to_printer, to_pdf, is_code_of_conduct):
    if (validate(fill_info) == True):
        return editor.process(fill_info, isTaxIncluded, isOpenOutputActive, to_printer, to_pdf, is_code_of_conduct)
    else:
        print('not validated')
        return False



## reset form fields
def reset(form_elements):
    form_elements['client_name_1_entry'].delete(0, "end")
    form_elements['email_address_1_entry'].delete(0, "end")
    form_elements['phone_number_1_entry'].delete(0, "end")
    form_elements['document_date_entry'].delete(0, "end")
    form_elements['application_type_entry'].delete(0, "end")
    form_elements['application_fee_entry'].delete(0, "end")

    for i in range(len(form_elements['payment_list'])):
        form_elements['payment_list'][i]['amount'].delete(0, "end")
        form_elements['payment_list'][i]['amount'].insert("end", "")
        form_elements['payment_list'][i]['date'].delete(0, "end")
        form_elements['payment_list'][i]['date'].insert("end", "")

    return form_elements


##
def autofill_amount(var, index, mode):
    amount_input = vars.form['autofill_amount'].get()
    (vars.form['payment_list'][0]['amount']).delete(0, 'end')
    (vars.form['payment_list'][0]['amount']).insert(0, amount_input)


##
def autofill_date(var, index, mode):
    doc_date = vars.form['document_date_entry'].get()

    for i in range(len(doc_date)):
        if (doc_date[i].isdigit() or doc_date[i] == '/'):
            (vars.form['payment_list'][0]['date']).delete(0, 'end')
            (vars.form['payment_list'][0]['date']).insert(0, doc_date)
        else:
            (vars.form['document_date_entry']).delete(0, 'end')
            (vars.form['document_date_entry']).insert(0, doc_date[0:-1])
            (vars.form['payment_list'][0]['date']).delete(0, 'end')
            (vars.form['payment_list'][0]['date']).insert(0, doc_date[0:-1])

    if (len(doc_date) == 0):
        (vars.form['payment_list'][0]['date']).delete(0, 'end')


