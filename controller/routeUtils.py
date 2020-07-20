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


@app.route('/cuidappte/utils/<id>', methods=['GET'])
def get_utils(id):
    try:
        if id == "1":
            idAsist = mongo.db.cargos.find()
            # asist["id"] = repararIdInput(asist["_id"])
            # asist.pop("_id")
            return dumps(idAsist)

        elif id == "2":
            idAsist = mongo.db.areas.find()
            # asist["id"] = repararIdInput(asist["_id"])
            # asist.pop("_id")
            return dumps(idAsist)

    except ValueError:
        print(ValueError)
        jsonResp = {
            "codRes": "99",
            "message": "{}".format("Error get utils")
        }
        return jsonify(jsonResp)


def updateAt():
    import pytz
    lima = pytz.timezone('America/Lima')
    return datetime.now(lima)


@app.route('/cuidappte/utils/<id>', methods=['POST'])
def add_utils(id):
    try:
        print(id)
        _json = request.json
        print("Body", _json)
        import pytz
        if id == "1":
            print("entro al if")
            lima = pytz.timezone('America/Lima')
            li_time = datetime.now(lima)
            _json['created_at'] = li_time
            _json['updated_at'] = li_time
            # conteo = mongo.db.cargos.count()
            try:
                print("try")
                conteo = mongo.db.cargos.find().sort('registro', -1).limit(1)
                conteo = list(conteo)
                print(conteo)
                _json['registro'] = conteo[0]['registro'] + 1
            except:
                _json['registro'] = 1
            print(_json)
            id = mongo.db.cargos.insert(_json)
            resp = jsonify('utils added successfully!')
            resp.status_code = 200
            return resp

        if id == "2":
            print("entro al if")
            lima = pytz.timezone('America/Lima')
            li_time = datetime.now(lima)
            _json['created_at'] = li_time
            _json['updated_at'] = li_time
            try:
                print("try")
                conteo = mongo.db.areas.find().sort('registro', -1).limit(1)
                conteo = list(conteo)
                print(conteo)
                _json['registro'] = conteo[0]['registro'] + 1
            except:
                _json['registro'] = 1
            print(_json)
            id = mongo.db.areas.insert(_json)
            resp = jsonify('utils added successfully!')
            resp.status_code = 200
            return resp
    except:
        # print(ValueError)
        # except:
        jsonResp = {
            "codRes": "99",
            "message": "{}".format("Error guarando su utils")
        }
        return jsonify(jsonResp)


# user = mongo.db.utils.find()
# print(list(user))
# print(user)
# resp = dumps(user)
# Converting string to list
# print(asd)


# @app.route('/cuidappte/utils', methods=['POST'])
# def add_utils():
#     import pytz
#     lima = pytz.timezone('America/Lima')
#     li_time = datetime.now(lima)
#     _json = request.json
#     _json['idUser'] = repararIdInput(_json['id'])
#     _json.pop('id')
#     _json.pop('codRes')
#     _json.pop('temp')
#
#     idAsist = mongo.db.utils.find({"idUser": _json['idUser']})
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
#             id = mongo.db.utils.insert(_json)
#             resp = jsonify('utils added successfully!')
#             resp.status_code = 200
#             return resp
#
#         if cantAsist == 1:
#             # fehcaEvaluarTest = _json['utils']['created_at']
#             # fehcaEvaluarTest = datetime.strptime(fehcaEvaluarTest, '')
#             # print(fehcaEvaluarTest)
#             # print("#############################", type(fehcaEvaluarTest))
#             # tz = pytz.timezone('America/St_Johns')
#             # fehcaEvaluarTest = fehcaEvaluarTest.replace(tzinfo=pytz.UTC)
#             # fehcaEvaluar = fehcaEvaluarTest.astimezone(lima)
#             # print(fehcaEvaluar)
#             mongo.db.utils.update_one({'idUser': _json['idUser']},
#                                            {'$push': {"archivos": {
#                                                "comentario": _json['comentario'],
#                                                "documento": _json['docs'],
#                                                "created_at": li_time
#                                            }}})
#             resp = jsonify('Update utils successfully!')
#             resp.status_code = 200
#             return resp
#         #     id = mongo.db.utils.insert(_json)
#         #     resp = jsonify('User added successfully!')
#         #     resp.status_code = 200
#         #     return resp
#     except:
#         # except:
#         jsonResp = {
#             "codRes": "99",
#             "message": "{}".format("Error guarando su utils")
#         }
#         return jsonify(jsonResp)
#     # user = mongo.db.utils.find()
#     # print(list(user))
#     # print(user)
#     # resp = dumps(user)
#     # Converting string to list
#     # print(asd)


@app.route('/cuidappte/utils', methods=['PUT'])
def put_utils():
    print("Consultando Creditos del ID: {}".format(id))
    user = mongo.db.utils.find()
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


@app.route('/cuidappte/utils/<tipo>/<id>', methods=['DELETE'])
def delete_utils(tipo, id):
    print(tipo)
    print(id)
    if tipo == 1:
        mongo.db.cargos.delete({'registro': id})
    if tipo == 2:
        mongo.db.areas.delete_one({'registro': id})
    resp = jsonify('registro eliminado correctamente!')
    resp.status_code = 200
    return resp
