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
    print('Введите API_KEY')
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
