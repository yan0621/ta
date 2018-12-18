import os

from flask import (
    Blueprint, flash, Flask, g, redirect, render_template, request, url_for
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
  
  return render_template('/ta/show.html')