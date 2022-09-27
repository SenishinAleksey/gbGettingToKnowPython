import os
import pickle

phonebook_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../phonebook.pickle')
phonebook = {}


def init():
    global phonebook
    if os.path.exists(phonebook_file_path):
        with open(phonebook_file_path, 'rb') as f:
            phonebook = pickle.load(f)


def add(last_name, name, phone, description):
    if not last_name or not name or not phone or not description:
        raise Warning('извините, но все поля обязательны к заполнению')
    if phone in phonebook:
        raise Warning('такой номер телефона уже есть в телефонной книге')
    phonebook[phone] = [last_name, name, description]
    save()
    return 'запись добавлена'


def save():
    with open(phonebook_file_path, 'wb') as phonebook_file:
        pickle.dump(phonebook, phonebook_file)


def get_notes_for_page(page):
    notes = get_all_notes()
    if not notes:
        raise Warning('телефонная книга пуста')
    pages_count = len(notes) // 5
    if len(notes) % 5 != 0:
        pages_count += 1
    return {
        'page': page,
        'pages_count': pages_count,
        'notes': notes[5 * (page - 1):5 * page]
    }


def get_all_notes():
    notes = []
    number_note = 1
    for phone, data in phonebook.items():
        notes.append((number_note, data[0], data[1], phone, data[2]))
        number_note += 1
    return notes


def get_note_data_by_number(number_note):
    notes = get_all_notes()
    if number_note not in list(zip(*notes))[0]:
        raise Warning('записи с таким номером не существует')
    for note in notes:
        if number_note == note[0]:
            return note[1:]


def edit(phone, last_name, name, description):
    if not last_name or not name or not phone or not description:
        raise ValueError('не переданы обязательные поля')
    if phone not in phonebook:
        raise Warning('такого номера телефона нет в телефонной книге')
    phonebook[phone] = [last_name, name, description]
    save()
    return f'данные номера {phone} изменены'


def del_note(phone):
    if not phone:
        raise ValueError('не переданы обязательные поля')
    if phone not in phonebook:
        raise Warning('такого номера телефона нет в телефонной книге')
    phonebook.pop(phone)
    save()
    return f'номер {phone} удален'


def get_note_data_by_phone(phone):
    return phonebook.get(phone, False)


def export_phonebook(file_name, write_data_function):
    if not file_name:
        raise Warning('название файла не может быть пустым!')
    notes = get_all_notes()
    write_data_function(file_name, notes)
    return f'телефонная книга записана в {file_name}'


def import_phonebook(file_name, get_data_function):
    if not file_name:
        raise Warning('название файла не может быть пустым!')
    if not os.path.exists(file_name):
        raise Warning('такого файла не существует')
    added = 0
    edited = 0
    no_changes = 0
    notes = get_data_function(file_name)
    for note in notes:
        phonebook_note_data = get_note_data_by_phone(note[2])
        if phonebook_note_data:
            if note[0] == phonebook_note_data[0] and note[1] == phonebook_note_data[1] and note[3] == \
                    phonebook_note_data[2]:
                no_changes += 1
            else:
                edit(note[2], note[0], note[1], note[3])
                edited += 1
        else:
            add(note[0], note[1], note[2], note[3])
            added += 1
    return f'импортировано. Добавлено новых записей: {added}, изменено: {edited}, оставлено без изменений: {no_changes}'
