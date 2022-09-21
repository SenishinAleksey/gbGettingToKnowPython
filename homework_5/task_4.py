# Реализуйте RLE алгоритм: реализуйте модуль сжатия и восстановления данных.

def rle_encode(s):
    res = ''
    count = 1
    symbol = s[0]
    for c in s[1:]:
        if c == symbol:
            count += 1
        else:
            res += str(count) + symbol
            symbol = c
            count = 1
    res += str(count) + symbol
    return res


def rle_decode(s):
    res = ''
    number = ''
    for c in s:
        if c.isdigit():
            number += c
        else:
            res += c * int(number)
            number = ''
    return res


print(rle_encode('WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'))
print(rle_decode('12W1B12W3B24W1B14W'))
