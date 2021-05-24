import click
import pprint

from flask import Flask, g
from flask.cli import with_appcontext

from st_assistant.data import stock_price_loader

@click.command('load-price')
@with_appcontext
def auto_command():
  """Command line for loading prices."""
  click.echo('Starts loading prices.')
  loader = stock_price_loader.SinaStockPriceLoader()
  loader.load(['sh600928', 'sz002307'])


def init_app(app):
  app.cli.add_command(auto_command)