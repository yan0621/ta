import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ta_train.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def validate(username, password):
  error = None
  if not username:
    error = 'username must not be empty!'
  elif not password:
    error = 'password must not be empty!' 
  return error


@bp.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    error = None
    db = get_db()

    error = validate(username, password)
    if not error:
      if db.execute('select id from user where username = ?', (username,)).fetchone() is not None:
        error = 'username already exists!'

    if not error:
      db.execute('insert into user (username, password) values (?, ?)', (username, generate_password_hash(password)))
      db.commit()
      return redirect(url_for('auth.login'))

    flash(error)

  return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None

    error = validate(username, password)
    if not error:
      user = db.execute('select * from user where username = ?', (username,)).fetchone()
      if not user:
        error = 'username does not exist!'
      elif not check_password_hash(user['password'], password):
        error = 'password is not correct!'

    if not error:
      session.clear()
      session['user_id'] = user['id']
      return redirect(url_for('index'))

    flash(error)

  return render_template('auth/login.html')


@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))


@bp.before_app_request
def load_user_info():
  user_id = session.get('user_id')

  if not user_id:
    g.user = None
  else:
    g.user = get_db().execute('select * from user where id = ?', (user_id,)).fetchone()


def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth/login'))

    return view(**kwargs)

  return wrapped_view