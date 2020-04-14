import re
import datetime
import click
from click.exceptions import BadParameter
from forex_python.converter import CurrencyCodes


'''
Валидация введенного тикера на корректность
'''
def validate_ticker(ctx, param, value):
    try:
        if re.fullmatch(r"^[A-Z]{3}$", value):         # Проверяем соответствует ли тикер формату
            c = CurrencyCodes()
            if c.get_currency_name(value):             # Если можем получить название по тикеру
                return value                           # то выходим, иначе бросаем эксепшн
            else:
                raise BadParameter('такого тикера нет')
        else:
            raise BadParameter('тикер не соответствует формату ААА')
    except BadParameter as error:                      # В случае ошибки
        click.echo(f'Ошибка: {error}')                 # выводим ее
        value = click.prompt(param.prompt)             # и делаем магию с колбэками
        return validate_ticker(ctx, param, value)      # которую возвращаем обратно

'''
Валидация суммы конвертации
'''
def validate_amount(ctx, param, value):
    try:
        if re.fullmatch(r"^\d+(\d*|\.?\d+)$", value):
            return value
        else:
            raise BadParameter('некорректное число для перевода')
    except BadParameter as error:
        click.echo(f'Ошибка: {error}')
        value = click.prompt(param.prompt)
        return validate_amount(ctx, param, value)

'''
Валидация даты для конвертации по историческому курсу
'''
def validate_date(ctx, param, value):
    if value:
        result = re.match(r"(\d{4})-(\d{2})-(\d{2})", value)
        try:
            assert(len(result.groups()) == 3)
            dt = datetime.datetime(year=int(result.groups()[0]), \
                                    month=int(result.groups()[1]), \
                                    day=int(result.groups()[2]))
        except AssertionError:
            click.echo('Не получилось спарсить дату, использую текущую')
            return None
        except ValueError:
            click.echo('Некорректная дата, будет использована текущая')
            return None
        else:
            return dt
    else: 
        return None