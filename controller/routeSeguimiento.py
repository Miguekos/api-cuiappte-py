import random
import string
from datetime import datetime, timedelta

from bson.json_util import dumps
from bson.objectid import ObjectId

import pytz
from flask import jsonify, request
from flask_cors import CORS

from app import app
from mongo import mongo

CORS(app, supports_credentials=True)

def formatDate(v):
    import pytz
    lima = pytz.timezone('America/Lima')
    fehcaEvaluarTest = v
    # print("fehcaEvaluarTest", fehcaEvaluarTest)
    # tz = pytz.timezone('America/St_Johns')
    fehcaEvaluarTest = fehcaEvaluarTest.replace(tzinfo=pytz.UTC)
    # print("fehcaEvaluarTest 2", fehcaEvaluarTest)
    fehcaEvaluar = fehcaEvaluarTest.astimezone(lima)
    # print("fehcaEvaluarTest 3", fehcaEvaluar)
    # print("fehcaEvaluar")
    # print(fehcaEvaluar)
    # print(datetime.now(lima))
    # return v or datetime.now(lima)
    return fehcaEvaluar

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
        _json.pop("pwd")
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
        _json.pop("pwd")
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
        args = request.args
        fi = args["fi"]
        ff = args["ff"]
        # print(type(fi))
        in_time_obj = datetime.strptime("{} 00:00:00".format(fi), '%d/%m/%Y %H:%M:%S')
        in_time_obj = formatDate(in_time_obj) + timedelta(hours=5)
        out_time_obj = datetime.strptime("{} 23:59:59".format(ff), '%d/%m/%Y %H:%M:%S')
        out_time_obj = formatDate(out_time_obj) + timedelta(hours=5)
        print("Traer datos de {} hasta {}".format(in_time_obj, out_time_obj))
        users = mongo.db.seguimiento.find({'created_at': {"$gte": in_time_obj, "$lt": out_time_obj}})
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
