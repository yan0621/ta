import mysql.connector
import sqlite3


class DB(object):
  
  def __init__(self, config):
    self.type = config['DATABASE_TYPE']
    if self.type == 'mysql':
      self._db = self._create_mysql_db(
          host=config['DATABASE_HOST'],
          user=config['DATABASE_USER'],
          database=config['DATABASE']
      )
    elif self.type == 'sqlite':
      self._db = self._create_sqlite_db(config['DATABASE'])
    else:
      raise Exception('Unsupported db type %s!' % self._type)

  def _create_mysql_db(self, host, user, database):
    return mysql.connector.connect(
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
    if self.type == 'mysql':
      cursor = self._db.cursor()
      cursor.execute(sql)
      return cursor.fetchall()
    elif self.type == 'sqlite':
      return self._db.execute(sql).fetchall()
  
  def batch_execute(self, sql_list):
    '''Executes a list of sqls.'''
    if self.type == 'mysql':
      cursor = self._db.cursor()
      for sql in sql_list:
        cursor.execute(sql)
      self._db.commit()
    elif self.type == 'sqlite':
      for sql in sql_list:
        self._db.execute(sql)
      
  def execute_script(self, content):
    '''Executes a string content containing multiple sqls.'''
    if self.type == 'mysql':
      pass
    elif self.type == 'sqlite':
      pass
  
  def close(self):
    if self._db is not None:
      self._db.close()
