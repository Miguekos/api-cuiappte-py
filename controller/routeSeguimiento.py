import random
import string
from datetime import datetime

from bson.json_util import dumps
from bson.objectid import ObjectId

import pytz
from flask import jsonify, request
from flask_cors import CORS

from app import app
from mongo import mongo

CORS(app, supports_credentials=True)


# @app.route("/")
# def index():
#     return "The URL for this page is {}".format(url_for("index"))

def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))

# Rutas User
@app.route('/cuidappte/seguimiento', methods=['POST'])
def add_seguimiento():
    lima = pytz.timezone('America/Lima')
    li_time = datetime.now(lima)
    _json = request.json
    try:
        _json.pop("codRes")
        _json['created_at'] = li_time
        _json['id_'] = _json['id']['$oid']
        _json.pop("id")
        # print(_json)

        if _json:
            # do not save password as a plain text
            # save details
            try:
                id = mongo.db.seguimiento.insert(_json)
                resp = jsonify('User added successfully!')
                resp.status_code = 200
                return resp
            except:
                jsonResp = {
                    "codRes": "99",
                    "message": "{}".format("Un error al registrar su seguimiento")
                }
                return jsonify(jsonResp)
        else:
            return not_found()
    except:
        _json['created_at'] = li_time
        _json['id_'] = _json['_id']['$oid']
        _json.pop("_id")
        # print(_json)

        if _json:
            # do not save password as a plain text
            # save details
            try:
                id = mongo.db.seguimiento.insert(_json)
                resp = jsonify('User added successfully!')
                resp.status_code = 200
                return resp
            except:
                jsonResp = {
                    "codRes": "99",
                    "message": "{}".format("Un error al registrar su seguimiento")
                }
                return jsonify(jsonResp)
        else:
            return not_found()

@app.route('/cuidappte/seguimientoJefe', methods=['POST'])
def get_seguimientoJefe():
    _json = request.json
    users = mongo.db.seguimiento.find({'jefeDirecto' : _json['dni']})
    resp = dumps(users)
    # resp = list(users)
    # print(resp)
    return resp

@app.route('/cuidappte/seguimiento/<id>', methods=['GET'])
def get_seguimiento(id):
    if id == "all":
        users = mongo.db.seguimiento.find()
        resp = dumps(users)
        # resp = list(users)
        # print(resp)
        return resp

    if id:
        users = mongo.db.seguimiento.find_one({'_id': ObjectId(id)})
        print(id)
        resp = dumps(users)
        # resp = list(users)
        # print(resp)
        return resp

@app.route('/cuidappte/seguimiento/seguimiento', methods=['GET'])
def get_seguimiento_ciudate():
    users = mongo.db.seguimiento.find({"seguimiento" : 1})
    resp = dumps(users)
    # resp = list(users)
    print(resp)
    return resp

@app.route('/cuidappte/seguimiento/dealta', methods=['GET'])
def get_seguimiento_dealta():
    users = mongo.db.seguimiento.find({"dealta" : 1})
    resp = dumps(users)
    # resp = list(users)
    # print(resp)
    return resp

@app.route('/cuidappte/seguimientoOne/<id>', methods=['GET'])
def get_seguimiento_one(id):
    users = mongo.db.seguimiento.find({'id_': id})
    resp = dumps(users)
    # resp = list(users)
    # print(resp)
    return resp

@app.route('/cuidappte/seguimiento', methods=['PUT'])
def update_seguimiento():
    lima = pytz.timezone('America/Lima')
    li_time = datetime.now(lima)
    _json = request.json
    _id = _json['_id']['$oid']
    _json['updated_at'] = li_time
    _json.pop('_id')
    try:
        _json.pop('created_at')
    except:
        print("No tiene created_at")
    # _temp = _json['temp']
    # validate the received values
    # save edits
    mongo.db.seguimiento.update_one({'_id': ObjectId(_id)},
                             {'$set': _json})
    resp = jsonify('User updated successfully!')
    resp.status_code = 200
    return resp


@app.route('/cuidappte/seguimiento/<id>', methods=['DELETE'])
def delete_seguimiento(id):
    mongo.db.seguimiento.delete_one({'_id': ObjectId(id)})
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
