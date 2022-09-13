# Напишите программу, которая принимает на вход вещественное число и показывает сумму его цифр.

num = ''
while len(num) == 0:
    user_input = input('Введите число: ')
    if not user_input.isdigit():
        print('Должно быть введено число')
    else:
        num = user_input
sum_ = 0
for n in num:
    if n.isdigit():
        sum_ += int(n)
print(f'Сумма чисел: {sum_}')
