import os
import datetime
import asyncio
import time
from collections import deque
import keyboard


def enter_mode():  # Установка режима работы программы server или client

    while True:
        mode_flag = input('Введите режим работы (1 - server или 2 - client): ')
        if mode_flag in ('1', '2'):
            return 'server' if mode_flag == '1' else 'client'
        else:
            print('Введена неверная комбинация. Допустимые значения 1 или 2. ')


def username_check_is_busy_or_create(path_to_file_db):
    # создание файла username.txt проверка имени в БД ников nicks.txt
    # Вызывается из функции создания файлов create_file

    while True:

        name = input('Введите желаемое имя пользователя: ')
        if name in '/+-\'\n!\\#@$., %^&*()':
            print(f'Имя не может содержать такое имя как {name}.')
            continue

        if os.path.isfile(os.path.join(path_to_file_db, 'nicks.txt')):
            names_list = dict()
            with open(os.path.join(path_to_file_db, 'nicks.txt'), 'r+', encoding='utf-8') as file:
                file.readline()  # пропуск чтения первой строки в файле. В ней указывается кем создан файл.
                for line in file:
                    line = line.strip().split()
                    names_list[line[0]] = line[1]
                if name in names_list.keys():
                    print(f'Имя пользователя {name} уже используется.\n '
                          f'Имя пользователя зарегистрировано {names_list[name]}.\n'
                          f'Попробуйте придумать другое имя.')

                else:

                    time_now = datetime.datetime.now()
                    file.write(f'{name} {time_now.strftime("%d/%m/%Y--%H:%M:%S")}\n')
                    print(f'Имя пользователя {name} успешно зарегистрировано.\n'
                          f'Имя пользователя зарегистрировано {time_now.strftime("%d/%m/%Y--%H:%M:%S")}.')
                    return name

        else:
            with open(os.path.join(path_to_file_db, 'nicks.txt'), 'w', encoding='utf-8') as file:
                time_now = datetime.datetime.now()
                file.write(f'*** [{time_now.strftime("%d/%m/%Y--%H:%M:%S")}] Файл создан пользователем {name}. *** \n')
                file.write(f'{name} {time_now.strftime("%d/%m/%Y--%H:%M:%S")}\n')
                return name


def search_keys_in_setting(search_word):
    with open('settings.txt', 'r', encoding='utf-8') as setting_file:
        for line in setting_file:
            line = line.strip().split(' ')
            if line[0] == search_word:
                return line[1]
        return 0


def create_file(file_name_for_create, prog_mode, path_to_file=None):
    # Создание необходимых файлов

    if file_name_for_create == 'settings.txt':
        # Отсутствует локальный файл содержащий путь к серверу файлов
        # \\MainPC\test_chat_project

        with open('settings.txt', 'w', encoding='utf-8') as file:
            share = check_share()
            username = username_check_is_busy_or_create(share)
            file.write(f'server {str(share)}\n')
            file.write(f'mode {prog_mode}\n')
            file.write(f'nickname {username}\n')
            time_now = datetime.datetime.now()
            file.write(f'created {time_now.strftime("%d/%m/%Y--%H:%M:%S")}')

    elif file_name_for_create == 'nicks.txt':
        # отсутствует файл ников на сервере

        name = search_keys_in_setting('nickname')
        share_url = search_keys_in_setting('server')

        with open(os.path.join(share_url, 'nicks.txt'), 'w', encoding='utf-8') as file:
            time_now = datetime.datetime.now()
            file.write(f'*** [{time_now.strftime("%d/%m/%Y--%H:%M:%S")}] Файл создан пользователем {name}. *** \n')
            file.write(f'{name} {time_now.strftime("%d/%m/%Y--%H:%M:%S")}\n')

    elif file_name_for_create == 'chat.txt':
        # Отсутствует файл с чатом на сервере

        username = search_keys_in_setting('nickname')
        time_now = datetime.datetime.now()
        with open(os.path.join(path_to_file, 'chat.txt'), 'w', encoding='utf-8') as file:
            file.write(f'*** [{time_now.strftime("%d/%m/%Y--%H:%M:%S")}] Файл создан пользователем {username}. *** \n')

    else:
        print('Поступил запрос на создание неизвестного файла')


def check_share(path_to_share=None):
    # Проверка доступа к сетевому каталогу программы
    # возвращает сетевой путь
    # \\MainPC\test_chat_project

    while True:
        if path_to_share is None:
            path_to_share = input('Введите полный сетевой путь к каталогу программы на сервере : ')
        if not os.path.exists(path_to_share) or not path_to_share.startswith('\\'):
            print('Ошибка. Путь не существует в сети...')
            path_to_share = None
        else:
            return path_to_share


def check_files_prog(mode):
    # Проверка наличия всех файлов, при отсутствии - создание
    # режим работы клиента
    # - проверить файлы на сервере: 'nicks.txt' и 'chat.txt'- проверить
    # - проверить локальные файлы: 'mode.txt', 'settings.txt', 'username.txt'

    list_client_dir = os.listdir(os.getcwd())

    if 'settings.txt' not in list_client_dir:
        create_file('settings.txt', mode)

    setting_db = dict()
    with open('settings.txt', 'r', encoding='utf-8') as setting:
        for line in setting:
            line = line.strip().split(' ')
            if len(line) == 2:
                setting_db[line[0]] = line[1]
            else:
                print('Ошибка.')
                print(f'Строка {line} в файле settings.txt')
                return None

    server_url = setting_db.get('server', None)

    if server_url is None:
        print('Ошибка в файле settings.txt. Неверный параметр в значении "server"')
        ask = input('Желаете пересоздать файл settings.txt? (да или нет)? : ').lower()
        if ask == 'да':
            create_file('settings.txt', mode)
        return check_files_prog(mode)
    else:
        list_server_dir = os.listdir(server_url)

        if 'chat.txt' not in list_server_dir:
            print('Файл чата не найден. Создаю..')
            create_file('chat.txt', mode, server_url)

        if 'nicks.txt' not in list_server_dir:
            print('Файл ников не найден. Создаю..')
            create_file('nicks.txt', mode, server_url)

        else:
            print('Пройдена проверка файлов')

        return setting_db


def print_chat(userdata):
    key = 'a'
    while True:

        with open(os.path.join(userdata['server'], 'chat.txt'), 'r', encoding='utf-8') as file_chat:
            for row in deque(file_chat, 10):
                print(row.strip())
        enter_user = input(f'{"*"*30}\nВведите 1, если хотите ввести сообщение. \n'
                           'Введите [q] если хотите выйти из программы.\n'
                           'Для продолжения нажмите любую клавишу.')
        if '1' == enter_user:

            with open(os.path.join(userdata['server'], 'chat.txt'), 'a', encoding='utf-8') as enter_chat:
                message = input(f'{userdata["nickname"]} введите сообщение:')
                time_now = datetime.datetime.now()
                enter_chat.write(f'[{time_now.strftime("%d/%m/%Y %H:%M:%S")}] {userdata["nickname"]}: {message}\n')

        elif '[q]' == enter_user:
            break
        else:
            continue

#
# async def enter_message_chat(userdata_dict):
#     while True:
#         try:
#             file = open(os.path.join(userdata_dict['server'], 'chat.txt'), 'a', encoding='utf-8')
#             time_now = datetime.datetime.now()
#             message = input(f'{userdata_dict["username"]} введите сообщение:')
#             file.write(f'[{time_now.strftime("%d/%m/%Y %H:%M:%S")}] {userdata_dict["username"]}: {message}\n')
#         except IOError:
#             continue
#         await asyncio.sleep(3.0)


# async def start(dict_userdata):
#     coroutines = list()
#     coroutines.append(asyncio.create_task(print_chat(dict_userdata)))
#     # coroutines.append(asyncio.create_task(enter_message_chat(dict_userdata)))
#     await asyncio.wait(coroutines)


live_status = False
work_mode = enter_mode()
user_data = check_files_prog(work_mode)
if user_data is not None:
    print('ОК. Поехали дальше')

else:
    print('Ошибка!')

print_chat(user_data)
# asyncio.run(start(user_data))
