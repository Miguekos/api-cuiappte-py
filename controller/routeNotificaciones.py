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


@app.route('/cuidappte/notifications/<tipo>', methods=['GET'])
def get_notifications_consintomas(tipo):
    try:
        print(type(tipo))
        print(tipo)
        global idAsist
        if tipo == "1":
            idAsist = mongo.db.notificaciones_consintomas.find()
        if tipo == "2":
            idAsist = mongo.db.notificaciones_cuidate.find()
        return dumps(idAsist)
        # asist["id"] = repararIdInput(asist["_id"])
        # asist.pop("_id")
    except ValueError:
        print(ValueError)
        jsonResp = {
            "codRes": "99",
            "message": "{}".format("Error get documentos")
        }
        return jsonify(jsonResp)


def updateAt():
    import pytz
    lima = pytz.timezone('America/Lima')
    return datetime.now(lima)

@app.route('/cuidappte/notifications/<tipo>/<id>', methods=['DELETE'])
def delete_notificaciones(tipo, id):
    print("ID: {}".format(id))
    try:
        if tipo == 1:
            mongo.db.notificaciones_consintomas.delete_one({'_id': ObjectId(id)})
            resp = jsonify('registro eliminado correctamente!')
            resp.status_code = 200
            return resp
        if tipo == 2:
            mongo.db.notificaciones_cuidate.delete_one({'_id': ObjectId(id)})
            resp = jsonify('registro eliminado correctamente!')
            resp.status_code = 200
            return resp
    except:
        jsonResp = {
            "codRes": "99",
            "message": "{}".format("Error get documentos")
        }
        return jsonify(jsonResp)
