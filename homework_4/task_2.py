# Задайте натуральное число N. Напишите программу, которая составит список простых множителей числа N

n = int(input())
res = []
i = 2
while n >= i ** 2:
    if n % i == 0:
        res.append(i)
        n = n // i
    else:
        i += 1
if n > 1:
    res.append(n)
print(res)
