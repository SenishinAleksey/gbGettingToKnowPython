import csv


def write(file_name, workers):
    data = [[
        worker['id'],
        worker['last_name'],
        worker['name'],
        worker['year_of_birth'],
        worker['position'],
        worker['work_phone'],
        worker['salary'],
    ] for worker in workers.values()]
    with open(file_name, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([
            'ИД',
            'Фамилия',
            'Имя',
            'Год рождения',
            'Должность',
            'Рабочий телефон',
            'Оклад'
        ])
        csv_writer.writerows(data)


def get(file_name):
    data = []
    with open(file_name) as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 7 and row[0] and row[1] and row[2] and row[3] and row[4] and row[5] and row[6]:
                data.append({
                    'id': row[0],
                    'last_name': row[1].capitalize(),
                    'name': row[2].capitalize(),
                    'year_of_birth': row[3],
                    'position': row[4],
                    'work_phone': row[5],
                    'salary': row[6]
                })
            else:
                raise Warning('некорректный формат файла импорта')
    return data[1:]
