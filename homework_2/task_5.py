# Реализуйте алгоритм перемешивания списка

from random import randint

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
len_lst = len(lst)
for i in range(len_lst):
    rand_position = randint(i, len_lst - 1)
    lst[i], lst[rand_position] = lst[rand_position], lst[i]
print(lst)
