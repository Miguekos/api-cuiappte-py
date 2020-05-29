from app import app
from flask import jsonify, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from mongo import mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_cors import CORS
import pytz
from datetime import datetime, timedelta

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


def FechaTodo():
    now = datetime.now()
    fechax = (now - timedelta(days=5))
    fechaa = (now - timedelta(days=4))
    fechab = (now - timedelta(days=3))
    fechac = (now - timedelta(days=2))
    fechad = (now - timedelta(days=1))
    fechae = (now - timedelta(days=0))
    graficDate = []
    graficDate.append(fechax.strftime('%m-%d'))
    graficDate.append(fechaa.strftime('%m-%d'))
    graficDate.append(fechab.strftime('%m-%d'))
    graficDate.append(fechac.strftime('%m-%d'))
    graficDate.append(fechad.strftime('%m-%d'))
    graficDate.append(fechae.strftime('%m-%d'))
    return graficDate

def CalcuarTodo(arg):
    now = datetime.now()
    from_date_x = []
    from_date_1 = []
    from_date_2 = []
    from_date_3 = []
    from_date_4 = []
    from_date_5 = []
    fechax = (now - timedelta(days=5))
    fechaa = (now - timedelta(days=4))
    fechab = (now - timedelta(days=3))
    fechac = (now - timedelta(days=2))
    fechad = (now - timedelta(days=1))
    fechae = (now - timedelta(days=0))
    # AllClientes = mongo.db.clientes.find()
    for post in arg:
        # from_date.append(post['created_at'].strftime("%Y-%m-%d"))
        # to_date.append(post['created_at'].strftime("%Y-%m-%d"))
        # print(post['created_at'].strftime("%Y-%m-%d"))
        # print(now.strftime("%Y-%m-%d"))
        # print(post['created_at'])
        fehcaEvaluar = post['created_at'] - timedelta(hours=5)
        if fehcaEvaluar.strftime("%Y-%m-%d") == fechax.strftime("%Y-%m-%d"):
            from_date_x.append(fehcaEvaluar.strftime("%Y-%m-%d"))
            # print("hoy")
            # print(fehcaEvaluar.strftime(

        elif fehcaEvaluar.strftime("%Y-%m-%d") == fechaa.strftime("%Y-%m-%d"):
            from_date_1.append(fehcaEvaluar.strftime("%Y-%m-%d"))
            # print("hoy - 1")
            # print(fehcaEvaluar.strftime(

        elif fehcaEvaluar.strftime("%Y-%m-%d") == fechab.strftime("%Y-%m-%d"):
            from_date_2.append(fehcaEvaluar.strftime("%Y-%m-%d"))
            # print("hoy - 2")
            # print(fehcaEvaluar.strftime(

        elif fehcaEvaluar.strftime("%Y-%m-%d") == fechac.strftime("%Y-%m-%d"):
            from_date_3.append(fehcaEvaluar.strftime("%Y-%m-%d"))
            # print("hoy - 3")
            # print(fehcaEvaluar.strftime(

        elif fehcaEvaluar.strftime("%Y-%m-%d") == fechad.strftime("%Y-%m-%d"):
            from_date_4.append(fehcaEvaluar.strftime("%Y-%m-%d"))
            # print("hoy - 4")
            # print(fehcaEvaluar.strftime(

        elif fehcaEvaluar.strftime("%Y-%m-%d") == fechae.strftime("%Y-%m-%d"):
            from_date_5.append(fehcaEvaluar.strftime("%Y-%m-%d"))
            # print("hoy - 5")

    print(from_date_x)
    print(from_date_1)
    print(from_date_2)
    print(from_date_3)
    print(from_date_4)
    print(from_date_5)
    graficSeria = []
    graficDate = []
    graficSeria.append(len(from_date_x))
    graficSeria.append(len(from_date_1))
    graficSeria.append(len(from_date_2))
    graficSeria.append(len(from_date_3))
    graficSeria.append(len(from_date_4))
    graficSeria.append(len(from_date_5))

    graficDate.append(fechax.strftime('%m-%d'))
    graficDate.append(fechaa.strftime('%m-%d'))
    graficDate.append(fechab.strftime('%m-%d'))
    graficDate.append(fechac.strftime('%m-%d'))
    graficDate.append(fechad.strftime('%m-%d'))
    graficDate.append(fechae.strftime('%m-%d'))

    # jsonRsult = {
    #     "asd" : graficSeria,
    #     "qwe" : graficDate
    # }
    return graficSeria



@app.route('/clientes/reporte')
def clientsReporte():
    clientes = mongo.db.clientes.count()
    clientesCS = mongo.db.clientes.count({"estados": "01"})
    clientesS = mongo.db.clientes.count({"estados": "00"})
    clientesC1 = mongo.db.clientes.count({"area": "Producción"})
    clientesC2 = mongo.db.clientes.count({"area": "Ventas"})
    clientesC3 = mongo.db.clientes.count({"area": "Administración"})
    clientesC4 = mongo.db.clientes.count({"area": "Gerencia"})

    # now = datetime.now()
    # from_date_x = []
    # from_date_1 = []
    # from_date_2 = []
    # from_date_3 = []
    # from_date_4 = []
    # from_date_5 = []
    # fechax = (now - timedelta(days=0))
    # fechaa = (now - timedelta(days=1))
    # fechab = (now - timedelta(days=2))
    # fechac = (now - timedelta(days=3))
    # fechad = (now - timedelta(days=4))
    # fechae = (now - timedelta(days=5))
    # AllClientes = mongo.db.clientes.find()
    # print(CalcuarTodo(mongo.db.clientes.find()))
    # for post in AllClientes:
    #     # from_date.append(post['created_at'].strftime("%Y-%m-%d"))
    #     # to_date.append(post['created_at'].strftime("%Y-%m-%d"))
    #     # print(post['created_at'].strftime("%Y-%m-%d"))
    #     # print(now.strftime("%Y-%m-%d"))
    #     # print(post['created_at'])
    #     fehcaEvaluar = post['created_at'] - timedelta(hours=5)
    #     if fehcaEvaluar.strftime("%Y-%m-%d") == fechax.strftime("%Y-%m-%d"):
    #         from_date_x.append(fehcaEvaluar.strftime("%Y-%m-%d"))
    #         # print("hoy")
    #         # print(fehcaEvaluar.strftime(
    #
    #     elif fehcaEvaluar.strftime("%Y-%m-%d") == fechaa.strftime("%Y-%m-%d"):
    #         from_date_1.append(fehcaEvaluar.strftime("%Y-%m-%d"))
    #         # print("hoy - 1")
    #         # print(fehcaEvaluar.strftime(
    #
    #     elif fehcaEvaluar.strftime("%Y-%m-%d") == fechab.strftime("%Y-%m-%d"):
    #         from_date_2.append(fehcaEvaluar.strftime("%Y-%m-%d"))
    #         # print("hoy - 2")
    #         # print(fehcaEvaluar.strftime(
    #
    #     elif fehcaEvaluar.strftime("%Y-%m-%d") == fechac.strftime("%Y-%m-%d"):
    #         from_date_3.append(fehcaEvaluar.strftime("%Y-%m-%d"))
    #         # print("hoy - 3")
    #         # print(fehcaEvaluar.strftime(
    #
    #     elif fehcaEvaluar.strftime("%Y-%m-%d") == fechad.strftime("%Y-%m-%d"):
    #         from_date_4.append(fehcaEvaluar.strftime("%Y-%m-%d"))
    #         # print("hoy - 4")
    #         # print(fehcaEvaluar.strftime(
    #
    #     elif fehcaEvaluar.strftime("%Y-%m-%d") == fechae.strftime("%Y-%m-%d"):
    #         from_date_5.append(fehcaEvaluar.strftime("%Y-%m-%d"))
    #         # print("hoy - 5")
    #
    # print(from_date_x)
    # print(from_date_1)
    # print(from_date_2)
    # print(from_date_3)
    # print(from_date_4)
    # print(from_date_5)
    # graficSeria = []
    # graficDate = []
    # graficSeria.append(len(from_date_x))
    # graficSeria.append(len(from_date_1))
    # graficSeria.append(len(from_date_2))
    # graficSeria.append(len(from_date_3))
    # graficSeria.append(len(from_date_4))
    # graficSeria.append(len(from_date_5))
    #
    # graficDate.append(fechax.strftime('%m-%d'))
    # graficDate.append(fechaa.strftime('%m-%d'))
    # graficDate.append(fechab.strftime('%m-%d'))
    # graficDate.append(fechac.strftime('%m-%d'))
    # graficDate.append(fechad.strftime('%m-%d'))
    # graficDate.append(fechae.strftime('%m-%d'))







    # i = 0
    # while i > 5:
    #     graficDate.append(now - timedelta(days=i))
    # print(from_date_count)
    # print(from_date_1_count)
    # print(from_date_2_count)
    # print(from_date_3_count)
    # print(from_date_4_count)
    # print(from_date_5_count)
    # jsonFechas = {
    #     "date": from_date_count,
    #     "date_1": from_date_1_count,
    #     "date_2": from_date_2_count,
    #     "date_3": from_date_3_count,
    #     "date_4": from_date_4_count,
    #     "date_5": from_date_5_count
    # }
    # print(jsonFechas)
    # print(list(AllClientes['created_at']))
    # fechaw = from_date[0].strftime("%Y-%m-%d")
    # print("{}".format(fechaw))
    # print(to_date[0])
    # from_date = datetime(2010, 12, 31, 12, 30, 30, 125000)
    # to_date = datetime(2011, 12, 31, 12, 30, 30, 125000)

    # fechas = mongo.db.clientes.find({"date": {"$gte": from_date[0], "$lt": to_date[0]}})
    # print(list(fechas))
    # print(datetime.now())
    # resp = dumps(users)
    resp = jsonify({
        "clientes": clientes,
        "clientesCS": clientesCS,
        "clientesS": clientesS,
        "clientesC1": clientesC1,
        "clientesC2": clientesC2,
        "clientesC3": clientesC3,
        "clientesC4": clientesC4,
        "graficSeriaCS": CalcuarTodo(mongo.db.clientes.find({"estados": "01"})),
        "graficSeriaS" : CalcuarTodo(mongo.db.clientes.find({"estados": "00"})),
        "graficDate" : FechaTodo()
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
    user = mongo.db.clientes.find({'dni': id})
    resp = dumps(user)
    return resp


@app.route('/cliente/update', methods=['POST'])
def update_client():
    _json = request.json
    print(_json)
    # _id = id
    _temp = _json['temp']
    _id = _json['_id']
    # _name = _json['name']
    # _email = _json['email']
    # _password = _json['pwd']
    # validate the received values
    # if _name and _email and _password and _id and request.method == 'PUT':
    # asd = {'_id': ObjectId("{}".format(id))}
    # print(asd)
    # do not save password as a plain text
    # save edits
    mongo.db.clientes.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                 {'$set': {'temp': _temp}})
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
