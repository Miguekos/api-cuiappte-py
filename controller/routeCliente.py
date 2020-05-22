from app import app
from flask import jsonify, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from mongo import mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_cors import CORS
import pytz
from datetime import datetime

CORS(app, supports_credentials=True)


def calcuarDeuda(monto, porcent):
    return monto * (porcent / 100) + monto


# Rutas User
@app.route('/cliente/add', methods=['POST'])
def add_client():
    lima = pytz.timezone('America/Lima')
    li_time = datetime.now(lima)
    _json = request.json
    print(_json)
    # _name = _json['name']
    # _email = _json['email']
    # _password = _json['pwd']
    # validate the received values
    # if _name and _email and _password and request.method == 'POST':
    # do not save password as a plain text
    # _hashed_password = generate_password_hash(_password)
    # save details
    # id = mongo.db.clientes.insert({'name': "_name", 'email': "_email"})
    _json.update({"created_at": li_time})
    # _json.update({"deuda" : calcuarDeuda(_json['monto'], 20), "interes" : 20, "created_at" : li_time},)
    try:
        global id
        id = mongo.db.clientes.insert(_json)
        print(id)
        _jsonAlert = {
            "idCliente": id,
            "cantCreditos": 0,
            "diasMora": 0,
            "detalleMora": []
        }
        alert = mongo.db.alertas.insert(_jsonAlert)
        print("Respuesta de la alerta: {}".format(alert))
        resp = jsonify('{}'.format(id))
        resp.status_code = 200
        return resp
    except:
        user = mongo.db.clientes.find_one({'dni': _json['dni']})
        resp = dumps(user)
        if resp == "null":
            print("ValueError")
            jsonResp = {
                "codRes": "99",
                "message": "{}".format(id)
            }
            return jsonify(jsonResp)
        else:
            print("ValueError")
            jsonResp = {
                "codRes": "02",
                "message": "{}".format(id)
            }
            return jsonify(jsonResp)


@app.route('/clientes/reporte')
def clientsReporte():
    clientes = mongo.db.clientes.count()
    clientesCS = mongo.db.clientes.count({"estados": "01"})
    clientesS = mongo.db.clientes.count({"estados": "00"})
    clientesC1 = mongo.db.clientes.count({"area": "Producción"})
    clientesC2 = mongo.db.clientes.count({"area": "Ventas"})
    clientesC3 = mongo.db.clientes.count({"area": "Administración"})
    clientesC4 = mongo.db.clientes.count({"area": "Gerencia"})

    # resp = dumps(users)
    resp = jsonify({
        "clientes": clientes,
        "clientesCS": clientesCS,
        "clientesS": clientesS,
        "clientesC1": clientesC1,
        "clientesC2": clientesC2,
        "clientesC3": clientesC3,
        "clientesC4": clientesC4
    })
    return resp


@app.route('/clientes')
def clientsCS():
    users = mongo.db.clientes.find()
    resp = dumps(users)
    return resp


@app.route('/clientesCS')
def clientsS():
    users = mongo.db.clientes.find({"estados": "01"})
    resp = dumps(users)
    return resp


@app.route('/clientesS')
def clients():
    users = mongo.db.clientes.find({"estados": "00"})
    resp = dumps(users)
    return resp


@app.route('/cliente/<id>')
def client(id):
    user = mongo.db.clientes.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp


@app.route('/cliente/update/<id>', methods=['PUT'])
def update_client(id):
    _json = request.json
    # _id = _json['_id']
    # _name = _json['name']
    # _email = _json['email']
    # _password = _json['pwd']
    # validate the received values
    # if _name and _email and _password and _id and request.method == 'PUT':
    asd = {'_id': ObjectId("{}".format(id))}
    print(asd)
    # do not save password as a plain text
    # save edits
    mongo.db.clientes.update_one({'_id': ObjectId("{}".format(id))},
                                 {'$set': _json})
    resp = jsonify('User updated successfully!')
    resp.status_code = 200
    return resp
    # else:
    #     return not_found()


@app.route('/cliente/delete/<id>', methods=['DELETE'])
def delete_client(id):
    mongo.db.clientes.delete_one({'_id': ObjectId(id)})
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
