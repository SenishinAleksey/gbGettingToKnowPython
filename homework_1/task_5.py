# Напишите программу, которая принимает на вход координаты двух точек и находит расстояние между ними в 2D пространстве.

print('Введите координаты точки A')
a = int(input('X: ')), int(input('Y: '))
print('Введите координаты точки B')
b = int(input('X: ')), int(input('Y: '))
print(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5)