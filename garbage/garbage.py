##
def handle_click_history():
    global history_window, history_entries, status_string, history_table_frame, form, icon
    status_string.set('opened history')
    os.system('cls')

    history_entries = form_logic.get_history()

    if (history_entries is None):
        popup(title="Failed", message="No history available", corner_radius=4)

    else:
        if (history_window is None or not history_window.winfo_exists()): 
            history_window = ctk.CTkToplevel()

            history_table_contents = [['created by','created date','client','type','fee','active']]

            for entry in history_entries[table_ranges['start'] : table_ranges['end']]:
                history_table_contents.append([
                    entry['created_by'],
                    entry['created_date'],
                    entry['client_name'],
                    entry['application_type'],
                    entry['application_fee'],
                    entry['is_active'].title(),
                ])

            form['inactive_filter_btn'] = ctk.CTkButton(master=history_window, text="show only inactive", border_width=1, corner_radius=4, fg_color='transparent', command=lambda:show_only_inactive(history_table_contents), width=120)
            form['inactive_btn'] = ctk.CTkButton(master=history_window, text="inactive", border_width=1, corner_radius=4, fg_color='transparent', command=lambda:toggle_active(False), width=60)
            form['active_btn'] = ctk.CTkButton(master=history_window, text="active", border_width=1, corner_radius=4, fg_color='transparent', command=lambda:toggle_active(True), width=60)
            form['import_btn'] = ctk.CTkButton(master=history_window, text="import", border_width=1, corner_radius=4, fg_color='transparent', command=handle_click_import, width=60)
            form['prev_btn'] = ctk.CTkButton(master=history_window, text="<", border_width=0, corner_radius=4, fg_color='transparent', command=handle_click_prev, width=30, state='disabled')
            form['next_btn'] = ctk.CTkButton(master=history_window, text=">", border_width=1, corner_radius=4, fg_color="transparent", command=handle_click_next, width=30, state='normal')

            if len(history_entries) < 15:
                form['next_btn'].configure(fg_color='transparent', state='disabled', border_width=0)

            history_table_frame = CTkTable(
                master=history_window, 
                row=16, 
                column=len(history_table_contents[0]), 
                values=history_table_contents, 
                corner_radius=4, 
                header_color="#5e5e5e",
                hover_color="#1f538d",
            )

            form['row_selector'] = CTkTableRowSelector(history_table_frame, max_selection=1)

            history_table_frame.pack(expand=False, fill="both", padx=20, pady=[20,60])
            form['inactive_filter_btn'].place(x=20, y=505)
            form['inactive_btn'].place(x=660, y=505)
            form['active_btn'].place(x=740, y=505)
            form['import_btn'].place(x=820, y=505)
            form['prev_btn'].place(x=900, y=505)
            form['next_btn'].place(x=950, y=505)

            w = 1000
            h = 550
            x = (ws/2) - (w/2)
            y = (hs/2) - (h/2) + 40

            history_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
            history_window.focus()
            history_window.after(201, lambda: history_window.iconbitmap("assets\\logo.ico"))
            history_window.title("History")
            history_window.resizable(False, False)
            history_window.after(100, lambda: history_window.focus())

        else:
            history_window.focus()


##
def show_only_inactive(history_table_contents):
    global form, history_entries, history_table_frame, filters, filtered_entries

    filtered_entries = [['created by','created date','client','type','fee','active']]

    if (filters['only_inactive'] == False):
        for entry in (history_entries):
            if (str(entry['is_active']).lower() == 'false'):
                filtered_entries.append([
                    entry['created_by'],
                    entry['created_date'],
                    entry['client_name'],
                    entry['application_type'],
                    entry['application_fee'],
                    entry['is_active'].title(),
                ])

        form['inactive_filter_btn'].configure(border_width=0, fg_color='white', text_color='black', text="show all")
        filters['only_inactive'] = True

    else:
        filtered_entries = history_table_contents
        form['inactive_filter_btn'].configure(border_width=1, fg_color='transparent', text_color='white', text="show only inactive")
        filters['only_inactive'] = False

    form['row_selector'].clear_selection()
    history_table_frame.update_values(filtered_entries)


##
def toggle_active(set_to):
    global form, history_entries, history_table_frame

    selected_row = form['row_selector'].get()
    print(selected_row)
    form['row_selector'].clear_selection()
    matching_inactive_index = -1
    matching_index = -1
    index_of_flag = 5


    if (len(selected_row) == 0):
        popup(title="Failed", message="No row is selected", corner_radius=4)

    else:
        selected_row_data = {
            'created_by': selected_row[0][0],
            'created_date': selected_row[0][1],
            'client_name': selected_row[0][2],
            'application_type': selected_row[0][3],
            'application_fee': selected_row[0][4],
            'is_active': (selected_row[0][5]).title(),
        }

        for index, entry in enumerate(history_entries):

            if (filters['only_inactive'] == True):
                if (str(entry['is_active']).title() == 'False'): 
                    matching_inactive_index += 1

            if (
                entry['created_by'] == selected_row_data['created_by']
                and entry['created_date'] == selected_row_data['created_date']
                and entry['client_name'] == selected_row_data['client_name']
                and entry['application_type'] == selected_row_data['application_type']
                and entry['application_fee'] == selected_row_data['application_fee']
            ):
                matching_index = index

                # add 1 to the index to account for the heading column
                index_to_change = matching_index + 1
                if (filters['only_inactive'] == True):
                    index_to_change = matching_inactive_index + 1

                print('matching_index: ' + str(matching_index))
                print('matching_inactive_index: ' + str(matching_inactive_index))

    #             # change the value on the table
    #             history_table_frame.insert(
    #                 index_to_change, 
    #                 index_of_flag, 
    #                 'False' if set_to == 0 else 'True',
    #             )

    #             # change the value on the buffer
    #             history_entries[index]['is_active'] == 'False' if set_to == 0 else 'True'

    #             # write the change to file
    #             file_location = os.getcwd() + "\\logs\\history.csv"
    #             df = pd.read_csv(file_location)
    #             df.loc[(index_to_change-1), 'is_active'] = set_to
    #             df.to_csv(file_location, index=False) 

    #             # read the file again to repopulate with new changes
    #             history_entries = form_logic.get_history()

    #             break

    #     if (matching_index == -1 and len(selected_row) > 0):
    #         popup(title="Failed", message="Error finding the row", corner_radius=4)
    #         history_window.destroy()


## 
def handle_click_import():
    global form, history_entries

    selected_row = form['row_selector'].get()
    form['row_selector'].clear_selection()
    matching_entry = None

    if (len(selected_row) == 0):
        popup(title="Failed", message="No row is selected", corner_radius=4)

    else:
        selected_row_data = {
            'created_by': selected_row[0][0],
            'created_date': selected_row[0][1],
            'client_name': selected_row[0][2],
            'application_type': selected_row[0][3],
            'application_fee': selected_row[0][4],
        }

        for entry in history_entries:
            if (
                entry['created_by'] == selected_row_data['created_by'] and
                entry['created_date'] == selected_row_data['created_date'] and
                entry['client_name'] == selected_row_data['client_name'] and
                entry['application_type'] == selected_row_data['application_type'] and
                entry['application_fee'] == selected_row_data['application_fee']
            ):
                matching_entry = (entry)
                import_match(matching_entry)
                history_window.destroy()
                break

    if (matching_entry is None and len(selected_row) > 0):
        popup(title="Failed", message="Error finding the row", corner_radius=4)


##
def import_match(matching_entry):
    global form, status_string
    status_string.set("data imported from history")

    form['document_date'].delete(0, 'end')
    form['client_name'].delete(0, 'end')
    form['application_type'].delete(0, 'end')
    form['application_fee'].delete(0, 'end')
    form['email_address'].delete(0, 'end')
    form['phone_number'].delete(0, 'end')
    form['include_taxes'].set(True)
    form['is_active'].set(False)

    form['document_date'].insert(0, matching_entry['date_on_document'])
    form['client_name'].insert(0, matching_entry['client_name'])
    form['application_type'].insert(0, matching_entry['application_type'])
    form['application_fee'].insert(0, matching_entry['application_fee'])
    form['email_address'].insert(0, matching_entry['email'])
    form['phone_number'].insert(0, matching_entry['phone'])

    # set the payments
    for i in range(12):
        form['payment_list'][i]['date'].delete(0, 'end')
        form['payment_list'][i]['amount'].delete(0, 'end')

        form['payment_list'][i]['date'].insert(0, matching_entry['date_' + str(i + 1)])
        form['payment_list'][i]['amount'].insert(0, matching_entry['amount_' + str(i + 1)])

    # set the taxes switch
    if (matching_entry['add_taxes'].lower() == 'true'):
        form['include_taxes'].set(True)
    else:
        form['include_taxes'].set(False)

    # set the active switch
    if (matching_entry['is_active'].lower() == 'true'):
        form['is_active'].set(True)
    else:
        form['is_active'].set(False)


## 
def handle_click_next():
    switch_page('next')


##
def handle_click_prev():
    switch_page('prev')


##
def switch_page(direction):
    global form, table_ranges, history_table_frame, icon

    form['row_selector'].clear_selection()

    if (direction == 'next'):
        # navigate if a page is available
        if table_ranges['end'] < len(history_entries):
            table_ranges['start'] += 15
            table_ranges['end'] += 15

        # disable button when last page is reached
        if table_ranges['end'] + 15 > len(history_entries):
            form['next_btn'].configure(state='disabled', fg_color='transparent', border_width=0)
            form['prev_btn'].configure(state='normal', fg_color='transparent', border_width=1)

    elif (direction == 'prev'):
        # navigate if a page is available
        if table_ranges['start'] > 0:
            table_ranges['start'] -= 15 
            table_ranges['end'] -= 15

        # disable button when first page is reached
        if table_ranges['start'] - 15 < 0:
            form['prev_btn'].configure(state='disabled', fg_color='transparent', border_width=0)
            form['next_btn'].configure(state='normal', fg_color='transparent', border_width=1)

    history_table_contents = [['created by','created date','client','type','fee','active']]

    for entry in history_entries[table_ranges['start'] : table_ranges['end']]:

        current_row = [
            entry['created_by'],
            entry['created_date'],
            entry['client_name'],
            entry['application_type'],
            entry['application_fee'],
            entry['is_active'].title(),
        ]

        history_table_contents.append(current_row)

    history_table_frame.update_values(history_table_contents)
