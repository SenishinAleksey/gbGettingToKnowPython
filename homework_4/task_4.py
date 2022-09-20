# Задана натуральная степень k. Сформировать случайным образом список коэффициентов (значения от 0 до 100) многочлена
# и записать в файл многочлен степени k.

from random import randint


def get_x_with_coef(c): return str(c) + 'x' if c != 1 else 'x'


k = int(input())
res = []
for i in range(k, -1, -1):
    coefficient = randint(0, 100)
    if coefficient == 0:
        continue
    else:
        if i == 0:
            res.append(str(coefficient))
            continue
        elif i == 1:
            res.append(get_x_with_coef(coefficient))
        else:
            res.append(get_x_with_coef(coefficient) + '^' + str(i))

with open('task_4.txt', 'w') as f:
    f.write('+'.join(res) + '=0')
