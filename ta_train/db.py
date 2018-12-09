import mysql.connector

import click
from flask import current_app, g
from flask.cli import with_appcontext

from data import data_pro


def get_db():
  if 'db' not in g:
    g.db = mysql.connector.connect(
        host=current_app.config['DATABASE_HOST'],
        user=current_app.config['DATABASE_USER'],
        database=current_app.config['DATABASE']
    )

  return g.db


def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()

def init_db():
  db = get_db()
  cursor = db.cursor()

  with current_app.open_resource('schema.sql') as f:
    for statement in f.read().decode('utf8').split(';'):
      cursor.execute(statement)


@click.command('init-db')
@with_appcontext
def init_db_command():
  """Clear the existing data and create new tables."""
  init_db()
  click.echo('Initialized the database.')


@click.command('import-data')
@click.argument('filename')
@with_appcontext
def import_data(filename):
  if data_pro.import_data(get_db(), filename):
    click.echo('Data imported.')
  else:
    click.echo('Failed to import data.')


@click.command('import-variety')
@click.argument('filename')
@with_appcontext
def import_variety(filename):
  if data_pro.import_variety(get_db(), filename):
    click.echo('Variety imported.')
  else:
    click.echo('Failed to import variety.')


def init_app(app):
  app.teardown_appcontext(close_db)
  app.cli.add_command(init_db_command)
  app.cli.add_command(import_data)
  app.cli.add_command(import_variety)