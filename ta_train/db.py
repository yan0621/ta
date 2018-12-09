import click
import mysql.connector
import sqlite3

from flask import current_app, g
from flask.cli import with_appcontext

from data import data_pro


class DB(object):
  
  def __init__(self, config):
    self.type = config['DATABASE_TYPE']
    if self._type == 'mysql':
      self._db = self._create_mysql_db(
          host=config['DATABASE_HOST'],
          user=config['DATABASE_USER'],
          database=config['DATABASE']
      )
    elif self._type == 'sqlite':
      self._db = self._create_sqlite_db(config['DATABASE'])
    else:
      raise Exception('Unsupported db type %s!' % self._type)

  def _create_mysql_db(self, host, user, database):
    return mysql.connector.connect(host
        host=host,
        user=user,
        database=database
    )
    
  def _create_sqlite_db(self, database):
    db = sqlite3.connect(
        database,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row
    return db

  def execute(self, sql):
    '''Executes a single sql.'''
    if self.type == 'mysql':
      self._db.cursor().execute(sql)
      self._db.commit()
    elif self.type == 'sqlite':
      self._db.execute(sql)
  
  
  def execute_and_fetch(self, sql):
    '''Executes a single sql and returns query results.'''
    pass
  
  def batch_execute(self, sql_list):
    '''Executes a list of sqls.'''
    pass
    
  def execute_script(self, content):
    '''Executes a string content containing multiple sqls.'''
    pass
    
  def close():
    if _db is not None:
      _db.close()


def get_db():
  if 'db' not in g:
    g.db = DB(current_app.config)

  return g.db


def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()


def init_db():
  db = get_db()

  with current_app.open_resource('schema.sql') as f:
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