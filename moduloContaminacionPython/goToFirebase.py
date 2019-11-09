import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('dogKey.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://airea-app.firebaseio.com/'
})

# Almacenar data en registro historico
def send(timestamp,param,value):
    dataSend = {}
    urlDevice = 'data' + param + "/"
    ref = db.reference(urlDevice)
    dataSend["timestamp"] = timestamp
    dataSend["values"] = value
    ref.push(dataSend)