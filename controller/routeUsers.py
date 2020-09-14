import random
import string
from datetime import datetime

import pytz
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

import funciones
from app import app
from mongo import mongo

CORS(app, supports_credentials=True)


# @app.route("/")
# def index():
#     return "The URL for this page is {}".format(url_for("index"))

def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


# Rutas User
@app.route('/cuidappte/user/add', methods=['POST'])
def add_user():
    lima = pytz.timezone('America/Lima')
    li_time = datetime.now(lima)
    _json = request.json
    _name = _json['name']
    _telefono = _json['telefono']
    _email = _json['email']
    _dni = _json['dni']
    _area = _json['area']
    _url = 'https://api.apps.com.pe/uploads/'
    _role = _json['role']
    _temp = _json['temp']
    _jefeDirecto = _json['jefeDirecto']
    _edad = _json['edad']
    _sexo = _json['sexo']
    _departamento = _json['departamento']
    _cargo = _json['cargo']
    _sueldo = _json['sueldo']

    _medico = 0
    _certificado = ""
    _seguimiento = 0
    _dealta = 0
    _profile = 'boy-avatar.png'
    global _password
    # _password = _json['pwd']
    _password = random_char(6)
    # if len(_password) == 0:
    #     _password = 'secret'
    # else:
    #     _password = _json['pwd']
    # validate the received values
    if _name and _email and _password and request.method == 'POST':

        # do not save password as a plain text
        _hashed_password = generate_password_hash(_password)
        # save details
        try:
            funciones.enviarCorreo(_email, _name, _password)
            id = mongo.db.user.insert(
                {'name': _name,
                 'dni': _dni,
                 'email': _email,
                 'telefono': _telefono,
                 'profile': _profile,
                 'url': _url,
                 'role': _role,
                 'seguimiento': _seguimiento,
                 'dealta': _dealta,
                 'certificado': _certificado,
                 'area': _area,
                 'temp': _temp,
                 'medico': _medico,
                 'edad': _edad,
                 'sexo': _sexo,
                 'departamento': _departamento,
                 'cargo': _cargo,
                 'sueldo': _sueldo,
                 "jefeDirecto": _jefeDirecto,
                 'pwd': _hashed_password, "created_at": li_time
                 })
            resp = jsonify('User added successfully!')
            resp.status_code = 200
            return resp
        except:
            user = mongo.db.user.find_one({"dni": _json['dni']})
            # userd = list(user)
            userd = dict(user)
            # print(dumps(userd))
            # return dumps(userd)
            # return [dict(mongo.db.user.find_one({"dni" : _json['dni']}))]
            if (userd):
                jsonResp = {
                    "codRes": "02",
                    "message": "{}".format(userd)
                }
                return dumps(jsonResp)
            else:
                jsonResp = {
                    "codRes": "99",
                    "message": "{}".format(userd)
                }
                return jsonify(jsonResp)
    else:
        return not_found()


@app.route('/cuidappte/login', methods=["POST"])
def login():
    _json = request.json
    try:
        emailCustom = _json["email"].casefold()
        emailCustom = emailCustom.strip()
        _user = mongo.db.user.find_one({
            'email': emailCustom
        })
        print("_user", type(_user))
        if _user != None:
            validar = check_password_hash(_user['pwd'], _json["pwd"])
            print("validar", validar)
            if validar == True:
                idUser = _user['_id']
                print(idUser)
                jsonFinal = {
                    "codRes": "00",
                    "id": idUser,
                    "name": _user['name'],
                    "email": _user['email'],
                    "dni": _user['dni'],
                    "telefono": _user['telefono'],
                    "url": _user['url'],
                    "profile": _user['profile'],
                    "area": _user['area'],
                    "role": _user['role'],
                    "temp": _user['temp']
                }
                return dumps(jsonFinal)
            else:
                jsonFinal = {
                    "codRes": "01",
                    "message": "Password Incorrecto"
                }
                resp = jsonify(jsonFinal)
                resp.status_code = 200
                return resp
        else:
            jsonFinal = {
                "codRes": "01",
                "message": "Email Incorrecto"
            }
            resp = jsonify(jsonFinal)
            resp.status_code = 200
            return resp
    except ValueError:
        print(ValueError)
        # jsonFinal = {
        #     "codRes": "99",
        #     "message": "ErrorControlado"
        # }
        # resp = jsonify(jsonFinal)
        # resp.status_code = 200
        # return resp


@app.route('/cuidappte/user/users')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp


@app.route('/cuidappte/user/<id>')
def user(id):
    print(id)
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    # print(list(user))
    resp = dumps(user)
    return resp


@app.route('/cuidappte/user/temp', methods=['PUT'])
def update_user_temp():
    _json = request.json
    _id = _json['_id']
    _temp = _json['temp']
    # validate the received values
    # save edits
    mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                             {'$set': {'temp': _temp}})
    resp = jsonify('User updated successfully!')
    resp.status_code = 200
    return resp


@app.route('/cuidappte/user/updateImage', methods=['PUT'])
def update_user_updateImage():
    _json = request.json
    _id = _json['_id']
    _profile = _json['profile']
    # validate the received values
    # save edits
    mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                             {'$set': {'profile': _profile}})
    resp = jsonify('User updated successfully!')
    resp.status_code = 200
    return resp


@app.route('/cuidappte/user/certificado', methods=['PUT'])
def update_user_certificado():
    _json = request.json
    _id = _json['_id']
    _certificado = _json['certificado']
    # validate the received values
    # save edits
    mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                             {'$set': {'certificado': _certificado}})
    resp = jsonify('User updated successfully!')
    resp.status_code = 200
    return resp


@app.route('/cuidappte/user/update', methods=['PUT'])
def update_user():
    _json = request.json
    _id = _json['_id']
    _name = _json['name']
    _email = _json['email']
    _telefono = _json['telefono']
    _dni = _json['dni']
    _profile = _json['profile']
    _edad = _json['edad']
    _role = _json['role']
    _sexo = _json['sexo']
    _departamento = _json['departamento']
    _cargo = _json['cargo']
    _area = _json['area']
    _jefeDirecto = _json['jefeDirecto']
    _sueldo = _json['sueldo']
    _medico = _json['medico']
    _password = _json['pwd']
    # validate the received values
    if _name and _email and _id and request.method == 'PUT':
        # do not save password as a plain text
        global jsonUpdate, _hashed_password
        if len(_password) == 0:
            jsonUpdate = {'name': _name,
                          'dni': _dni,
                          'email': _email,
                          'telefono': _telefono,
                          'role': _role,
                          'profile': _profile,
                          'medico': _medico,
                          'edad': _edad,
                          'sexo': _sexo,
                          'departamento': _departamento,
                          'cargo': _cargo,
                          'area': _area,
                          'sueldo': _sueldo,
                          'jefeDirecto' : _jefeDirecto
                          }
        else:
            _hashed_password = generate_password_hash(_password)
            jsonUpdate = {'name': _name,
                          'dni': _dni,
                          'email': _email,
                          'telefono': _telefono,
                          'role': _role,
                          'profile': _profile,
                          'medico': _medico,
                          'edad': _edad,
                          'sexo': _sexo,
                          'departamento': _departamento,
                          'cargo': _cargo,
                          'sueldo': _sueldo,
                          'jefeDirecto': _jefeDirecto,
                          'pwd': _hashed_password}
        # save edits
        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                 {'$set': jsonUpdate})
        resp = jsonify('User updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/cuidappte/user/recuperar', methods=['PUT'])
def recuperar_user():
    _json = request.json
    emailCustom = _json["email"].casefold()
    emailCustom = emailCustom.strip()
    buscarCliente = mongo.db.user.find_one({'email': emailCustom})
    try:
        buscarCliente = dict(buscarCliente)
        print(buscarCliente)
        # return jsonify("Tu correo existe")
        # validate the received values
        _password = random_char(6)
        # do not save password as a plain text
        try:
            funciones.enviarCorreo(emailCustom, buscarCliente['name'], _password)
            global jsonUpdate, _hashed_password
            _hashed_password = generate_password_hash(_password)
            jsonUpdate = {'pwd': _hashed_password}
            # save edits
            mongo.db.user.update_one({'email': emailCustom},
                                     {'$set': jsonUpdate})
            resp = {
                "codRes": "00",
                "message": "{}".format("Pass generada correctamente")
            }
            return jsonify(resp)
        except:
            return jsonify("No se pudo generar el nuevo pass")
    except:
        jsonResp = {
            "codRes": "01",
            "message": "{}".format("Correo no existe")
        }
        return jsonify(jsonResp)


@app.route('/cuidappte/user/updateall', methods=['PUT'])
def update_user_general():
    _json = request.json

    # do not save password as a plain text
    global jsonUpdate, _hashed_password
    if len(_password) == 0:
        jsonUpdate = {'name': _name, 'dni': _dni, 'email': _email, 'telefono': _telefono, 'profile': _profile}
    else:
        _hashed_password = generate_password_hash(_password)
        jsonUpdate = {'name': _name, 'dni': _dni, 'email': _email, 'telefono': _telefono, 'profile': _profile,
                      'pwd': _hashed_password}
    # save edits
    mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                             {'$set': jsonUpdate})
    resp = jsonify('User updated successfully!')
    resp.status_code = 200
    return resp


@app.route('/cuidappte/user/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id': ObjectId(id)})
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
