from db_utils import change_language


def get_index(data: list):
    try:
        current_index = int(input())
        return current_index
    except ValueError:
        print(f'Введите число от 1 до {len(data)}')
        get_index(data)


def check_settings(lang: str):
    if lang == 'ru':
        print('Результат по-умолчанию выводится на русском языке. Хотите изменить на английский? '
              'Введите ответ в формате Y/N')
        user_input = input()
        if user_input.lower() == 'y' or user_input.lower() == 'н':
            change_language('settings.db', 'en')
        elif user_input.lower() == 'n' or user_input.lower() == 'т':
            pass
        else:
            print('Введите ответ в формате "Y/N"')
    elif lang == 'en':
        print('Результат по-умолчанию выводится на английском языке. Хотите изменить на русский?')
        user_input = input()
        if user_input.lower() == 'y' or user_input.lower() == 'н':
            change_language('settings.db', 'ru')
        elif user_input.lower() == 'n' or user_input.lower() == 'т':
            pass
        else:
            print('Введите ответ в формате "Y/N"')
            check_settings(lang)
