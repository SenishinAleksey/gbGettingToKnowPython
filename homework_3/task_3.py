# Задайте список из вещественных чисел. Напишите программу, которая найдёт разницу между максимальным и минимальным
# значением дробной части элементов.

lst = [float(i) for i in input().split()]
fracts = [float('0.' + str(i).split('.')[1]) for i in lst if i % 1 != 0]
print(max(fracts) - min(fracts))
