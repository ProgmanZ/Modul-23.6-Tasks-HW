# Задача 3. Счастливое число

import random

all_count = 0
out_file = open('out_file.txt', 'a')

try:
    while all_count < 777:
        user_number = input(f'Сумма всех чисел = {all_count}. Введите число: ')
        if user_number.isdigit():
            if 1 == random.randint(0, 13):
                raise SyntaxError

            out_file.write(user_number + '\n')
            all_count += int(user_number)

except SyntaxError:
    print('Вас постигла неудача!')

else:
    print('Вы успешно выполнили условие для выхода из порочного цикла!')

finally:
    out_file.close()
