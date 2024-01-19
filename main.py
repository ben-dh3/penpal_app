"""
this is the "secret sauce" -- a single entry-point that resolves the
import dependencies.  If you're using blueprints, you can import your
blueprints here too.

then when you want to run your app, you point to main.py or `main.app`
"""
from app import app, db
import os
from models import *
from views import *

def create_tables():
    # Create table for each model if it does not exist.
    # Use the underlying peewee database object instead of the
    # flask-peewee database wrapper:
    db.drop_tables([User, Post])
    db.create_tables([User, Post], safe=True)
    user1 = User(username='Ben DH', email='benjaminduffield1997@gmail.com', password='password123', hometown='Putney', profile_picture='ben.jpg')
    user1.save()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))