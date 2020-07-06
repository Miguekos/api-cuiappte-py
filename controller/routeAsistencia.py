import collections
from datetime import datetime

from bson.json_util import dumps
# JSON.parse (dumps)
from bson.objectid import ObjectId
from flask import jsonify, request
from flask_cors import CORS

from app import app
from mongo import mongo

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
    _json.pop('_id')

    idAsist = mongo.db.asistencia.find({"idUser": _json['idUser']})
    try:
        cantAsist = len(list(idAsist))
        print(type(cantAsist))
        print(cantAsist)
        if cantAsist == 0:
            _json['created_at'] = li_time
            _json['updated_at'] = li_time
            _json['asistenciaEntrada'] = _json['asistencia']
            _json.pop("asistencia")
            print("add")
            id = mongo.db.asistencia.insert(_json)
            resp = jsonify('asistencia added successfully!')
            resp.status_code = 200
            return resp

        if cantAsist == 1:
            # fehcaEvaluarTest = _json['asistencia']['created_at']
            # fehcaEvaluarTest = datetime.strptime(fehcaEvaluarTest, '')
            # print(fehcaEvaluarTest)
            # print("#############################", type(fehcaEvaluarTest))
            # tz = pytz.timezone('America/St_Johns')
            # fehcaEvaluarTest = fehcaEvaluarTest.replace(tzinfo=pytz.UTC)
            # fehcaEvaluar = fehcaEvaluarTest.astimezone(lima)
            # print(fehcaEvaluar)
            _json['updated_at'] = li_time
            _json['asistenciaSalida'] = _json['asistencia']
            _json.pop("asistencia")
            _json.pop("created_at")
            print("update")
            mongo.db.asistencia.update_one({'idUser': _json['idUser']},
                                           {'$set': _json})
            resp = jsonify('Update asistencia successfully!')
            resp.status_code = 200
            return resp
        #     id = mongo.db.asistencia.insert(_json)
        #     resp = jsonify('User added successfully!')
        #     resp.status_code = 200
        #     return resp
    except ValueError:
    # except:
        print(ValueError)
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
