from datetime import datetime

from bson.json_util import dumps
# JSON.parse (dumps)
from flask import jsonify, request
from flask_cors import CORS
from bson.objectid import ObjectId

from app import app
from mongo import mongo

CORS(app, supports_credentials=True)


def repararIdInput(id):
    print(id['$oid'])
    return id['$oid']


def updateAt():
    import pytz
    lima = pytz.timezone('America/Lima')
    return datetime.now(lima)


@app.route('/cuidappte/comunicados/<id>', methods=['GET'])
def get_comunicados(id):
    try:
        idAsist = mongo.db.comunicados.find({"idUser": id})
        # asist["id"] = repararIdInput(asist["_id"])
        # asist.pop("_id")
        return dumps(idAsist)
    except ValueError:
        print(ValueError)
        # jsonResp = {
        #     "codRes": "99",
        #     "message": "{}".format("Error get comunicados")
        # }
        # return jsonify(jsonResp)


@app.route('/cuidappte/comunicados', methods=['POST'])
def add_comunicados():
    import pytz
    lima = pytz.timezone('America/Lima')
    li_time = datetime.now(lima)
    _json = request.json
    _json['idUser'] = repararIdInput(_json['id'])
    _json.pop('id')
    _json.pop('codRes')
    _json.pop('temp')

    try:
        _json['created_at'] = li_time
        _json['updated_at'] = li_time
        id = mongo.db.comunicados.insert(_json)
        resp = jsonify('Update comunicados successfully!')
        resp.status_code = 200
        return resp
    except ValueError:
        print(ValueError)
        # except:
        # jsonResp = {
        #     "codRes": "99",
        #     "message": "{}".format("Error guarando su comunicados")
        # }
        # return jsonify(jsonResp)

@app.route('/cuidappte/comunicados/<id>', methods=['DELETE'])
def delete_comunicados(id):
    print("ID que se elminara: {}".format(id))
    mongo.db.comunicados.delete({'_id': ObjectId(id)})
    resp = jsonify('registro eliminado correctamente!')
    resp.status_code = 200
    return resp