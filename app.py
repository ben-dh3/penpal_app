import os
from peewee import *
from flask import Flask
from html_sanitizer import Sanitizer

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sanitizer = Sanitizer()
# name of database
db = SqliteDatabase('peewee_app.db')
app.secret_key = os.environ.get('SECRET_KEY') or 'you-cannot-guess'
