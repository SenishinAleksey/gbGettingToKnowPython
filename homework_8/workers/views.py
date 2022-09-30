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


def show_workers_list(workers):
    print(f"\033[1mСписок работников\033[0m")
    show_workers_notes(workers['notes'])
    menu = {
        'title': '',
        'options':
            {
                1: 'Добавить'
            }
    }
    if workers['notes']:
        menu['options'][2] = 'Карточка работника'
        menu['options'][3] = 'Поиск'
    if workers['page'] < workers['pages_count']:
        menu['options'][4] = 'След. стр.'
    if workers['page'] > 1:
        menu['options'][5] = 'Пред. стр.'
    menu['options'][6] = 'Импорт'
    menu['options'][7] = 'Экспорт'
    menu['options'][0] = 'Выход'
    return show_menu(menu, in_line=True)


def show_workers_notes(workers_notes):
    print('-' * 40)
    if not workers_notes:
        print('Список пуст')
    for worker in workers_notes:
        print(f'{worker[0]}: {worker[1]} - {worker[2]}')
    print('-' * 40)


def add_worker():
    last_name = input('Фамилия: ')
    name = input('Имя: ')
    year_of_birth = input('Год рождения: ')
    position = input('Должность: ')
    work_phone = input('Рабочий телефон: ')
    salary = input('Оклад: ')
    return last_name, name, year_of_birth, position, work_phone, salary


def show_error(mes):
    print(f'\033[31mОшибка: {mes}\033[0m')


def show_success(mes):
    print(f'\033[32mУспешно: {mes}\033[0m')


def worker_id_request():
    answer = input('Введите ИД работника: ')
    if answer.isdigit():
        return int(answer)
    show_error('ожидается число')
    return worker_id_request()


def file_type_menu():
    menu = {
        'title': 'Выберите тип файла:',
        'options': {
            1: 'csv',
            2: 'json',
        }
    }
    return show_menu(menu)


def file_name_request():
    return input('Введите название файла: ')


def show_more_info(worker_data):
    print(f"\033[1mКарточка работника\033[0m")
    print('-' * 40)
    print(f'ИД: {worker_data["id"]}')
    print(f'Имя: {worker_data["last_name"]} {worker_data["name"]}')
    print(f'Должность: {worker_data["position"]}\tРабочий телефон: {worker_data["work_phone"]}')
    print(f'Год рождения: {worker_data["year_of_birth"]}\tОклад: {worker_data["salary"]} руб.')
    print('-' * 40)
    menu = {
        'title': '',
        'options':
            {
                1: 'Изменить',
                2: 'Удалить',
                0: 'Вернуться в список'
            }
    }
    return show_menu(menu, in_line=True)


def edit_worker(worker_data):
    print('Введите новые значения или оставьте пустым, если не требуется изменять:')
    last_name = input(f'Фамилия [{worker_data["last_name"]}]: ')
    name = input(f'Имя [{worker_data["name"]}]: ')
    position = input(f'Должность [{worker_data["position"]}]: ')
    work_phone = input(f'Рабочий телефон [{worker_data["work_phone"]}]: ')
    year_of_birth = input(f'Год рождения [{worker_data["year_of_birth"]}]: ')
    salary = input(f'Оклад [{worker_data["salary"]}]: ')
    return {
        'id': worker_data['id'],
        'last_name': last_name if last_name else worker_data['last_name'],
        'name': name if name else worker_data['name'],
        'position': position if position else worker_data['position'],
        'work_phone': work_phone if work_phone else worker_data['work_phone'],
        'year_of_birth': year_of_birth if year_of_birth else worker_data['year_of_birth'],
        'salary': salary if salary else worker_data['salary'],
    }


def show_search_params():
    params = {
        1: 'last_name',
        2: 'name',
        3: 'year_of_birth',
        4: 'position',
        5: 'work_phone'
    }
    menu = {
        'title': 'Выберите параметр для поиска:',
        'options': {
            1: 'Фамилия',
            2: 'Имя',
            3: 'Год рождения',
            4: 'Должность',
            5: 'Рабочий телефон'
        }
    }
    return params[show_menu(menu)]


def search_query_request():
    return input('Введите фразу для поиска: ')


def show_search_result(workers, query):
    print(f"\033[1mРезультаты поиска для \"{query}\"\033[0m")
    show_workers_notes(workers['notes'])
    menu = {
        'title': '',
        'options': {}
    }
    if workers['notes']:
        menu['options'][1] = 'Карточка работника'
    if workers['page'] < workers['pages_count']:
        menu['options'][4] = 'След. стр.'
    if workers['page'] > 1:
        menu['options'][5] = 'Пред. стр.'
    menu['options'][0] = 'Вернуться в список'
    return show_menu(menu, in_line=True)
