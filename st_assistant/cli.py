import click
import pprint

from flask import Flask, g
from flask.cli import with_appcontext

from st_assistant.data import stock_pos_loader
from st_assistant.data import stock_price_loader

@click.command('load-price')
@with_appcontext
def load_price():
  """Command line for loading prices."""
  click.echo('Starts loading prices.')
  loader = stock_price_loader.SinaStockPriceLoader()
  prices = loader.load(['sh600928', 'sz002307'])
  print(prices)


@click.command('load-pos')
@with_appcontext
def load_pos():
  click.echo('Starts loading stock pos.')
  loader = stock_pos_loader.StockPosLoader()
  loader.load()


def init_app(app):
  app.cli.add_command(load_price)
  app.cli.add_command(load_pos)