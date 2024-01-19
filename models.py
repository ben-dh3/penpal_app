"""
models imports app, but app does not import models so we haven't created
any loops.
"""
from peewee import *
from app import db

# model class -> database table
class User(Model):
    id = AutoField()
    username = CharField()
    email = CharField(unique=True) 
    password = CharField()
    hometown = CharField()
    profile_picture = CharField()

    class Meta:
        database = db # This model uses the "peewee_app.db" database.

class Post(Model):
    message = CharField()
    time = TimeField()
    sender_id = ForeignKeyField(User, to_field="id")
    recipient_id = ForeignKeyField(User, to_field="id")

    class Meta:
        database = db # this model uses the "peewee_app.db" database


db.connect()