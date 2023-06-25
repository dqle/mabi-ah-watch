import flask
import logging
import pymongo
import os
from dotenv import load_dotenv

### Load Environment Variable from input.env file
load_dotenv()
MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_PASWORD = os.getenv("MONGODB_PASWORD")

def get_collection():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://{}:{}@mabi-ah.hdehgcc.mongodb.net/?retryWrites=true&w=majority".format(MONGODB_USER,MONGODB_PASWORD)
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = pymongo.MongoClient(CONNECTION_STRING)
 
   # Get the database
   database = client['mabi_ah_watch']

   # Get the collection
   return database['ah_items']

def insert_item(item, collection):
    collection.insert_one(item)

def get_all_items_in_collection(collection):
    return list(collection.find({},{"_id" : 0}))

app = flask.Flask(__name__)

#Disable logging
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True


@app.route('/')
def index():
    collection = get_collection()
    headings = ("Name", "Id", "Price")
    listings = get_all_items_in_collection(collection)
    return flask.render_template('index.html', headers=headings, listings=listings)

@app.route('/add-item', methods=['POST'])
def add_item():
    collection = get_collection()
    name = flask.request.json['name']
    id = flask.request.json['id']
    price = flask.request.json['price']
    item = {
        "name": name,
        "id": id,
        "price": price
    }
    insert_item(item, collection)
    return flask.redirect(flask.url_for('index'))

@app.route('/delete-item', methods=['POST'])
def delete_item():
    collection = get_collection()
    delete_item_name = flask.request.json['name']
    collection.delete_one({ "name": delete_item_name })
    return flask.redirect(flask.url_for('index'))

@app.route('/bulk-add', methods=['POST'])
def bulk_add():
    collection = get_collection()
    items = flask.request.json
    collection.insert_many(items)
    return flask.Response(status=200)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2412)