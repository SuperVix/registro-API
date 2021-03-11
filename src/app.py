from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
import pymongo


app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://Vix:1234@cluster0.w4ogh.mongodb.net/veterinaria?retryWrites=true&w=majority")
db = client.test

@app.route('/users', methods=['POST'])
def create_user():
    #Receiving data
    name = request.json['name']
    surname = request.json['surname']
    email = request.json['email']
    password = request.json['password']

    if name and surname and email and password:
        hashed_password = generate_password_hash(password)
        id = db.users.insert_one(
            {'name': name, 'surname': surname, 'email': email, 'password': hashed_password}
        )
        response = {
            'id': str(id),
            'name': name,
            'surname': surname,
            'email': email,
            'password': hashed_password
        }
        return response
    else:
        return not_found()

    return {'message': 'received '}

@app.route('/users', methods=['GET'])
def get_users():
    users = db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User ' + id + ' was deletedsuccessfully'})
    return response

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    name = request.json['name']
    surname = request.json['surname']
    email = request.json['email']
    password = request.json['password']

    if name and surname and email and password:
        hashed_password = generate_password_hash(password)
        db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'name': name,
            'surname': surname,
            'email': email,
            'password': hashed_password
        }})
        response = jsonify({'message': 'User ' + id + 'was update successfully'})
        return response

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resourse Not Found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True)

