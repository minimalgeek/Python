import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

DATABASE = 'proba'

app = Flask(__name__)
app.config.from_object(__name__)  # load config from this file , main.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)  # points to a config file to be loaded


@app.teardown_appcontext
def close_db(error):
    print('>>>>>>> close_db <<<<<<<<')
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


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

# ret = get_db().execute("SELECT 1")
# print(ret)
