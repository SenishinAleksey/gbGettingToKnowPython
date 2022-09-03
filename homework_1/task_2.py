# Напишите программу для. проверки истинности утверждения ¬(X ⋁ Y ⋁ Z) = ¬X ⋀ ¬Y ⋀ ¬Z для всех значений предикат.

def get_values():
    for n in range(8):
        b = ''
        while n > 0:
            b = str(n % 2) + b
            n = n // 2
        b = b.zfill(3)
        yield list(int(num) for num in b)


for value in get_values():
    x, y, z = value
    print(f'Проверка для X={x}, Y={y}, Z={z}: ', end='')
    if (not(x or y or z)) == (not x and not y and not z):
        print('верно')
    else:
        print('не верно')
