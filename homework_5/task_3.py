# Создайте программу для игры в "Крестики-нолики".

from random import randint, choice

game_pole = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
win_combinations = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    (1, 4, 7),
    (2, 5, 8),
    (3, 6, 9),
    (1, 5, 9),
    (3, 5, 7)
)


def print_pole(pole):
    for i in range(3):
        print(' | '.join(pole[i * 3: i * 3 + 3]))


def is_win(user_selects):
    win = False
    for a, b, c in win_combinations:
        if a in user_selects and b in user_selects and c in user_selects:
            win = True
            break
    return win


def get_bot_turn():
    turn = 0
    for a, b, c in win_combinations:
        if a in users_selects[1] and b in users_selects[1] and c not in users_selects[2]:
            turn = c
        elif b in users_selects[1] and c in users_selects[1] and a not in users_selects[2]:
            turn = a
        elif a in users_selects[1] and c in users_selects[1] and b not in users_selects[2]:
            turn = b
    for a, b, c in win_combinations:
        if a in users_selects[2] and b in users_selects[2] and c not in users_selects[1]:
            turn = c
        elif b in users_selects[2] and c in users_selects[2] and a not in users_selects[1]:
            turn = a
        elif a in users_selects[2] and c in users_selects[2] and b not in users_selects[1]:
            turn = b
    if turn:
        return str(turn)
    else:
        return choice(list(filter(lambda x: x.isdigit(), game_pole)))


users_selects = {
    1: [],
    2: []
}

print('Введите количество игроков. 1 (с ботом) или 2 (с другим игроком):')
while True:
    mode_input = input()
    if mode_input in ('1', '2'):
        with_bot = mode_input == '1'
        break
    else:
        print('Введите 1 или 2')
user = randint(1, 2)
print(f'Игру начинает {user} игрок')
while True:
    print_pole(game_pole)
    print(f'Ход {user} игрока')
    if with_bot and user == 2:
        bot_turn = get_bot_turn()
        game_pole[game_pole.index(bot_turn)] = 'O'
        users_selects[user].append(int(bot_turn))
        pass
    else:
        while True:
            user_input = input('Выберите номер поля: ')
            if user_input.isdigit() and 0 < int(user_input) <= 9:
                if int(user_input) in users_selects[1] + users_selects[2]:
                    print('Это поле уже занято')
                    continue
                game_pole[game_pole.index(user_input)] = 'X' if user == 1 else 'O'
                users_selects[user].append(int(user_input))
                break
            else:
                print('Должно быть выбрано не занятое поле от 1 до 9')
    if is_win(users_selects[user]):
        print_pole(game_pole)
        print(f'Победил {user} игрок.')
        break
    elif len(users_selects[1] + users_selects[2]) == 9:
        print_pole(game_pole)
        print('Ничья')
        break
    user = 2 if user == 1 else 1
