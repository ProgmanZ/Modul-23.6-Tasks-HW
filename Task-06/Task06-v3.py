import os
import datetime
# \\MainPC\test_chat_project

main_files = ('mode.txt', 'settings.txt', 'username.txt', 'nicks.txt', 'chat.txt')
status = {key: False for key in main_files}


def enter_mode():
    # Установка режима работы программы server или client

    while True:
        mode_flag = input('Введите режим работы (1 - server или 2 - client): ')
        if mode_flag in ('1', '2'):
            return 'server' if mode_flag == '1' else 'client'
        else:
            print('Введена неверная комбинация. Допустимые значения 1 или 2. ')


def enter_file_creation(file_name):
    # Информирует пользователя об отсутствии файлов
    # Запрашивает у пользователя необходимость создания файлов.
    # Возвращает True или False

    print(f'Файл {file_name} не найден в каталоге программы.')
    while True:
        answer = input('Создать файл (да, нет)?').lower()
        if answer == 'да':
            return True
        elif answer == 'нет':
            return False
        else:
            print('Введен неверный ответ. Допустимые значения ответа "да" или "нет"..')


def username_check_enter(path_to_file_db):
    # создание файла username.txt проверка имени в БД ников nicks.txt
    # Вызывается из функции создания файлов create_file

    while True:
        name = input('Введите желаемое имя пользователя: ')
        with open(os.path.join(path_to_file_db, 'nicks.txt'), 'a+', encoding='utf-8') as file:
            names = file.readlines()
            if name not in names:
                file.write(f'{name} {datetime.datetime.now()}\n')
                return name
            else:
                print('Введенное имя пользователя уже используется. Попробуйте выбрать другое.')


def create_file(create_file_name, dict_files_status, path_to_file, prog_mode, username=None):
    # Создание необходимых файлов

    if create_file_name == 'settings.txt':
        # Отсутствует файл содержащий путь к серверу файлов

        with open(os.path.join(path_to_file, 'settings.txt'), 'w', encoding='utf-8') as file:
            file.write(f'{str(path_to_file)}')

    elif create_file_name == 'mode.txt':
        # Отсутствует файл работы режима программы

        with open(os.path.join(path_to_file, 'mode.txt'), 'w', encoding='utf-8') as file:
            file.write(f'{prog_mode}')

    elif create_file_name == 'nicks.txt':
        # БД ников не существовало на сервере

        with open(os.path.join(path_to_file, 'nicks.txt'), 'w', encoding='utf-8') as file:
            file.write(f'*** [{datetime.datetime.now()}] Файл создан пользователем {username}. *** \n')
            file.write(f'{username} {datetime.datetime.now()}\n')

    elif create_file_name == 'username.txt':
        # пользователь утратил файл с его именем или запускает программу впервые
        # файл должен быть у каждого клиента локальный свой

        username = username_check_enter(path_to_file)  # проверка на существование имени в БД ников
        with open('username.txt', 'w', encoding='utf-8') as file_username:
            file_username.write(f'{username} {datetime.datetime.now()}')

    elif create_file_name == 'chat.txt':
        # Отсутствует файл с чатом
        with open(os.path.join(path_to_file, 'chat.txt'), 'w', encoding='utf-8') as file:
            file.write(f'*** [{datetime.datetime.now()}] Файл создан пользователем {username}. *** \n')
        dict_files_status['chat.txt'] = True

    else:
        # ошибка при создании файлов
        print('В программе произошла ошибка при создании файлов')


def check_files_prog(mode, dict_file_status, works_files_list):
    # Проверка сетевого пути к файлам
    # Проверка наличия всех файлов, при отсутствии - создание

    path_to_files = input('Введите полный сетевой путь к каталогу программы на сервере: ')
    if not os.path.exists(path_to_files):
        print('Вы ввели путь, который не существует в сети.')
    else:
        list_entered_dir = os.listdir(path_to_files)
        lost_files = list()

        for file in works_files_list:
            if file in list_entered_dir:
                if file == 'username.txt' and mode == 'client':
                    if os.path.isfile('username.txt'):  # Проверка наличия локального файла
                        dict_file_status[file] = True
                    else:
                        create_file(file, dict_file_status, path_to_files, mode)

            else:
                if enter_file_creation(file):
                    create_file(file, dict_file_status, path_to_files, mode)   # функция создания файлов пользователей
                else:
                    lost_files.append(file)
        if len(lost_files):
            print('Программа не сможет работать без следующих файлов:')
            for file_name in lost_files:
                print(f'\t{file_name}')
            print(f'Попробуйте найти эти файлы у других участников и '
                  f'скопировать эти файлы на сервер по пути{path_to_files}.')
            return False

        return True


work_mode = enter_mode()
live_status = check_files_prog(work_mode, status, main_files)