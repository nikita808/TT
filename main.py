import os
import sys
import requests

from db_utils import select_all_tasks, create_db, change_settings
from helpers import check_settings, get_index

if not os.path.isfile('settings.db'):
    create_db('settings.db')
    settings = select_all_tasks('settings.db')
    check_settings(settings['language'])

settings = select_all_tasks('settings.db')

is_used = True
token = settings['API_KEY']
url = settings['default_url']
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f"Token {token}",
}

language = settings["language"]
while is_used:
    print('Введите желаемый адрес либо "0", если хотите изменить настройки: \n')
    inp = input()
    if inp == '0':
        language = change_settings(language)
    else:
        address = f'{{"query": "{inp}", "language": "{language}"}}'.encode('utf-8')

        res = requests.post(url, data=address, headers=headers).json().get('suggestions')
        if res:
            if len(res) > 1:
                print('Выберите нужный вам вариант либо введите "0", если хотите закрыть программу: \n')
                for ad in res:
                    index = res.index(ad) + 1
                    print(f"{index}: {ad['value']}")

                wanted_address_index = get_index(res)
                if wanted_address_index == 0:
                    sys.exit(0)
                else:
                    wanted_address_index -= 1
                    wanted_address = res[wanted_address_index]
                    print(f'\n{wanted_address.get("value")}, '
                          f"Широта: {wanted_address.get('data').get('geo_lat')},"
                          f" Долгота: {wanted_address.get('data').get('geo_lon')} ")
            else:
                print(f'\nПо вашему запросу найден один вариант: {res[0].get("value")}, '
                      f'Широта: {res[0].get("data").get("geo_lat")}, '
                      f'Долгота: {res[0].get("data").get("geo_lon")}')
        else:
            print('По вашему запросу не найдено адресов')
        print('\nПродолжить использование программы? Введите ответ в формате Y/N')
        user_input = input()
        if user_input.lower() == 'y' or user_input.lower() == 'н':
            pass
        elif user_input.lower() == 'n' or user_input.lower() == 'т':
            is_used = False
        else:
            print('Введите ответ в формате "Y/N"')
