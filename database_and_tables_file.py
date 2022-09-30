from peewee import *
from os import path
# this is how to specify the path where the db is to be stored
db_connection_path = path.dirname(path.realpath(__file__))
# this is how to create our DB
db = SqliteDatabase(path.join(db_connection_path, "emobilis.db"))
# start creating tables
class User(Model):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()
    # this is how to put our table into our database
    class Meta:
        database = db

class Question(Model):
    question = CharField()
    answer = CharField()
    class Meta:
        database = db

# Finally create the two tables
User.create_table(fail_silently=True)
Question.create_table(fail_silently= True)