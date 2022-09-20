# Вычислить число c заданной точностью d

from math import pi

d = 0.001
s = str(d)
ndigits = len(s) - s.find('.') - 1
print(round(pi, ndigits))
