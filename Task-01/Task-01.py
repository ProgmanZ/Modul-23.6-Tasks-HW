# Задача 1. Имена 2

import datetime

number_string = 0
all_symbols_sum = 0

with open('people.txt', 'r', encoding='utf-8') as input_file:
    for line in input_file:
        number_string += 1
        try:
            len_string = len(line.strip('\n'))
            all_symbols_sum += len_string
            if len_string < 3:
                raise SyntaxError

        except SyntaxError:
            print(f'Ошибка: менее трёх символов в строке {number_string}!')
            with open('errors.log', 'a', encoding='utf-8') as error_file:
                error_file.write(f'{str(datetime.datetime.now())}\t')
                error_file.write(f'Ошибка: менее трёх символов в строке {number_string}!\n')

    print(f'Общее количество символов:{all_symbols_sum}.')



