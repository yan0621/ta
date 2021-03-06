import os
import time

from flask import (
    Blueprint, flash, Flask, g, jsonify, redirect, render_template, request, url_for
)
from werkzeug.utils import secure_filename

from objects import price
from ta_train.db import get_db

bp = Blueprint('ta', __name__)

UPLOAD_FOLDER = '/tmp/ta/upload'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def is_file_allowed(filename):
  return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def ensure_upload_folder(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)


@bp.route('/ta/upload_data', methods=['GET', 'POST'])
def upload_data():
  if request.method == 'POST':
    if 'file' not in request.files:
      flash('No file found')
      return redirect(request.url)
    file = request.files['file']
    # when user does not select any file
    if not file.filename:
      flash('No file selected')
      return redirect(request.url)
    if file and is_file_allowed(file.filename):
      filename = secure_filename(file.filename)
      ensure_upload_folder(app.config['UPLOAD_FOLDER'])
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect(url_for('ta.data_uploaded', filename=filename))
    else:
      flash('Bad file type')
      return redirect(request.url)

  return render_template('ta/upload_data.html')


@bp.route('/ta/uploaded/<filename>')
def data_uploaded(filename):
  with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
    content = f.readlines()
  return render_template('ta/data_uploaded.html', content=content)


@bp.route('/ta/list')
def list_variety():
  db = get_db()
  variety_in_db = db.execute_and_fetch('select * from Variety')

  variety_list = []
  for (data_id, vtype, exchange, name, code) in variety_in_db:
    variety_list.append({
      'id': id,
      'type': vtype,
      'exchange': exchange,
      'name': name,
      'code': code
    })

  db.close()
  return render_template('ta/list.html', variety_list=variety_list)


@bp.route('/ta/show/<data_id>')
def show_variety(data_id):
  db = get_db()
  
  variety = db.execute_and_fetch('select * from Variety where id = %s' % data_id)[0]
  meta = {
    'data_id': data_id,
    'name': variety[3], # name
    'code': variety[4], # code
  }
  
  pdata = db.execute_and_fetch('select * from Price where vid = %s' % data_id)
  render_data = []
  for p in pdata:
    render_data.append([
      1000 * time.mktime(p[5].timetuple()), # datetime -> timestamp
      p[6]/100.0, # open
      p[7]/100.0, # high
      p[8]/100.0, # low
      p[9]/100.0, # close
      p[10]] # volume
    )
  return render_template('/ta/show.html', meta=meta, render_data=render_data)


@bp.route('/ta/dobtest')
def double_blind_test():
  db = get_db()
  meta = {}
  render_data = []

  return render_template('/ta/show.html', meta=meta, render_data=render_data)


@bp.route('/ta/fetch')
def fetch_data():
  data_id = request.args.get('data_id')
  start_date = request.args.get('start_date')
  offset = request.args.get('offset')
  period = request.args.get('period')
  
  db = get_db()
  prices = db.execute_and_fetch(
          'select * from Price where vid = %s and start_date >= %s and period = %s ' +
          'ordered by start_date asc limit %s'
          % (data_id, start_date, period, offset))
  pdata = []
  
  return jsonify({
    'status': 'ok',
    'data': pdata
  })