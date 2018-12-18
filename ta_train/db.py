import click

from flask import current_app, g
from flask.cli import with_appcontext

from data import data_pro

from ta_train.db_model import DB
from ta_train.mock_db_model import MockDB


def get_db():
  if 'db' not in g:
    if current_app.config['DATABASE_TYPE'] == 'mock':
      g.db = MockDB()
    else:
      g.db = DB(current_app.config)

  return g.db


def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()


def init_db():
  db = get_db()

  sql_schema = 'schema.sql' if db.type == 'mysql' else 'sqlite-schema.sql'
  with current_app.open_resource(sql_schema) as f:
    for statement in f.read().decode('utf8').split(';'):
      db.execute(statement)


@click.command('init-db')
@with_appcontext
def init_db_command():
  """Clear the existing data and create new tables."""
  init_db()
  close_db()
  click.echo('Initialized the database.')


@click.command('import-data')
@click.argument('filename')
@with_appcontext
def import_data(filename):
  if data_pro.import_data(get_db(), filename):
    click.echo('Data imported.')
  else:
    click.echo('Failed to import data.')
  close_db()


@click.command('import-variety')
@click.argument('filename')
@with_appcontext
def import_variety(filename):
  if data_pro.import_variety(get_db(), filename):
    click.echo('Variety imported.')
  else:
    click.echo('Failed to import variety.')
  close_db()


def init_app(app):
  app.teardown_appcontext(close_db)
  app.cli.add_command(init_db_command)
  app.cli.add_command(import_data)
  app.cli.add_command(import_variety)