# Задача 4. Регистрация

def check_data(input_string):
    input_string = input_string.strip().split(' ')
    if len(input_string) < 3:
        raise IndexError
    elif not input_string[0].isalpha():
        raise NameError
    elif not ('@' and '.' in input_string[1][input_string[1].index('@'):]):
        raise SyntaxError
    elif input_string[-1].isalpha():
        raise ValueError
    elif not(10 < int(input_string[-1]) < 100):
        raise ValueError
    else:
        return None


with open('registrations.txt', 'r', encoding='utf-8') as input_file_reg, \
        open('registrations_bad.log', 'a', encoding='utf-8') as bad_log_file,\
        open('registrations_good.log', 'a', encoding='utf-8') as good_log_file:

    for line in input_file_reg:
        try:
            check_data(line)

        except IndexError:
                bad_log_file.write(f'{line.strip()}\tНЕ присутствуют все три поля.\n')

        except NameError:
                bad_log_file.write(f'{line.strip()}\tПоле имени содержит НЕ только буквы.\n')

        except SyntaxError:
                bad_log_file.write(f'{line.strip()}\tПоле «Имейл» НЕ содержит @ или .(точку).\n')

        except ValueError:
            bad_log_file.write(f'{line.strip()}\tПоле «Возраст» НЕ является числом от 10 до 99.\n')

        else:
            good_log_file.write(line)
