
from flask import Blueprint, jsonify

rutas = Blueprint("rutas", __name__)

@rutas.route("/api/peliculas", methods=["GET"])
def listar_peliculas():
    peliculas = []

    return jsonify(peliculas), 200
