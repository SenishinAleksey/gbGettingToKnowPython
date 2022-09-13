# Задайте список из n чисел последовательности (1+1/n)^n выведите на экран их сумму.

num = 0
while num <= 0:
    user_input = input('Введите число: ')
    if not user_input.isdigit() and int(user_input) <= 0:
        print('Должно быть введено число больше 0')
    else:
        num = int(user_input)
lst = []
for n in range(1, num + 1):
    lst.append((1 + 1 / n) ** n)
print(sum(lst))
