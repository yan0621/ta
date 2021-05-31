import click
import pprint

from flask import Flask, g
from flask.cli import with_appcontext

from st_assistant import stock_analyzer
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
  pos = loader.load()
  print(pos)

@click.command('analyze')
@with_appcontext
def analyze():
  pos_loader = stock_pos_loader.StockPosLoader()
  pos = loader.load()
  stock_ids = [p.stock_id for p in pos]
  price_loader = stock_price_loader.SinaStockPriceLoader()
  prices = price_loader.load(stock_ids)
  analyzer = stock_analyzer.Analyzer(pos, prices)


def init_app(app):
  app.cli.add_command(load_price)
  app.cli.add_command(load_pos)