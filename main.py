__author__ = 'Berker GUCUR'
from flask import Flask, jsonify
from peewee import *
from flask_peewee.db import Database
from datetime import datetime
import json

DATABASE = {
    'name': 'cheatsheet',
    'engine': 'peewee.MySQLDatabase',
    'user': 'root',
    'passwd': '',
}
app = Flask(__name__)
app.config.from_object(__name__) # load database configuration from this module
db = Database(app)

class Category(db.Model):
    id = PrimaryKeyField()
    parent_id = IntegerField(default=0) #bir ust kategori
    name = CharField()
    desc = TextField()
    created_at = DateTimeField(default= datetime.now())
    class Meta:
        db_table = 'category'

class CheatSheet(db.Model):
    id = PrimaryKeyField()
    category_id = ForeignKeyField(Category, related_name='sheets')
    title = CharField(unique=True)
    data = TextField()
    created_at = DateTimeField(default= datetime.now())
    class Meta:
        db_table = 'cheat_sheets'


@app.route("/")
def home():
    return "Welcome CheatSheet App's Webservice"

@app.route("/v1/category/main")
def main_category():
    data = []
    query = Category.select().where(Category.parent_id == 0)
    for x in query:
        data.append(x._data)

    return json.dumps(data)

@app.route("/v1/category/get/<id>")
def get_category(id):
    return json.dumps(Category.select().where(Category.id == id).dicts().get())


if __name__ == "__main__":
    app.debug = True
    app.run()