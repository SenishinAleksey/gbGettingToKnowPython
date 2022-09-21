# Создайте программу для игры с конфетами
# Условие задачи: На столе лежит 2021 конфета. Играют два игрока делая ход друг после друга. Первый ход определяется
# жеребьёвкой. За один ход можно забрать не более чем 28 конфет.

from random import randint


def get_bot_turn(num):
    if num - 28 > 29 or num == 29:
        return randint(1, 28)
    else:
        return num - 29


print('Введите количество игроков. 1 (с ботом) или 2 (с другим игроком):')
while True:
    mode_input = input()
    if mode_input in ('1', '2'):
        with_bot = mode_input == '1'
        break
    else:
        print('Введите 1 или 2')
number_of_candies = 2021
user = randint(1, 2)
print(f'Игру начинает {user} игрок')
while True:
    print(f'Ход {user} игрока. Конфет на столе: {number_of_candies}')
    if with_bot and user == 2:
        bot_turn = get_bot_turn(number_of_candies)
        print(f'Бот решил взять: {bot_turn}')
        number_of_candies -= bot_turn
    else:
        while True:
            user_input = input()
            if user_input.isdigit() and 0 < int(user_input) <= 28:
                number_of_candies -= int(user_input)
                break
            else:
                print('Должно быть введено число от 1 до 28')
    user = 2 if user == 1 else 1
    if number_of_candies <= 28:
        print(f'Победил {user} игрок. Конфет на столе осталось: {number_of_candies}')
        break
