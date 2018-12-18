from datetime import datetime
import os
import re

from flask import current_app

FILENAME_SEP = '[_\\.]'

app = current_app


def import_variety_line(db, vline):
  tokens = vline.split(',')
  sql = 'select id from Variety where type = "%s" and exchange = "%s" and name = "%s" and code="%s"' % (tokens[0], tokens[1], tokens[2], tokens[3])
  data_id = db.execute_and_fetch(sql)[0]
  if data_id:
    app.logger.warn('conflict variety record: %s', tokens)
    return False
  else:
    sql = 'insert into Variety (type, exchange, name, code) values (%s, %s, %s, %s)' % (tokens[0], tokens[1], tokens[2], tokens[3])
    db.execute(sql)
    return True


def import_variety(db, filename):
  try:
    count = 0
    with open(filename) as f:
      lines = f.readlines()
      for line in lines:
        if import_variety_line(db, line):
          count += 1

    return count > 0
  except Exception as e:
    app.logger.warn(e)
    return False


def get_unit(vtype, exchange):
  if vtype == 'ST':
    if exchange == 'SH' or exchange == 'SZ':
      return 'CNY'


def c2int(price_str):
  return int(float(price_str) * 100)


def import_data(db, filename):
  tokens = re.split(FILENAME_SEP, os.path.basename(filename))
  app.logger.info(tokens)
  (vtype, exchange, code) = tokens[0], tokens[1], tokens[2]
  data_id = db.execute_and_fetch('select id from Variety where type = %s and exchange = %s and code = %s', (vtype, exchange, code))[0]
  if not data_id:
    app.logger.warn('Variety does not exist: %s %s %s', vtype, exchange, code)
    return False
  else:
    app.logger.info('import data id: %s', data_id[0])
    sql_list = []
    with open(filename) as f:
      lines = f.readlines()
      for line in lines:
        tokens = line.split(',')
        if len(tokens) < 7:
          app.logger.warn('skip bad data line %s', line)
          continue
        start_date = datetime.strptime(tokens[0], '%Y/%m/%d').strftime('%Y-%m-%d')
        start_ts = '%s 00:00:00' % tokens[0]
        sql_list.append('insert into Price(vid, unit, period, start_date, start_ts, open, high, low, close, volume, turnover) ' + \
                        'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (data_id[0], #vid
                         get_unit(vtype, exchange), #unit
                         '1d', #period
                         start_date, #start_date
                         start_ts, #start_ts
                         c2int(tokens[1]), # open
                         c2int(tokens[2]), #high
                         c2int(tokens[3]), #low
                         c2int(tokens[4]), #close
                         int(tokens[5]), #volume
                         float(tokens[6]) #turnover
                        ))
    
    db.batch_execute(sql_lsit)
    db.close()
    return True