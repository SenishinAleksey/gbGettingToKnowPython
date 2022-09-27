import models.csv as csv
import models.json as json
import models.phonebook as phonebook
import models.txt as txt
import models.xml as xml
import views

phonebook.init()


def main_menu():
    user_answer = views.show_main_menu()
    if user_answer == 1:
        phonebook_list()
    elif user_answer == 2:
        add_new_note()
    elif user_answer == 3:
        import_phonebook()
    elif user_answer == 4:
        export_phonebook()
    elif user_answer == 0:
        exit(0)


def phonebook_list(page=1):
    try:
        notes = phonebook.get_notes_for_page(page)
        user_answer = views.show_phonebook(notes)
        if user_answer == 1:
            edit_note(page)
        elif user_answer == 2:
            del_note(page)
        elif user_answer == 3:
            phonebook_list(page + 1)
        elif user_answer == 4:
            phonebook_list(page - 1)
        elif user_answer == 0:
            main_menu()
    except Warning as mes:
        views.show_error(mes)
        main_menu()


def edit_note(page=1):
    number_note = views.number_notes_request()
    try:
        note_data = phonebook.get_note_data_by_number(number_note)
        last_name, name, description = views.edit_note(note_data)
        mes = phonebook.edit(note_data[2], last_name, name, description)
        views.show_success(mes)
    except Warning as mes:
        views.show_error(mes)
    phonebook_list(page)


def del_note(page=1):
    number_note = views.number_notes_request()
    try:
        note_data = phonebook.get_note_data_by_number(number_note)
        mes = phonebook.del_note(note_data[2])
        views.show_success(mes)
        phonebook_list()
    except Warning as mes:
        views.show_error(mes)
        phonebook_list(page)


def add_new_note():
    last_name, name, phone, description = views.add_note()
    try:
        mes = phonebook.add(last_name, name, phone, description)
        views.show_success(mes)
    except Warning as mes:
        views.show_error(mes)
    main_menu()


def export_phonebook():
    user_answer = views.file_type_menu()
    file_name = views.file_name_request()
    try:
        if user_answer == 1:
            mes = phonebook.export_phonebook(file_name, txt.write)
        elif user_answer == 2:
            mes = phonebook.export_phonebook(file_name, csv.write)
        elif user_answer == 3:
            mes = phonebook.export_phonebook(file_name, json.write)
        else:
            mes = phonebook.export_phonebook(file_name, xml.write)
        views.show_success(mes)
    except Warning as msg:
        views.show_error(msg)
    main_menu()


def import_phonebook():
    user_answer = views.file_type_menu()
    file_name = views.file_name_request()
    try:
        if user_answer == 1:
            mes = phonebook.import_phonebook(file_name, txt.get)
        elif user_answer == 2:
            mes = phonebook.import_phonebook(file_name, csv.get)
        elif user_answer == 3:
            mes = phonebook.import_phonebook(file_name, json.get)
        else:
            mes = phonebook.import_phonebook(file_name, xml.get)
        views.show_success(mes)
    except Warning as msg:
        views.show_error(msg)
    main_menu()
