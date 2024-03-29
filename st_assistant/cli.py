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
  pos_loader = stock_pos_loader.StockPosLoader()
  pos = pos_loader.load()
  stock_ids = [p.id for p in pos]
  price_loader = stock_price_loader.SinaStockPriceLoader()
  price_loader.loadToFile(stock_ids)

@click.command('load-pos')
@with_appcontext
def load_pos():
  click.echo('Starts loading stock pos.')
  loader = stock_pos_loader.StockPosLoader()
  pos = loader.load()
  print(pos)

@click.command('analyze')
@click.option('--cash')
@with_appcontext
def analyze(cash):
  pos_loader = stock_pos_loader.StockPosLoader()
  pos = pos_loader.load()
  stock_ids = [p.id for p in pos]
  price_loader = stock_price_loader.SinaStockPriceLoader()
  prices = price_loader.loadFromDataFile()
  analyzer = stock_analyzer.Analyzer(pos, prices, int(cash))
  actions = analyzer.run()
  for action in actions:
    print(action)

@click.command('offset')
@with_appcontext
def offset():
  pos_loader = stock_pos_loader.StockPosLoader()
  pos = pos_loader.load()
  stock_ids = [p.id for p in pos]
  price_loader = stock_price_loader.SinaStockPriceLoader()
  prices = price_loader.loadFromDataFile()
  analyzer = stock_analyzer.Analyzer(pos, prices)
  offsets = analyzer.runOffset()
  for offset in offsets:
    print(offset)
  

def init_app(app):
  app.cli.add_command(load_price)
  app.cli.add_command(load_pos)
  app.cli.add_command(analyze)
  app.cli.add_command(offset)