# Задайте числами список из N элементов, заполненных из промежутка [-N, N]. Найдите произведение элементов на указанных
# позициях. Позиции хранятся в файле file.txt в одной строке одно число.

num = 0
while num <= 0:
    user_input = input('Введите число: ')
    if not user_input.isdigit() and int(user_input) <= 0:
        print('Должно быть введено число больше 0')
    else:
        num = int(user_input)
lst = list(range(-num, num + 1))
positions = []
with open('file.txt', encoding='utf-8') as f:
    for string in f:
        position = string.strip()
        if position.isdigit():
            positions.append(int(position))
if positions:
    result = 1
    for i in positions:
        if i > len(lst) - 1 or i < -len(lst):
            print(f'Позиция {i} не входит в получившийся список и пропускается')
            continue
        result *= lst[i]
    print(result)
else:
    print('В файле не указаны позиции')
