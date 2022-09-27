import json


def write(file_name, notes):
    data = [{'last_name': note[1], 'name': note[2], 'phone': note[3], 'description': note[4]} for note in notes]
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get(file_name):
    data = []
    with open(file_name) as f:
        notes = json.load(f)
        for note in notes:
            note_data = [
                note.get('last_name', False),
                note.get('name', False),
                note.get('phone', False),
                note.get('description', False)
            ]
            if len(note_data) == 4 and note_data[0] and note_data[1] and note_data[2] and note_data[3]:
                data.append(note_data)
            else:
                raise Warning('некорректный формат файла импорта')
    return data
