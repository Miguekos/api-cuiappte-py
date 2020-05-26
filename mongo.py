from app import app
from flask_pymongo import PyMongo

app.secret_key = "secret key"
# app.config["MONGO_URI"] = "mongodb://95.111.235.214:32773/cuiappte"
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/cuiappte"
mongo = PyMongo(app)