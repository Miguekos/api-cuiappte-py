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


@app.route('/cuidappte/documentos/<id>', methods=['GET'])
def get_documentos(id):
    try:
        idAsist = mongo.db.documentos.find({"idUser": id})
        # asist["id"] = repararIdInput(asist["_id"])
        # asist.pop("_id")
        return dumps(idAsist)
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


@app.route('/cuidappte/documentos', methods=['POST'])
def add_documentos():
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
        id = mongo.db.documentos.insert(_json)
        resp = jsonify('documentos added successfully!')
        resp.status_code = 200
        return resp
    except:
        # except:
        jsonResp = {
            "codRes": "99",
            "message": "{}".format("Error guarando su documentos")
        }
        return jsonify(jsonResp)


# user = mongo.db.documentos.find()
# print(list(user))
# print(user)
# resp = dumps(user)
# Converting string to list
# print(asd)


# @app.route('/cuidappte/documentos', methods=['POST'])
# def add_documentos():
#     import pytz
#     lima = pytz.timezone('America/Lima')
#     li_time = datetime.now(lima)
#     _json = request.json
#     _json['idUser'] = repararIdInput(_json['id'])
#     _json.pop('id')
#     _json.pop('codRes')
#     _json.pop('temp')
#
#     idAsist = mongo.db.documentos.find({"idUser": _json['idUser']})
#     try:
#         cantAsist = len(list(idAsist))
#         print(type(cantAsist))
#         print(cantAsist)
#         if cantAsist == 0:
#             _json['created_at'] = li_time
#             _json['updated_at'] = li_time
#             _json['archivos'] = [{
#                 "comentario": _json['comentario'],
#                 "documento": _json['docs'],
#                 "created_at": li_time
#             }]
#             _json.pop("comentario")
#             _json.pop("docs")
#             print("add")
#             id = mongo.db.documentos.insert(_json)
#             resp = jsonify('documentos added successfully!')
#             resp.status_code = 200
#             return resp
#
#         if cantAsist == 1:
#             # fehcaEvaluarTest = _json['documentos']['created_at']
#             # fehcaEvaluarTest = datetime.strptime(fehcaEvaluarTest, '')
#             # print(fehcaEvaluarTest)
#             # print("#############################", type(fehcaEvaluarTest))
#             # tz = pytz.timezone('America/St_Johns')
#             # fehcaEvaluarTest = fehcaEvaluarTest.replace(tzinfo=pytz.UTC)
#             # fehcaEvaluar = fehcaEvaluarTest.astimezone(lima)
#             # print(fehcaEvaluar)
#             mongo.db.documentos.update_one({'idUser': _json['idUser']},
#                                            {'$push': {"archivos": {
#                                                "comentario": _json['comentario'],
#                                                "documento": _json['docs'],
#                                                "created_at": li_time
#                                            }}})
#             resp = jsonify('Update documentos successfully!')
#             resp.status_code = 200
#             return resp
#         #     id = mongo.db.documentos.insert(_json)
#         #     resp = jsonify('User added successfully!')
#         #     resp.status_code = 200
#         #     return resp
#     except:
#         # except:
#         jsonResp = {
#             "codRes": "99",
#             "message": "{}".format("Error guarando su documentos")
#         }
#         return jsonify(jsonResp)
#     # user = mongo.db.documentos.find()
#     # print(list(user))
#     # print(user)
#     # resp = dumps(user)
#     # Converting string to list
#     # print(asd)


@app.route('/cuidappte/documentos', methods=['PUT'])
def put_documentos():
    print("Consultando Creditos del ID: {}".format(id))
    user = mongo.db.documentos.find()
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
    return "dumps(val)"


@app.route('/cuidappte/documentos/<id>', methods=['DELETE'])
def delete_documentos(id):
    print("ID: {}".format(id))
    mongo.db.documentos.delete_one({'_id': ObjectId(id)})
    resp = jsonify('registro eliminado correctamente!')
    resp.status_code = 200
    return resp
