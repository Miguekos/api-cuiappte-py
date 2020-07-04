from app import app
from flask import jsonify, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from mongo import mongo
from bson.json_util import dumps
# JSON.parse (dumps)
from bson.objectid import ObjectId
from flask_cors import CORS
from pytz import timezone
from datetime import datetime, timedelta
import collections
CORS(app, supports_credentials=True)

def repararIdInput(id):
    print(id['$oid'])
    return id['$oid']

@app.route('/cuidappte/asistencia', methods=['GET'])
def get_asistecia():
    try:
        asist = mongo.db.asistencia.find()
        # asist["id"] = repararIdInput(asist["_id"])
        # asist.pop("_id")
        return dumps(asist)
    except ValueError:
        print(ValueError)
        jsonResp = {
            "codRes": "99",
            "message": "{}".format("Error get asistencia")
        }
        return jsonify(jsonResp)

def updateAt():
    import pytz
    lima = pytz.timezone('America/Lima')
    return datetime.now(lima)

@app.route('/cuidappte/asistencia', methods=['POST'])
def add_asistencia():
    import pytz
    lima = pytz.timezone('America/Lima')
    li_time = datetime.now(lima)
    _json = request.json
    _json['idUser'] = repararIdInput(_json['_id'])
    _json['created_at'] = li_time
    _json['updated_at'] = li_time
    _json.pop('_id')
    try:
        id = mongo.db.asistencia.insert(_json)
        resp = jsonify('User added successfully!')
        resp.status_code = 200
        return resp
    except:
        jsonResp = {
            "codRes": "99",
            "message": "{}".format("Error guarando su asistencia")
        }
        return jsonify(jsonResp)
    # user = mongo.db.asistencia.find()
    # print(list(user))
    # print(user)
    # resp = dumps(user)
    # Converting string to list
    # print(asd)

@app.route('/cuidappte/asistencia', methods=['PUT'])
def put_asistencia():
    print("Consultando Creditos del ID: {}".format(id))
    user = mongo.db.asistencia.find()
       # print(user)
    resp = dumps(user)
    # Converting string to list
    res = resp.strip('][').split(', ')
    # # printing final result and its type
    # print("final list", res)
    # print(type(res))
    # print(type(user))
    asd = collections.Counter(res)
    # print(asd)
    return dumps(val)


@app.route('/cuidappte/asistencia', methods=['DELETE'])
def deleteAsistencia(id):
    print("Consultando Creditos del ID: {}".format(id))
    mongo.db.asistencia.delete_one({'_id': ObjectId(id)})
    resp = jsonify('abono eliminado correctamente!')
    resp.status_code = 200
    return resp

