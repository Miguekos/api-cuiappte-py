from flask import Flask, Blueprint

# blueprint = Blueprint('blueprint',__name__,template_folder='templates')
app = Flask(__name__)
# app.register_blueprint(blueprint, url_prefix='/blue')
# bp = Blueprint('burritos', __name__)
# app.register_blueprint(bp, url_prefix='/abc/123')

# @blueprint.route('/asdasd')
# def show():
#     return 'Hola blue print'

import controller.routeUsers
import controller.routeCliente
import controller.routeCreditos
import controller.routeAbonos
import controller.routeSeguimiento
import controller.routeAsistencia
import controller.routeDoc
import serverfile