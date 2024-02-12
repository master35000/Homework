import requests
import json

TOKEN = "6704658609:AAHYjAeepWCNNVO6KTtmO5AS5pj2IMvuBCI"            # Токен бота


def get_currency ():                                                        # функция запроса курсов валют через API и приведение в нужный вид
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'                      # ссылка для запроса
    r = json.loads(requests.get(url).content)['Valute']                     # запрос данных и преобразование в словарь
    for i in r.values():  # форматирование данных по валютам
        del i['ID']
        del i['NumCode']
        del i['Previous']
        del i['CharCode']
    r['RUB'] = {'Nominal': 1, 'Name': 'Российский Рубль', 'Value': 1}       # добавление валюты RUB
    r = dict(sorted(r.items()))                                             # сортировка словаря по ключам
    return r

def currency_name_list(cur):                                                # функция формирующая список доступных валют
    text= ''
    for key, value in cur.items():
        text+= f"{key} -  {value['Name']}\n"
    return(text)