from flask import Flask
from pymongo import MongoClient
import json


client = MongoClient()
db = client.devdb
collection = db.jobs

# reads json file, returns data as python dict
def load_data():
    with open("./app/data.json", "r") as file:
        data = json.load(file) # gets python dict
    return data

# insert data if not already inserted
if collection.count_documents({}) == 0:
    data = load_data()
    result = collection.insert_many(data)
    print ("total inserted:", len(result.inserted_ids))

# make job application Flask object
jobapp = Flask(__name__, static_url_path='/static')

import app.routes as routes