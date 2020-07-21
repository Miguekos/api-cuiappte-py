from datetime import datetime, timedelta

import pytz
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from flask import jsonify, request
from flask_cors import CORS

from app import app
from mongo import mongo

CORS(app, supports_credentials=True)


def calcuarDeuda(monto, porcent):
    return monto * (porcent / 100) + monto


# Rutas User
@app.route('/cuidappte/cliente/add', methods=['POST'])
def add_client():
    lima = pytz.timezone('America/Lima')
    li_time = datetime.now(lima)
    _json = request.json
    print(_json)
    _json.pop('_id')
    _json.pop('pwd')
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
    except ValueError:
        print(ValueError)
        # user = mongo.db.clientes.find_one({'dni': _json['dni']})
        # resp = dumps(user)
        # if resp == "null":
        #     print("ValueError")
        #     jsonResp = {
        #         "codRes": "99",
        #         "message": "{}".format(id)
        #     }
        #     return jsonify(jsonResp)
        # else:
        #     print("ValueError")
        #     jsonResp = {
        #         "codRes": "02",
        #         "message": "{}".format(id)
        #     }
        #     return jsonify(jsonResp)


def FechaTodo():
    lima = pytz.timezone('America/Lima')
    now = datetime.now(lima)
    print("FechaTodo", now)
    _json = request.json
    # print("FechaTodo", now)
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


def CalcuarTodoUpdate(arg):
    # print(arg)
    lima = pytz.timezone('America/Lima')
    now = datetime.now(lima)
    print(datetime.now())
    print("CalcuarTodo", now)
    # print("CalcuarTodo", now)
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
        # fehcaEvaluar = post['created_at'] - timedelta(hours=5)
        fehcaEvaluarTest = post['updated_at']
        # print("#############################", type(fehcaEvaluarTest))
        # tz = pytz.timezone('America/St_Johns')
        fehcaEvaluarTest = fehcaEvaluarTest.replace(tzinfo=pytz.UTC)
        fehcaEvaluar = fehcaEvaluarTest.astimezone(lima)
        # print(fehcaEvaluar)
        # print(datetime(fehcaEvaluarTest, tzinfo=lima).strftime("%Y-%m-%d"))
        # print(fehcaEvaluar)
        # print(post['_id'])
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

    # print(from_date_x)
    # print(from_date_1)
    # print(from_date_2)
    # print(from_date_3)
    # print(from_date_4)
    # print(from_date_5)
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


def CalcuarTodo(arg):
    # print(arg)
    lima = pytz.timezone('America/Lima')
    now = datetime.now(lima)
    print(datetime.now())
    print("CalcuarTodo", now)
    # print("CalcuarTodo", now)
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
        # fehcaEvaluar = post['created_at'] - timedelta(hours=5)
        fehcaEvaluarTest = post['created_at']
        # print("#############################", type(fehcaEvaluarTest))
        # tz = pytz.timezone('America/St_Johns')
        fehcaEvaluarTest = fehcaEvaluarTest.replace(tzinfo=pytz.UTC)
        fehcaEvaluar = fehcaEvaluarTest.astimezone(lima)
        # print(fehcaEvaluar)
        # print(datetime(fehcaEvaluarTest, tzinfo=lima).strftime("%Y-%m-%d"))
        # print(fehcaEvaluar)
        # print(post['_id'])
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

    # print(from_date_x)
    # print(from_date_1)
    # print(from_date_2)
    # print(from_date_3)
    # print(from_date_4)
    # print(from_date_5)
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


@app.route('/cuidappte/clientes/reporte')
def clientsReporte():
    asd = CalcuarTodo(mongo.db.clientes.find({"estados": "00"}))

    qwe = CalcuarTodo(mongo.db.clientes.find({"estados": "01"}))
    # print(qwe)
    # seguimientoF = mongo.db.seguimiento.find({"seguimiento": 1})
    # countSegui = len(list(seguimientoF))
    # print("asdasdasdasdasdasd",len(list(seguimientoF)))
    seguimiento = CalcuarTodo(mongo.db.seguimiento.find({"seguimiento": 1}))
    # print("seguimiento", list(seguimiento))
    # print("countSegui", countSegui)

    # dealtaF = mongo.db.seguimiento.find({"dealta": 1})
    # countDealta = len(list(dealtaF))
    dealta = CalcuarTodoUpdate(mongo.db.seguimiento.find({"dealta": 1}))
    # print("countDealta", countDealta)

    ps = mongo.db.clientes.count({"estados": "00"})
    pcs = mongo.db.clientes.count({"estados": "01"})
    countSegui = mongo.db.seguimiento.count({"seguimiento": 1})
    countAlta = mongo.db.seguimiento.count({"dealta": 1})
    #
    # countPCS = len(list(pcs))
    # countPS = len(list(ps))

    resp = jsonify({
        "clientes": pcs + ps,
        "clientesCS": int("{:.0f}".format(pcs * 100 / (pcs + ps))),
        "clientesS": int("{:.0f}".format(ps * 100 / (pcs + ps))),
        # # "clientesC1": clientesC1,
        # # "clientesC2": clientesC2,
        # # "clientesC3": clientesC3,
        # # "clientesC4": clientesC4,
        "graficSeriaCS": qwe,
        "graficSeriaS": asd,
        "seguimiento": countAlta + countSegui,
        "seguimientoCAlta": int("{:.0f}".format(countAlta * 100 / (countAlta + countSegui))),
        "seguimientoCSegui": int("{:.0f}".format(countSegui * 100 / (countAlta + countSegui))),
        "graficSeguimiento": seguimiento,
        "graficDeAlta": dealta,
        "graficDate": FechaTodo()
    })
    return resp


@app.route('/cuidappte/notification')
def notificaciones():
    import pytz
    lima = pytz.timezone('America/Lima')
    li_time = datetime.now() - timedelta(days=2)
    li_time_fin = datetime.now() - timedelta(days=0)
    print(li_time)
    print(li_time_fin)
    ini_date = li_time.strftime("%d/%m/%Y")
    fin_date = li_time_fin.strftime("%d/%m/%Y")
    in_time_obj = datetime.strptime("{} 00:00:00".format(ini_date), '%d/%m/%Y %H:%M:%S')
    out_time_obj = datetime.strptime("{} 23:59:59".format(fin_date), '%d/%m/%Y %H:%M:%S')
    conSintomas = mongo.db.clientes.find({'estados': "01", "created_at": {"$gte": in_time_obj, "$lt": out_time_obj}})
    EnCuidate = mongo.db.seguimiento.find({"created_at": {"$gte": in_time_obj, "$lt": out_time_obj}})
    mongo.db.notificaciones_consintomas.insert_many(list(conSintomas))
    mongo.db.notificaciones_cuidate.insert_many(list(EnCuidate))
    # print(list(conSintomas))
    # jsonResponse = {
    #     "ConSintomas": jsonify(conSintomas),
    #     "EnCuidate": "{}".format(EnCuidate)
    # }
    resp = jsonify("Notificaciones generadas")
    resp.status_code = 200
    return resp

@app.route('/cuidappte/clientes/reporte/order')
def clientsReporteOrder():
    # user = mongo.db.clientes.find()
    agr = [
        {
            '$group':
                {
                    '_id': {'dni': '$dni', 'enfermo': '$estados'}, 'personal': {'$push': "$$ROOT"},
                    "estados": {"$push": "$estados"},
                    "nombre": {"$last": "$nombre"},
                    "ultimaFecha": {"$last": "$created_at"},
                    "ulrimoEstado": {"$last": "$estados"},
                    "count": {"$sum": 1}
                }
        }
        # {'$addFields':
        #     {
        #         'estados': {'$addToSet': "$estados"}
        #     }
        # },
    ]

    # agr = [
    #     {
    #         '$group':
    #             {
    #                 '_id': '$dni', 'enformo': '$estados', 'personal': {'$push': "$$ROOT"},
    #                 "estados": {"$push": "$estados"},
    #                 "nombre": {"$last": "$nombre"},
    #                 "ultimaFecha": {"$last": "$created_at"},
    #                 "ulrimoEstado": {"$last": "$estados"},
    #                 "count": {"$sum": 1}
    #             }
    #     }
    #     # {'$addFields':
    #     #     {
    #     #         'estados': {'$addToSet': "$estados"}
    #     #     }
    #     # },
    # ]

    val = list(mongo.db.clientes.aggregate(agr))
    # print(val)
    return dumps(val)

    # print(arg)
    # print(asd)
    # for post in asd:
    #     # from_date.append(post['created_at'].strftime("%Y-%m-%d"))
    #     # to_date.append(post['created_at'].strftime("%Y-%m-%d"))
    #     # print(post['created_at'].strftime("%Y-%m-%d"))
    #     # print(now.strftime("%Y-%m-%d"))
    #     print(post)

    # print(qwe)

    # ps = mongo.db.clientes.count({"estados": "00"})
    # pcs = mongo.db.clientes.count({"estados": "01"})
    #
    # countPCS = len(list(pcs))
    # countPS = len(list(ps))

    # resp = jsonify({
    #     "clientes": pcs + ps,
    #     "clientesCS": "{:.0f}".format(pcs * 100 / (pcs + ps)),
    #     "clientesS": "{:.0f}".format(ps * 100 / (pcs + ps)),
    #     # # "clientesC1": clientesC1,
    #     # # "clientesC2": clientesC2,
    #     # # "clientesC3": clientesC3,
    #     # # "clientesC4": clientesC4,
    #     "graficSeriaCS": qwe,
    #     "graficSeriaS": asd,
    #     "graficDate": FechaTodo()
    # })
    # return resp


@app.route('/cuidappte/clientes')
def clients():
    users = mongo.db.clientes.find()
    resp = dumps(users)
    return resp


@app.route('/cuidappte/clientesCS')
def clientsCS():
    users = mongo.db.clientes.find({"estados": "01"})
    respuesta = list(users)
    print(len(respuesta))
    return dumps(respuesta)
    # resp = list(users)
    # print(resp)
    # return resp

@app.route('/cuidappte/clientesCSUser', methods=['POST'])
def clientsCSUser():
    _json = request.json
    print(_json)
    users = mongo.db.clientes.find({"estados": "01", "jefeDirecto": _json['dni']})
    respuesta = list(users)
    print(len(respuesta))
    return dumps(respuesta)

@app.route('/cuidappte/clientesS')
def clientsS():
    users = mongo.db.clientes.find({"estados": "00"})
    respuesta = list(users)
    print(len(respuesta))
    return dumps(respuesta)

@app.route('/cuidappte/clientesSUser', methods=['POST'])
def clientsSUser():
    _json = request.json
    print(_json)
    users = mongo.db.clientes.find({"estados": "00", "jefeDirecto": _json['dni']})
    respuesta = list(users)
    print(len(respuesta))
    return dumps(respuesta)


@app.route('/cuidappte/cliente/validar/<id>', methods=['GET'])
def client_validar(id):
    import pytz
    lima = pytz.timezone('America/Lima')
    li_time = datetime.now()
    ini_date = li_time.strftime("%d/%m/%Y")
    fin_date = li_time.strftime("%d/%m/%Y")
    in_time_obj = datetime.strptime("{} 00:00:00".format(ini_date), '%d/%m/%Y %H:%M:%S')
    out_time_obj = datetime.strptime("{} 23:59:59".format(fin_date), '%d/%m/%Y %H:%M:%S')
    user = mongo.db.clientes.find({'dni': id, "created_at": {"$gte": in_time_obj, "$lt": out_time_obj}})
    resp = dumps(user)
    print(resp)
    return resp


@app.route('/cuidappte/cliente/<id>')
def client(id):
    user = mongo.db.clientes.find({'dni': id})
    resp = dumps(user)
    return resp


@app.route('/cuidappte/cliente/update', methods=['POST'])
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


@app.route('/cuidappte/cliente/delete/<id>', methods=['DELETE'])
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
