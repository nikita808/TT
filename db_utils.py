import sqlite3


def select_all_tasks(db_file: str):
    query = 'select * from settings'
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query)

    result = [dict(row) for row in c.fetchall()]
    return result.pop()


def create_db(db_file: str):
    print('Введите ключ доступа API')
    API_KEY = input()
    create_query = f'''CREATE TABLE settings (
    default_url TEXT (255),
    API_KEY     TEXT (255),
    language    TEXT (20)
);'''
    insert_query = f'''INSERT INTO settings (default_url, API_KEY, language) values 
        ("https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address",
         "{API_KEY}", "ru");'''
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(create_query)
    c.execute(insert_query)
    conn.commit()
    c.close()


def change_language(db_file: str, lang: str):
    change_lang_query = f'''
    update settings set language = "{lang}";
    '''
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(change_lang_query)
    conn.commit()
    c.close()


def change_api_key(db_file: str, new_api_key: str):
    change_api_key_query = f'''
        update settings set API_KEY = "{new_api_key}";
        '''
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(change_api_key_query)
    conn.commit()
    c.close()


def change_settings(lang: str):
    print('Выберите настройки, которые хотите изменить: \n'
          '1. Изменить язык ответов\n'
          '2. Изменить API_KEY')
    user_input = input()
    if user_input == '1':
        if lang == 'ru':
            change_language('settings.db', 'en')
            print('Язык успешно изменен на английский')
            return 'en'
        elif lang == 'en':
            change_language('settings.db', 'ru')
            print('Язык успешно изменен на русский')
            return 'ru'
    elif user_input == '2':
        print('Введите новый ключ доступа API')
        new_api_key = input()
        change_api_key('settings.db', new_api_key=new_api_key)
        print('Новый ключ доступа API успешно установлен')
        return lang
    else:
        change_settings(lang)
        print('Введите корректный ответ')
