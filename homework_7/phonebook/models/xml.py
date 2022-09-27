import xml.etree.ElementTree as ElementTree
from xml.dom import minidom


def write(file_name, notes):
    xml = ElementTree.Element('phonebook')
    xml_notes = ElementTree.SubElement(xml, 'notes')
    for note in notes:
        xml_note = ElementTree.SubElement(xml_notes, 'note')
        xml_note_last_name = ElementTree.SubElement(xml_note, 'last_name')
        xml_note_last_name.text = note[1]
        xml_note_name = ElementTree.SubElement(xml_note, 'name')
        xml_note_name.text = note[2]
        xml_note_phone = ElementTree.SubElement(xml_note, 'phone')
        xml_note_phone.text = note[3]
        xml_note_description = ElementTree.SubElement(xml_note, 'description')
        xml_note_description.text = note[4]
    xml_str = minidom.parseString(ElementTree.tostring(xml)).toprettyxml(indent="   ")
    with open(file_name, 'w') as f:
        f.write(xml_str)


def get(file_name):
    data = []
    xml = minidom.parse(file_name)
    notes = xml.getElementsByTagName('note')
    for note in notes:
        last_name = note.getElementsByTagName('last_name')
        name = note.getElementsByTagName('name')
        phone = note.getElementsByTagName('phone')
        description = note.getElementsByTagName('description')
        note_data = [
            last_name[0].firstChild.data,
            name[0].firstChild.data,
            phone[0].firstChild.data,
            description[0].firstChild.data
        ]
        if len(note_data) == 4 and note_data[0] and note_data[1] and note_data[2] and note_data[3]:
            data.append(note_data)
        else:
            raise Warning('некорректный формат файла импорта')
    return data
