import csv


def write(file_name, notes):
    data = [[note[1], note[2], note[3], note[4]] for note in notes]
    with open(file_name, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['Фамилия', 'Имя', 'Телефон', 'Описание'])
        csv_writer.writerows(data)


def get(file_name):
    data = []
    with open(file_name) as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 4 and row[0] and row[1] and row[2] and row[3]:
                data.append(row)
            else:
                raise Warning('некорректный формат файла импорта')
    return data[1:]
