import os
from peewee import *
from flask import Flask
from html_sanitizer import Sanitizer

app = Flask(__name__)
sanitizer = Sanitizer()
# name of database
db = SqliteDatabase('peewee_app.db')
app.secret_key = os.environ.get('SECRET_KEY') or 'you-cannot-guess'
