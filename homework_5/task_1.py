# Напишите программу, удаляющую из текста все слова, содержащие "абв"

print(' '.join(list(filter(lambda x: 'абв' not in x, input().split()))))
