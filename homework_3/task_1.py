# Задайте список из нескольких чисел. Напишите программу, которая найдёт сумму элементов списка, стоящих на
# нечётной позиции.


lst = [int(i) for i in input().split()]
print(sum(lst[1::2]))
