import editor, re, win32api, win32print
from CTkMessagebox import CTkMessagebox as popup


## validates the form
def validate(fill_info):
    for key, val in fill_info.items():

        if (len(fill_info[key]) < 1):
            popup(icon="cancel", title="Error", message="All fields need to be filled", corner_radius=4)
            print("All fields need to be filled")
            return False

        if (key == "email_address") and ("@" not in fill_info[key]) and ("." not in fill_info[key]):
            popup(icon="cancel", title="Error", message="Invalid email address", corner_radius=4)
            print("Invalid email address")
            return False
        
        if (key == "payment_list"):
            for index in range(len(fill_info['payment_list'])):
                current_pay = fill_info['payment_list'][index]

                if (len(current_pay['amount']) == 0 and len(current_pay['amount']) == 0):
                    popup(icon="cancel", title="Error", message="Payment #" + str(index + 1) + " is incomplete", corner_radius=4)
                    print("Invalid amount in payment " + index)
                    return False

                if (re.search('[a-zA-Z]', current_pay['amount']) or re.search('[a-zA-Z]', current_pay['date'])):
                    popup(icon="cancel", title="Error", message="Invalid input in payment #" + str(index + 1), corner_radius=4)
                    print("Invalid amount in payment " + index)
                    return False

    return True


## runs the editor and displays message
def generate(fill_info, toPDF, toPrinter):

    if (validate(fill_info) == True):
        created_file = editor.process(fill_info, toPDF, toPrinter)

        if (toPrinter != False):
            # win32print.SetDefaultPrinter(toPrinter)
            # win32api.ShellExecute(0, "print", 'test.docx', None,  ".",  0)
            win32api.ShellExecute(0, "print", created_file, None,  ".",  0)
        
        return created_file

    return False


## reset form fields
def reset(form_elements):
    form_elements['client_name'].delete(0, "end")
    form_elements['application_type'].delete(0, "end")
    form_elements['application_fee'].delete(0, "end")
    form_elements['email_address'].delete(0, "end")
    form_elements['phone_number'].delete(0, "end")
    form_elements['document_date'].delete(0, "end")

    for i in range(len(form_elements['payment_list'])):
        form_elements['payment_list'][i]['amount'].delete(0, "end")
        form_elements['payment_list'][i]['amount'].insert("end", "")
        form_elements['payment_list'][i]['date'].delete(0, "end")
        form_elements['payment_list'][i]['date'].insert("end", "")

    # popup(icon="info", title="Success", message="Form cleared", corner_radius=4)

    return form_elements
