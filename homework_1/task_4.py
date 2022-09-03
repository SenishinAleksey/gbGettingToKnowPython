# Напишите программу, которая по заданному номеру четверти, показывает диапазон возможных координат точек в этой
# четверти (x и y).

diapasons = (
    'X: [0:∞)\nY: [0:∞)',
    'X: (-∞:0]\nY: [0:∞)',
    'X: (-∞:0]\nY: (-∞:0]',
    'X: [0:∞)\nY: (-∞:0]',
)
quarter = 0
while not quarter:
    number = int(input('Введите номер четверти: '))
    if 0 < number < 5:
        quarter = number
    else:
        print('Введите число от 1 до 4')
print(diapasons[quarter - 1])
