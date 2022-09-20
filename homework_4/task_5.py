# Даны два файла, в каждом из которых находится запись многочлена. Задача - сформировать файл, содержащий сумму
# многочленов.

from re import findall
from collections import Counter


def get_coefficients(polynomial: str):
    lst = findall(r'[+-]*\d*x\^\d*|[+-]\d*x|[+-]\d+', polynomial)
    coefficients = {}
    for v in lst:
        if 'x^' in v:
            v_split = v.split('x^')
            coefficients[int(v_split[1])] = int(v_split[0]) if v_split[0][-1].isdigit() else (int(v_split[0] + '1'))
        elif 'x' in v:
            v_split = v.split('x')
            coefficients[1] = int(v_split[0]) if v_split[0][-1].isdigit() else (int(v_split[0] + '1'))
        else:
            coefficients[0] = int(v)
    return coefficients


files = ('task_5_1.txt', 'task_5_2.txt')
res_coefficients = Counter()
for file in files:
    with open(file) as f:
        s = f.readline()
        coefficients = get_coefficients(s)
        res_coefficients.update(coefficients)

res_polynomial = ''
for i in sorted(res_coefficients, reverse=True):
    coefficient = res_coefficients[i]
    if not res_polynomial:
        res_polynomial += str(coefficient)
    else:
        if coefficient > 0:
            res_polynomial += '+'
        res_polynomial += str(coefficient)
    if i:
        res_polynomial += 'x'
    if i > 1:
        res_polynomial += '^' + str(i)
res_polynomial += '=0'

with open('task_5_3.txt', 'w') as f:
    f.write(res_polynomial)

# Так же, наткнулся на библиотеку sympy, доступную в pip, с помощью которой можно складывать многочлены

# from sympy import simplify, sympify
# a = sympify('17 * x ** 5 + x ** 4 + 55 * x ** 3 - 38 * x ** 2 + 60 * x + 54')
# b = sympify('95 * x ** 4 + 32 * x ** 3 + 47 * x ** 2 - 72 * x + 43')
# print(simplify(a + b))

# а так же, решать квадратные уравнения

# from sympy.solvers import solve
# from sympy import Symbol
# equation = 'x ** 2 - 16 * x + 28'
# x = Symbol('x')
# print('Корни уравнения:', solve(equation, x))
