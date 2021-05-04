import click
import pprint

from flask import Flask, g
from flask.cli import with_appcontext

@click.command('auto')
@with_appcontext
def auto_command():
  """Command line auto running."""
  click.echo('Auto starts running.')


def init_app(app):
  app.cli.add_command(auto_command)