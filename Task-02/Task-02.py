# Задача 2. Координаты

import random


def f(x, y):
    x += random.randint(0, 10)
    y += random.randint(0, 5)
    return x / y


def f2(x, y):
    x -= random.randint(0, 10)
    y -= random.randint(0, 5)
    return y / x


line_count = 0

try:
    with open('coordinates.txt', 'r') as file, open('result.txt', 'w') as file_2:
        for line in file:
            line_count += 1
            nums_list = line.strip().split(', ')
            print(nums_list)
            number = random.randint(0, 100)

            try:
                res1 = f(int(nums_list[0]), int(nums_list[1]))
                res2 = f2(int(nums_list[0]), int(nums_list[1]))
                my_list = [str(item) for item in sorted([res1, res2, number])]
                file_2.write(' '.join(my_list))

            except ZeroDivisionError:
                print('Ошибка! На ноль делить нельзя')
            except ValueError:
                print(f'Ошибка в строке {line_count}! Проверьте содержимое файла coordinates.txt.')
except FileNotFoundError:
    print('Ошибка! Проверьте наличие файла coordinates.txt.')
