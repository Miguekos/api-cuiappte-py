from app import app
from flask import jsonify, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from mongo import mongo
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_cors import CORS

import pytz
from datetime import datetime

CORS(app, supports_credentials=True)


# Rutas User
@app.route('/user/add', methods=['POST'])
def add_user():
    lima = pytz.timezone('America/Lima')
    li_time = datetime.now(lima)
    _json = request.json
    _name = _json['name']
    _telefono = _json['telefono']
    _email = _json['email']
    _dni = _json['dni']
    _url = 'https://api.apps.com.pe/uploads/'
    _role = _json['role']
    _profile = 'boy-avatar.png'
    global _password
    # _password = _json['pwd']
    _password = 'secret'
    # if len(_password) == 0:
    #     _password = 'secret'
    # else:
    #     _password = _json['pwd']
    # validate the received values
    if _name and _email and _password and request.method == 'POST':
        # do not save password as a plain text
        _hashed_password = generate_password_hash(_password)
        # save details
        id = mongo.db.user.insert(
            {'name': _name, 'dni': _dni, 'email': _email, 'telefono': _telefono, 'profile': _profile, 'url': _url, 'role': _role,
             'pwd': _hashed_password, "created_at": li_time})
        resp = jsonify('User added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/login', methods=["POST"])
def login():
    _json = request.json
    try:
        _user = mongo.db.user.find_one({
            'email': _json["email"]
        })
        print("_user", type(_user))
        if _user != None:
            validar = check_password_hash(_user['pwd'], _json["pwd"])
            print("validar", validar)
            if validar == True:
                idUser = _user['_id']
                print(idUser)
                jsonFinal = {
                    "codRes": "00",
                    "id": idUser,
                    "name": _user['name'],
                    "email": _user['email'],
                    "url": _user['url'],
                    "profile": _user['profile'],
                    "role": _user['role']
                }
                return dumps(jsonFinal)
            else:
                jsonFinal = {
                    "codRes": "01",
                    "message": "Password Incorrecto"
                }
                resp = jsonify(jsonFinal)
                resp.status_code = 200
                return resp
        else:
            jsonFinal = {
                "codRes": "01",
                "message": "Email Incorrecto"
            }
            resp = jsonify(jsonFinal)
            resp.status_code = 200
            return resp
    except:
        jsonFinal = {
            "codRes": "99",
            "message": "ErrorControlado"
        }
        resp = jsonify(jsonFinal)
        resp.status_code = 200
        return resp


@app.route('/user/users')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp


@app.route('/user/<id>')
def user(id):
    print(id)
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    # print(list(user))
    resp = dumps(user)
    return resp


@app.route('/user/updateImage', methods=['PUT'])
def update_user_updateImage():
    _json = request.json
    _id = _json['_id']
    _profile = _json['profile']
    # validate the received values
    # save edits
    mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                             {'$set': {'profile': _profile}})
    resp = jsonify('User updated successfully!')
    resp.status_code = 200
    return resp


@app.route('/user/update', methods=['PUT'])
def update_user():
    _json = request.json
    _id = _json['_id']
    _name = _json['name']
    _email = _json['email']
    _telefono = _json['telefono']
    _dni = _json['dni']
    _profile = ''
    _password = _json['pwd']
    # validate the received values
    if _name and _email and _id and request.method == 'PUT':
        # do not save password as a plain text
        global jsonUpdate, _hashed_password
        if len(_password) == 0:
            jsonUpdate = {'name': _name, 'dni': _dni, 'email': _email, 'telefono': _telefono, 'profile': _profile}
        else:
            _hashed_password = generate_password_hash(_password)
            jsonUpdate = {'name': _name, 'dni': _dni, 'email': _email, 'telefono': _telefono, 'profile': _profile,
                          'pwd': _hashed_password}
        # save edits
        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                 {'$set': jsonUpdate})
        resp = jsonify('User updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/user/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id': ObjectId(id)})
    resp = jsonify('User deleted successfully!')
    resp.status_code = 200
    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
