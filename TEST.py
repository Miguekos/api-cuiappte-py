from app import app
from flask import jsonify, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from mongo import mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_cors import CORS
import pytz
from datetime import datetime, timedelta



now = datetime.now()
# now = now.strftime("%Y-%m-%d")

print('hour:', now.today())
year = now.year
month = now.month
day = now.day

print(year)
print(month)
print(day)
now = now.strftime("%Y/%m/%d")
print("now", now)
asd = "2020-05-31 00:00:00"
from_date = datetime(2020, 5, 21, 00, 00, 00, 000000)
print(from_date)
to_date = datetime(year, month, day, 00, 00, 00, 000000)
print(to_date)


arg = mongo.db.clientes.find({"created_at": {"$gte": from_date, "$lt": to_date}})


# arg = mongo.db.clientes.find({"estados": "01"})
for post in arg:
    # from_date.append(post['created_at'].strftime("%Y-%m-%d"))
    # to_date.append(post['created_at'].strftime("%Y-%m-%d"))
    # print(post['created_at'].strftime("%Y-%m-%d"))
    # print(now.strftime("%Y-%m-%d"))
    # print(post['created_at'])
    # fehcaEvaluar = post['created_at']
    fehcaEvaluar = post
    print(fehcaEvaluar)