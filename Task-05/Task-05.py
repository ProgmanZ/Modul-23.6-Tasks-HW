# Задача 5. Текстовый калькулятор

def check_string_file(input_string):
    input_string = input_string.strip().split(' ')

    if len(input_string) < 3:
        raise IndexError

    elif input_string[1] not in ('//', '/', '*', '-', '+', '**', '%'):
        raise ArithmeticError

    elif input_string[1] == '/' and int(input_string[-1]) == 0:
        raise ZeroDivisionError

    elif not(input_string[0].isdigit()) or not(input_string[-1].isdigit()):
        raise ValueError

    else:
        return input_string


def calc_actions(input_action):

    match input_action[1]:

        case '//':
            action = int(input_action[0]) // int(input_action[-1])
        case '/':
            action = int(input_action[0]) / int(input_action[-1])
        case '*':
            action = int(input_action[0]) * int(input_action[-1])
        case '-':
            action = int(input_action[0]) - int(input_action[-1])
        case '+':
            action = int(input_action[0]) + int(input_action[-1])
        case '**':
            action = int(input_action[0]) ** int(input_action[-1])
        case '%':
            action = int(input_action[0]) % int(input_action[-1])
        case _:
            action = 0
    return action


all_sum_actions = 0

with open('calc.txt', 'r') as input_file:
    for line in input_file:
        try:
            all_sum_actions += calc_actions(check_string_file(line))

        except (IndexError, ValueError, NameError, ZeroDivisionError, ArithmeticError):
            print(f'Обнаружена ошибка в строке:{line}', end='\t')
            ask = input('Хотите исправить (да/нет)?')

            if 'да' == ask.lower():
                user_input_string = input('Введите исправленную строку:')
                all_sum_actions += calc_actions(check_string_file(user_input_string))

    print('Сумма результатов:', all_sum_actions)
