import os

from flask import Flask, request, jsonify, json
import pymongo
from pymongo.errors import InvalidName
from bson import json_util, ObjectId

app = Flask(__name__)
mongo_host = os.environ.get('MONGODB_SERVICE_HOST') or 'localhost'
mongo_port = int(os.environ.get('MONGODB_SERVICE_PORT') or 27017)
db_name = os.environ.get("MONGODB_DATABASE_NAME") or 'test'
client = pymongo.MongoClient(mongo_host, mongo_port)
db = client.get_database(db_name)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/data/<collection>', methods=['GET'])
def list_data(collection):
    result = {'collection': collection, 'data': []}
    for item in db.get_collection(collection).find({}):
        result['data'].append(json.loads(json.dumps(item, default=json_util.default)))
    return jsonify(result)


@app.route('/data/create', methods=['POST'])
def create_data():
    """
    POST /data/create
    {
        collection: "collection_name",
        data: [{k: v, ...}, ...]
    }
    """
    json_data = request.get_json()
    try:
        if 'collection' in json_data and 'data' in json_data:
            collection_name = json_data['collection']
            data = json_data['data']
            collection = db.get_collection(collection_name)
            collection.insert_many(data)
            return jsonify({'message': 'created'})
        else:
            return jsonify({'message': 'missing key'})
    except InvalidName:
        return jsonify({'message': 'invalid collection name'})


@app.route('/data/delete/<collection>/<id>', methods=['DELETE'])
def delete_data(collection, id):
    db.get_collection(collection).delete_one({"_id": ObjectId(id)})
    return jsonify({'message': 'deleted'})


if __name__ == '__main__':
    app.run()
