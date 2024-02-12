from data import get_currency

class APIException(Exception):                                              #собственный класс исключений
    pass

class Converter:
    @staticmethod
    def convert(amount, cur1, cur2):                                       # класс исключений проверяющий корректность введенных пользователем данных
        cl = get_currency()
        if cur1 == cur2:
            raise APIException(f'Валюты одинаковы {cur1}')
        if cur1 not in cl.keys():
            raise APIException(f'Валюты {cur1} нет среди доступных.')
        if cur2 not in cl.keys():
            raise APIException(f'Валюты {cur2} нет среди доступных.')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')
        return cl