import re
import datetime
import click
from src.convert import convert_currency, get_currency_symbol
from src.validate import validate_ticker, validate_amount, validate_date
from src.history import get_history


@click.group()
def cli():
    pass

@click.command()
@click.option('--src', required=True, callback=validate_ticker, prompt='Обозначение исходной валюты')
@click.option('--trg', required=True, callback=validate_ticker, prompt='Обозначение целевой валюты')
@click.option('--amount', required=True, callback=validate_amount, prompt='Укажите сумму для конвертации')
@click.option('--date', required=False, callback=validate_date, help='Дата в формате YYYY-MM-DD')
def convert(src, trg, amount, date=None):
    result = convert_currency(src, trg, float(amount), date=date)
    click.echo(f'Вы получите: {result} {get_currency_symbol(trg)}')

@click.command()
def history():
    get_history()

cli.add_command(convert)
cli.add_command(history)

if __name__=='__main__':
    cli()