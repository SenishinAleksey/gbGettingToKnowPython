import json


def write(file_name, workers):
    data = [{
        'id': worker['id'],
        'last_name': worker['last_name'],
        'name': worker['name'],
        'year_of_birth': worker['year_of_birth'],
        'position': worker['position'],
        'work_phone': worker['work_phone'],
        'salary': worker['salary']
    } for worker in workers.values()]
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get(file_name):
    data = []
    with open(file_name) as f:
        workers = json.load(f)
        for worker in workers:
            if len(worker) == 7 and worker['id'] and worker['last_name'] and worker['name'] \
                    and worker['year_of_birth'] and worker['position'] and worker['work_phone'] and worker['salary']:
                data.append(worker)
            else:
                raise Warning('некорректный формат файла импорта')
    return data
