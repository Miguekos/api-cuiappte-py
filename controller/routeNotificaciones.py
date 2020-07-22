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


@app.route('/cuidappte/notifications/alertas/<id>', methods=['GET'])
def get_notifications_alertas(id):
    try:
        idAsist = mongo.db.notificaciones.find({"dni": id, 'activo': 1})
        # CidAsist = mongo.db.notificaciones.count({"dni": id})
        # jsonResponse = {
        #     'message': dict(idAsist),
        #     'cantAsist': CidAsist
        # }
        return dumps(idAsist)
        # return jsonResponse
        # asist["id"] = repararIdInput(asist["_id"])
        # asist.pop("_id")
    except:
        jsonResp = {
            "codRes": "99",
            "message": "{}".format("Error get documentos")
        }
        return jsonify(jsonResp)


@app.route('/cuidappte/notifications/alertas', methods=['POST'])
def add_notifications_alertas():
    try:
        import pytz
        lima = pytz.timezone('America/Lima')
        _json = request.json
        FindNotiDe = mongo.db.user.find({'dni': _json['de']})
        FindNotiPara = mongo.db.user.find({'dni': _json['para']})
        FindNotiPara = list(FindNotiPara)[0]
        FindNotiDe = list(FindNotiDe)[0]
        FindNotiDe.pop('_id')
        FindNotiDe.pop('pwd')
        FindNotiPara.pop('_id')
        FindNotiPara.pop('pwd')
        print(FindNotiDe)
        jsonInsert = {
            'de': FindNotiDe,
            'para': FindNotiPara,
            'dni': FindNotiPara['dni'],
            'comentario': _json['comentario'],
            'color': _json['color'],
            'activo': 1,
            'created_at': datetime.now(lima)
        }
        idAsist = mongo.db.notificaciones.insert(jsonInsert)
        resp = jsonify('{}'.format("se registro la alerta"))
        resp.status_code = 200
        return resp
        # asist["id"] = repararIdInput(asist["_id"])
        # asist.pop("_id")
    except:
        jsonResp = {
            "codRes": "99",
            "message": "{}".format("Error get documentos")
        }
        return jsonify(jsonResp)


def updateAt():
    import pytz
    lima = pytz.timezone('America/Lima')
    return datetime.now(lima)


@app.route('/cuidappte/notifications/alertas/<id>', methods=['PUT'])
def delete_notificaciones(id):
    print("ID: {}".format(id))
    try:
        mongo.db.notificaciones.update_one({'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)},
                                     {'$set': {'activo': 0}})
        resp = jsonify('registro actualizado correctamente!')
        resp.status_code = 200
        return resp
    except:
        jsonResp = {
            "codRes": "99",
            "message": "{}".format("Error get documentos")
        }
        return jsonify(jsonResp)
