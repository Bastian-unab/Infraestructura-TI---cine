
from flask import Flask

def crear_app():
    app = Flask(__name__)

    from app.rutas import rutas
    app.register_blueprint(rutas)

    return app
