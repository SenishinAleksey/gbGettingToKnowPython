# Задайте число. Составьте список чисел Фибоначчи, в том числе для отрицательных индексов


def get_fibbonachi(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return get_fibbonachi(n - 1) + get_fibbonachi(n - 2)


def get_negafibbonachi(n):
    if n == -1:
        return 1
    elif n == -2:
        return -1
    return get_negafibbonachi(n + 2) - get_negafibbonachi(n + 1)


num = int(input())
result = []
for i in list(range(-num, num + 1)):
    if i < 0:
        result.append(get_negafibbonachi(i))
    else:
        result.append(get_fibbonachi(i))
print(result)
