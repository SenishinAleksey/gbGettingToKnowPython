# Напишите программу, которая принимает на вход вещественное число и показывает сумму его цифр.

num = ''
while len(num) == 0:
    user_input = input('Введите число: ')
    if not user_input.replace('.', '', 1).isdigit():
        print('Должно быть введено число')
    else:
        num = user_input
print(f'Сумма цифр: {sum(map(int, filter(lambda x: x.isdigit(), num)))}')
