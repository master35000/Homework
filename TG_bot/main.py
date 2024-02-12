import telebot
from data import TOKEN
from extensions import APIException
from extensions import Converter
from data import get_currency, currency_name_list

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])   # Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
def send_start_help(message):
    text = ('Для получения курса рубля к доступным валютам введите команду /rub_rate.\n\n'
            'Для получения кросс курса валют введите: количество валюты, тикер валюты, тикер'
            ' валюты в которую нужно перевести, например - 100 USD EUR.\n\nДля получения списка доступных '
            'валют введите команду /values\n\nДля вызова справки введите команду /help' )
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])    # Обрабатываются все сообщения, содержащие команды '/values'
def send_values(message):
    text = str(currency_name_list(get_currency()))          # формирование списка доступных валют с помощью импортированных функций
    bot.send_message(message.chat.id, text)                 # отправка списка валют в телеграмм

@bot.message_handler(commands=['rub_rate'])    # Обрабатываются все сообщения, содержащие команды '/rub_rate'
def send_values(message):
    text=''
    cur = get_currency()                        # запрос курсов валют
    del cur['RUB']
    for key, value in cur.items():              # выборка нужных данных
        text+= f"{key} - {value['Name']} -  {value['Value']} руб за {value['Nominal']} {key} \n"
    bot.send_message(message.chat.id, text)     # отправка сформированного сообщения в телеграмм

@bot.message_handler(content_types=['text'])     # Обработываются входящие сообщения
def convert(message: telebot.types.Message):
    try:
        if len(message.text.split(' ')) != 3:                               # Проверка введенного текста на соответствие условиям
            raise APIException('Запрос не удовлетворяет требованиям')        # Вызов исключения
        amount, cur1, cur2 = message.text.split(' ')                         # формирование данных от пользователя для обработки
        amount = amount.replace(',','.')                                     # замена запятой на точку в количестве валюты
        cur1, cur2 = cur1.upper(), cur2.upper()                                           # перевод тикеров в верхний регистр
        cl=Converter.convert(amount, cur1, cur2)                             # проверка и обработка данных пользователя, в случае успеха возврат данных полученных через API хапрос
    except APIException as e:                                                # вызов исключения в случае неудачи
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:                                                                   # в случае успеха вычисление кросс курса валют и отправка сообщения в телеграмм
        ex_rate = ((float(amount) / float(cl.get(cur1)['Nominal']) * float(cl.get(cur1)['Value'])) / float(cl.get(cur2)['Value'])) * float(cl.get(cur2)['Nominal'])
        text = f'Кросс курс {cur1}/{cur2} за {amount} {cur1} сотавляет {round(ex_rate, 4)} {cur2}'
        bot.reply_to(message, text)

bot.polling(none_stop=True)            # старт бота