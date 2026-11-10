
import os
import pymysql
from pymongo import MongoClient


def conectar():
    db = pymysql.connect(
        host="mysql",
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        cursorclass=pymysql.cursors.DictCursor
    )

    return db


def conectar_mongo():
    usuario = os.environ["MONGO_INITDB_ROOT_USERNAME"]
    clave = os.environ["MONGO_INITDB_ROOT_PASSWORD"]
    nombre = os.environ["MONGO_DATABASE"]

    uri = f"mongodb://{usuario}:{clave}@mongo:27017/?authSource=admin"

    cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)
    return cliente, cliente[nombre]
