import os
import sqlite3
import logging
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(__name__)  # load config from this file , main.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db/flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)  # points to a config file to be loaded


def log_enter_exit(func):
    def func_wrapper(*args, **kwargs):
        logger.info("> Enter %s <", func.__name__)
        ret = func(*args, **kwargs)
        logger.info("> Exit %s <", func.__name__)
        return ret

    return func_wrapper


@app.teardown_appcontext
@log_enter_exit
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.cli.command('initdb')
def init_db_command():
    init_db()


@log_enter_exit
def init_db():
    db = get_db()
    with app.open_resource('db/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    # allow the rows to be treated as if they were dictionaries instead of tuples
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    # you can store information safely on the g object
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


# Application code

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for(show_entries.__name__))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for(show_entries.__name__))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for(show_entries.__name__))
