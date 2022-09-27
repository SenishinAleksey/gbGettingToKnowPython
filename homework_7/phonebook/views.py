def show_menu(menu, in_line=False):
    if menu['title']:
        print(f"\033[1m{menu['title']}\033[0m")
    for num, option in menu['options'].items():
        if in_line and num != 0:
            print(f'{num} - \033[3m{option}\033[0m', end=' ')
        else:
            print(f'{num} - \033[3m{option}\033[0m')
    answer = input('Введите номер пункта меню: ')
    if answer.isdigit():
        answer = int(answer)
        if answer in menu['options']:
            return answer
    show_error('такого пункта не существует')
    return show_menu(menu, in_line)


def show_main_menu():
    menu = {
        'title': 'Главное меню',
        'options': {
            1: 'Просмотр справочника',
            2: 'Добавить запись',
            3: 'Импорт из файла',
            4: 'Экспорт в файл',
            0: 'Выход'
        }
    }
    return show_menu(menu)


def show_phonebook(notes):
    print('-' * 40)
    for note in notes['notes']:
        print(note[0], note[1], note[2], note[3], note[4])
    print('-' * 40)
    menu = {
        'title': '',
        'options':
            {
                1: 'Изменить запись',
                2: 'Удалить запись'
            }
    }
    if notes['page'] < notes['pages_count']:
        menu['options'][3] = 'След. стр.'
    if notes['page'] > 1:
        menu['options'][4] = 'Пред. стр.'
    menu['options'][0] = 'Главное меню'
    return show_menu(menu, in_line=True)


def add_note():
    last_name = input('Фамилия: ')
    name = input('Имя: ')
    phone = input('Телефон: ')
    description = input('Описание: ')
    return last_name, name, phone, description


def show_error(mes):
    print(f'\033[31mОшибка: {mes}\033[0m')


def show_success(mes):
    print(f'\033[32mУспешно: {mes}\033[0m')


def number_notes_request():
    answer = input('Введите номер записи: ')
    if answer.isdigit():
        return int(answer)
    show_error('ожидается число')
    return number_notes_request()


def edit_note(note_data):
    print('Введите новые значения или оставьте пустым, если не требуется изменять:')
    last_name = input(f'Фамилия [{note_data[0]}]: ')
    name = input(f'Имя [{note_data[1]}]: ')
    description = input(f'Описание [{note_data[3]}]: ')
    return (
        last_name if last_name else note_data[0],
        name if name else note_data[1],
        description if description else note_data[3]
    )


def file_type_menu():
    menu = {
        'title': 'Выберите тип файла:',
        'options': {
            1: 'txt',
            2: 'csv',
            3: 'json',
            4: 'xml'
        }
    }
    return show_menu(menu)


def file_name_request():
    return input('Введите название файла: ')
