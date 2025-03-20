from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
from bson.objectid import ObjectId


load_dotenv()


DB_NAME = getenv("DB_NAME")
DB_HOST = getenv("DB_HOST")
DB_PORT = int(getenv("DB_PORT"))
DB_COLLECTION = getenv("DB_COLLECTION")

app = Flask(__name__)
app.config["DEBUG"] = getenv("DEBUG")


try:
    client = MongoClient(DB_HOST, DB_PORT)
    print("Client connected successfully \n")
except:
    print("Could not connect to Client")

database = client[DB_NAME]
print("User database created or accessed successfully \n")

Collection = database[DB_COLLECTION]
print("User collection created or accessed successfully \n")


@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = list(Collection.find())

        for user in users:
            user['_id'] = str(user['_id'])
        
        return make_response(jsonify(users), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), 500)

@app.route('/users/<string:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        user = Collection.find_one({"_id": ObjectId(id)})

        if user:
            user['_id'] = str(user['_id'])
            return make_response(jsonify(user), 200)
        else:
           return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), 500)

@app.route('/users', methods=['POST'])
def post_user():
    try:
        data = request.get_json()
        user = Collection.insert_one(data)

        user['_id'] = str(user['_id'])

        return make_response(jsonify(user), 201)
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), 500)

@app.route('/users/<string:id>', methods=['PUT'])
def put_user(id):
    new_data = request.get_json()

    try:
        new_user = Collection.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': new_data}
        )

        new_user['_id'] = str(new_user['_id'])

        return make_response(jsonify(user), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), 500)

@app.route('/users/<string:id>', methods=['DELETE'])
def delete_user(id):
    try:
        Collection.delete_one({'_id': ObjectId(id)})

        return make_response(jsonify({'message': "User deleted successfully"}),204)
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), 500)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)