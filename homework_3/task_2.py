# Напишите программу, которая найдёт произведение пар чисел списка. Парой считаем первый и последний элемент, второй
# и предпоследний и т.д.


lst = [int(i) for i in input().split()]
result = []
for i in range(round(len(lst) / 2 + 0.1)):
    result.append(lst[i] * lst[-i - 1])
print(result)
