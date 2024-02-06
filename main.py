import customtkinter, editor, os

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("400x350")
root.iconbitmap("logo.ico")
root.title("AMCAIM Retainer Agreement Generator")

def generate_button():
    os.system('cls')

    editor.generate( 
        {
            'client': client_name.get(),
            'application_type': application_type.get(),
            'application_fee': application_fee.get(),
            'email_address': email_address.get(),
            'phone_number': phone_number.get(),
        }
    )

    print('success')

    # root.destroy()

frame = customtkinter.CTkFrame(master=root)
heading = customtkinter.CTkLabel(master=frame, text="Retainer Agreement Generator")
client_name = customtkinter.CTkEntry(master=frame, placeholder_text="Client name", width=300, border_width=0)
application_type = customtkinter.CTkEntry(master=frame, placeholder_text="Application type", width=300, border_width=0)
application_fee = customtkinter.CTkEntry(master=frame, placeholder_text="Application Fee", width=300, border_width=0)
email_address = customtkinter.CTkEntry(master=frame, placeholder_text="Email address", width=300, border_width=0)
phone_number = customtkinter.CTkEntry(master=frame, placeholder_text="Phone number", width=300, border_width=0)
button = customtkinter.CTkButton(master=frame, text="Generate", border_width=0, command=generate_button)

frame.pack(pady=10, padx=10, fill="both", expand=True)
heading.pack(pady=12, padx=10)
client_name.pack(pady=5, padx=10)
application_type.pack(pady=5, padx=10)
application_fee.pack(pady=5, padx=10)
email_address.pack(pady=5, padx=10)
phone_number.pack(pady=5, padx=10)
button.pack(pady=25, padx=10)

client_name.insert(0, 'Farabi Hussain')
application_type.insert(0, 'Express Entry')
application_fee.insert(0, '500')
email_address.insert(0, 'farabi@email.com')
phone_number.insert(0, '(123) 456-7890')

root.mainloop()
