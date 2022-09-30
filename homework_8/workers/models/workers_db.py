import csv
import os

workers_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../workers.csv')
workers = {}


def init():
    global workers
    if os.path.exists(workers_file_path):
        with open(workers_file_path) as f:
            workers_data = csv.reader(f)
            for worker_data in workers_data:
                workers[int(worker_data[0])] = {
                    'id': worker_data[0],
                    'last_name': worker_data[1],
                    'name': worker_data[2],
                    'year_of_birth': worker_data[3],
                    'position': worker_data[4],
                    'work_phone': worker_data[5],
                    'salary': worker_data[6]
                }


def save():
    with open(workers_file_path, 'w') as f:
        csv_writer = csv.writer(f)
        for worker_data in workers.values():
            csv_writer.writerow([
                worker_data['id'],
                worker_data['last_name'],
                worker_data['name'],
                worker_data['year_of_birth'],
                worker_data['position'],
                worker_data['work_phone'],
                worker_data['salary'],
            ])


def add(last_name, name, year_of_birth, position, work_phone, salary, worker_id=0):
    if '' in [last_name, name, year_of_birth, position, work_phone, salary]:
        raise Warning('все поля обязательны к заполнению!')
    if not worker_id:
        worker_id = 1 if not len(workers) else max(workers.keys()) + 1
    workers[worker_id] = {
        'id': worker_id,
        'last_name': last_name.capitalize(),
        'name': name.capitalize(),
        'year_of_birth': year_of_birth,
        'position': position,
        'work_phone': work_phone,
        'salary': salary
    }
    save()
    return 'работник добавлен'


def edit(worker_data):
    worker_id = int(worker_data['id'])
    if not workers.get(worker_id, False):
        raise Warning('работника с таким ИД нет в списке')
    workers[worker_id] = worker_data
    save()
    return f'данные работника {worker_id} обновлены'


def delete(worker_id):
    worker_id = int(worker_id)
    if not workers.get(worker_id, False):
        raise Warning('работника с таким ИД нет в списке')
    workers.pop(worker_id)
    save()
    return 'работник удален'


def get_workers_for_page(page, workers_list):
    pages_count = len(workers_list) // 10
    if len(workers_list) % 10 != 0:
        pages_count += 1
    return {
        'page': page,
        'pages_count': pages_count,
        'notes': workers_list[10 * (page - 1):10 * page]
    }


def get_workers_list():
    workers_list = []
    worker_ids = sorted(workers.keys())
    for worker_id in worker_ids:
        worker_data = workers[worker_id]
        workers_list.append([
            worker_id,
            worker_data['last_name'] + ' ' + worker_data['name'][0] + '.',
            worker_data['position']
        ])
    return workers_list


def get_worker_data(worker_id):
    worker_data = workers.get(worker_id, False)
    if worker_data:
        return worker_data
    else:
        raise Warning('работника с таким ИД нет в списке')


def search(param, query, page=1):
    if len(query) == 0:
        raise Warning('Не задана фраза для поиска')
    search_result = []
    worker_ids = sorted(workers.keys())
    for worker_id in worker_ids:
        worker_data = workers[worker_id]
        if query.lower() in worker_data[param].lower():
            search_result.append([
                worker_id,
                worker_data['last_name'] + ' ' + worker_data['name'][0] + '.',
                worker_data['position']
            ])
    return get_workers_for_page(page, search_result)


def export_workers(file_name, write_data_function):
    if not file_name:
        raise Warning('название файла не может быть пустым!')
    write_data_function(file_name, workers)
    return f'список работников записан в {file_name}'


def import_workers(file_name, get_data_function):
    if not file_name:
        raise Warning('название файла не может быть пустым!')
    if not os.path.exists(file_name):
        raise Warning('такого файла не существует')
    added = 0
    edited = 0
    no_changes = 0
    workers_data = get_data_function(file_name)
    for worker_data in workers_data:
        worker_id = int(worker_data['id'])
        worker_db_data = workers.get(worker_id, False)
        if worker_db_data:
            has_changes = False
            for key, value in worker_data.items():
                if worker_db_data[key] != value:
                    has_changes = True
                    break
            if not has_changes:
                no_changes += 1
            else:
                edit(worker_data)
                edited += 1
        else:
            add(
                worker_data['last_name'],
                worker_data['name'],
                worker_data['year_of_birth'],
                worker_data['position'],
                worker_data['work_phone'],
                worker_data['salary'],
                worker_id
            )
            added += 1
    return f'импортировано. Добавлено новых работников: {added}, изменено: {edited}, оставлено без изменений: {no_changes}'
