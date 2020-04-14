import datetime
from forex_python.converter import CurrencyRates, CurrencyCodes, RatesNotAvailableError
from config import WRITE_HISTORY_MODE
from src.history import write_history


'''
Обертка над форексовской функцией конвертации
'''
def convert_currency(source_ticker: str, target_ticker: str, amount, date=None):
    c = CurrencyRates()
    try:
        result = c.convert(source_ticker, target_ticker, amount, date)
    except RatesNotAvailableError as error:
        return error.__str__
    else:
        if WRITE_HISTORY_MODE:
            rate = str(c.get_rate(source_ticker, target_ticker, date))

            # Если делаем конвертацию по историческому курсу
            # то добавляем дату этого курса
            if date:
                rate += str(f" (исторический на {date.strftime('%d %B %Y')})")

            write_history(source_ticker, target_ticker, amount, rate, result)
        return result

'''
И еще одна обертка, чтобы было проще брать значок валюты
'''
def get_currency_symbol(ticker: str):
    c = CurrencyCodes()
    return c.get_symbol(ticker)