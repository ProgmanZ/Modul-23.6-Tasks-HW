# Задача 6. Чат

# Программа состоит из файлов:
#   nickname.txt - содержит ник пользователя если ник уже был зарегистрирован
#   prefix.txt --- содержит первой строчкой режим работы "server" или "local",
#                           второй строкой сетевой или локальный путь к файлу chat_db.txt и nick_db.txt
#   chat_db.txt -- копия всего чата с сервера (перезаписывается в случае увеличения размера конечного)
#   nick_db.txt -- копия всех ников с сервера (перезаписывается в случае увеличения размера конечного)
#
# Пользователь запускает программу. Программа смотрит в локальном каталоге файл-признак prefix.txt клиент или сервер.
# Если программа не находит файл-признак сервера или клиента:
# Программа спрашивает режим работы программы: клиент или сервер(+ роль локального клиента) создает или читает файлы.
#
#   Если программа запущена в режиме сервера - программа формирует базу данных chat_db.txt в текущем каталоге, если его
#   не было ранее + создает файл ников nick_db.txt, если его не было ранее
#   в режиме сервера пользователю сообщается, что необходимо расшарить папку с файлами базы и ников с правами
#   чтение-запись
#
# Если программа работает в режиме клиента и не находит файл prefix.txt:
#   программа запрашивает строку сетевого адреса к файлам на компьютере сервера в локальной сети
#   программа проверяет наличие и сообщает результат нахождения обоих файлов.
# В случае нахождения файлов чата и ников программа запрашивает ник у пользователя (у клиента и сервера одинаково)
# Программа проверяет файл ника в локальном каталоге. Если она его находит, то ник не запрашивается:
# - проверяется наличие текстового файла с именем файла == нику в локальном каталоге программы
# - проверяется ник в общем файле ников на сервере
#   если ник который ввел пользователь есть в имени локального файла + в каталоге ников на сервере - ник присваивается
#   этому пользователю.
#   Если ник в каталоге (файле) на сервере присутствует, но отсутствует файл в локальном каталоге программы - выводится
#   сообщение, что ник занят.
#   В случае если ника нет ни в имени локального файла, ни в файле-каталоге ников на сервере - ник присваивается
#   текущему пользователю, так же создается запись в удаленном файле ников + создается локальный текстовый файл в
#   каталоге программы.
# При всех успешных начальных проверках, программа проверяет размеры файлов чатов и файлов ников
# В случае увеличения этих файлов - копирует к себе в каталог
#


import datetime
import os


def file_chat_db(path_to_db='current_server'):
    if path_to_db == 'current_server':
        list_dir = os.listdir()
        if 'chat_file.txt' not in list_dir:
            chat_file_db = open('chat_file.txt', 'w')
            chat_file_db.close()
            print('Файл чата создан', datetime.datetime.now())
            print('Этот ПК используется в качестве сервера.')
            print('Вам необходимо "расшарить" папку с программой и предоставить права (чтение/запись) к папке')
            print('Так же сообщите путь к этой папке другим участникам.')
    else:
        try:
            with open(path_to_db, 'r', encoding='utf-8'):
                print('Файл базы чата успешно найден.')
        except FileNotFoundError:
            print('Ошибка. Файл чата не найден.')


def check_nick_name(path_to_db):
    while True:
        with open('nick_db.txt', 'a+', encoding='utf-8') as nick_db_file:
            list_nick = nick_db_file.readlines()
            nick = input('Введите никнейм: ')
            if nick in list_nick:
                print('Такое имя пользователя уже занято..')
            else:
                nick_db_file.write(str(nick) + '\n')
                return nick


def check_work(list_dir):  # Заранее подать список файлов на вход dir_list = os.listdir()
    # Запускается и проверяется первым
    work_status = dict()
    if 'prefix.txt' in list_dir:
        with open('prefix.txt', 'r', encoding='utf-8') as prefix_file:
            line = prefix_file.read()
            if line == 'server' or line == 'client':
                work_status[line] = prefix_file.read()
                #   После проверки этой функции передать значение в функцию проверки фалйла ников
                #
                #
                #
            else:
                print('Ошибка в файле prefix.txt. Удалите файл и запустите программу заново. Файл будет пересоздан.')

    else:
        with open('prefix.txt', 'w', encoding='utf-8') as prefix_file:  # если файл префикса не найден.
            ask = str
            while ask != 'server' or ask != 'client':
                ask = input('Введите режим работы программы (server | client): ').lower()
            if ask == 'server':
                prefix_file.write('server\n')
                pass  # создание файлов для сервера
            else:
                prefix_file.write('client\n')
                pass  # создание файлов для клиента


def read_messages(path_to_db):
    with open(path_to_db, 'r') as chat:
        all_chat = chat.readlines()
        print(all_chat)


def write_messages(nick_name, path_to_db):
    with open(path_to_db, 'a') as chat:
        input_message = input(f'{nick_name} введите ваше сообщение: ')
        chat.write(str(datetime.datetime.now()))
        chat.write(f'|-[{nick_name}]\t')
        chat.write(str(input_message) + '\n')
