import os
from peewee import *
from flask import Flask

app = Flask(__name__)
# name of database
db = SqliteDatabase('peewee_app.db')
app.secret_key = os.environ.get('SECRET_KEY') or 'you-cannot-guess'
