# Напишите программу, которая принимает на вход число N и выдает набор произведений чисел от 1 до N

num = 0
while num <= 0:
    user_input = input('Введите число: ')
    if not user_input.isdigit() and int(user_input) <= 0:
        print('Должно быть введено число больше 0')
    else:
        num = int(user_input)
result = [1]
for i in range(2, num + 1):
    result.append(i * result[i - 2])
print(result)
