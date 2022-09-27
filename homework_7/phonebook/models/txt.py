def write(file_name, notes):
    with open(file_name, 'w') as f:
        for i, note in enumerate(notes):
            f.write(f'{note[1]}\n{note[2]}\n{note[3]}\n{note[4]}\n')
            if i != len(notes) - 1:
                f.write('\n')


def get(file_name):
    file_data = [[], [], [], []]
    with open(file_name, 'r') as f:
        i = 0
        for line in f:
            data = line.strip()
            if (len(data) == 0 and i != 4) or (len(data) and i == 4):
                raise Warning('некорректный формат файла импорта')
            if i != 4:
                file_data[i].append(data)
            i = i + 1 if i != 4 else 0
    return list(zip(*file_data))
