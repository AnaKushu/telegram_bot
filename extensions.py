import requests
import json
from config import keys

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            raise APIException(f'Валюта {quote} не найдена!')

        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f'Валюта {base} не найдена!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_key}&tsyms={base_key}')
        resp = json.loads(r.content)[base_key] * float(amount)

        return resp
