
from flask import Flask, jsonify


def crear_app():
    app = Flask(__name__)

    from app.rutas import rutas
    app.register_blueprint(rutas)

    @app.errorhandler(404)
    def no_encontrado(error):
        return jsonify({
            "error": "Recurso no encontrado"
        }), 404

    @app.errorhandler(405)
    def metodo_invalido(error):
        return jsonify({
            "error": "Método no permitido"
        }), 405

    @app.errorhandler(500)
    def error_interno(error):
        return jsonify({
            "error": "Error interno del servidor"
        }), 500

    return app
