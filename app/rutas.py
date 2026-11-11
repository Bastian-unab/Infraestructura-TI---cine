from flask import Blueprint, jsonify, request
from app import datos
from app.datos import conectar, conectar_mongo

rutas = Blueprint("rutas", __name__)

@rutas.route("/api/peliculas", methods=["GET"])
def listar_peliculas():
    db = conectar()

    try:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM peliculas")
            peliculas = cur.fetchall()

        return jsonify(peliculas), 200
    finally:
        db.close()


@rutas.route("/api/peliculas", methods=["POST"])
def crear_pelicula():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"error": "Se requiere un JSON válido"}), 400

    titulo = datos.get("titulo")
    duracion = datos.get("duracion")
    clasificacion = datos.get("clasificacion")

    if not isinstance(titulo, str) or not titulo.strip():
        return jsonify({"error": "El título es obligatorio"}), 400

    if type(duracion) is not int or duracion <= 0:
        return jsonify({"error": "La duración debe ser un entero positivo"}), 400

    if not isinstance(clasificacion, str) or not clasificacion.strip():
        return jsonify({"error": "La clasificación es obligatoria"}), 400

    titulo = titulo.strip()
    clasificacion = clasificacion.strip()

    if len(titulo) > 150 or len(clasificacion) > 20:
        return jsonify({"error": "Uno de los textos supera el límite permitido"}), 400

    db = conectar()

    try:
        with db.cursor() as cur:
            sql = """
                INSERT INTO peliculas (titulo, duracion, clasificacion)
                VALUES (%s, %s, %s)
            """

            cur.execute(sql, (titulo, duracion, clasificacion))
            db.commit()
            id = cur.lastrowid

        return jsonify({
            "id": id,
            "titulo": titulo,
            "duracion": duracion,
            "clasificacion": clasificacion
        }), 201
    finally:
        db.close()


@rutas.route("/api/peliculas/<int:id>", methods=["GET"])
def obtener_pelicula(id):
    db = conectar()

    try:
        with db.cursor() as cur:
            cur.execute(
                "SELECT * FROM peliculas WHERE id = %s",
                (id,)
            )
            pelicula = cur.fetchone()

        if pelicula is None:
            return jsonify({"error": "Película no encontrada"}), 404

        return jsonify(pelicula), 200
    finally:
        db.close()


@rutas.route("/api/peliculas/<int:id>", methods=["PATCH"])
def editar_pelicula(id):
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict) or not datos:
        return jsonify({"error": "Se requiere un JSON con datos"}), 400

    campos = {"titulo", "duracion", "clasificacion"}

    if not set(datos).issubset(campos):
        return jsonify({"error": "Campos no permitidos"}), 400

    if "titulo" in datos:
        if not isinstance(datos["titulo"], str) or not datos["titulo"].strip():
            return jsonify({"error": "Título inválido"}), 400
        datos["titulo"] = datos["titulo"].strip()

        if len(datos["titulo"]) > 150:
            return jsonify({"error": "Título demasiado largo"}), 400

    if "duracion" in datos:
        if type(datos["duracion"]) is not int or datos["duracion"] <= 0:
            return jsonify({"error": "Duración inválida"}), 400

    if "clasificacion" in datos:
        if not isinstance(datos["clasificacion"], str) or not datos["clasificacion"].strip():
            return jsonify({"error": "Clasificación inválida"}), 400
        datos["clasificacion"] = datos["clasificacion"].strip()

        if len(datos["clasificacion"]) > 20:
            return jsonify({"error": "Clasificación demasiado larga"}), 400

    db = conectar()

    try:
        with db.cursor() as cur:
            cur.execute("SELECT id FROM peliculas WHERE id = %s", (id,))

            if cur.fetchone() is None:
                return jsonify({"error": "Película no encontrada"}), 404

            columnas = ", ".join(f"{campo} = %s" for campo in datos)
            valores = list(datos.values()) + [id]

            cur.execute(
                f"UPDATE peliculas SET {columnas} WHERE id = %s",
                valores
            )

            db.commit()

            cur.execute("SELECT * FROM peliculas WHERE id = %s", (id,))
            pelicula = cur.fetchone()

        return jsonify(pelicula), 200
    finally:
        db.close()


@rutas.route("/api/resenas", methods=["GET"])
def listar_resenas():
    cliente, db = conectar_mongo()

    try:
        datos = db.resenas.find()
        resenas = []

        for resena in datos:
            resena["id"] = str(resena.pop("_id"))
            resenas.append(resena)


        return jsonify(resenas), 200
    finally:
        cliente.close()


@rutas.route("/api/resenas", methods=["POST"])
def crear_resena():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"error": "Se requiere un JSON válido"}), 400

    id = datos.get("pelicula_id")
    nota = datos.get("calificacion")
    comentario = datos.get("comentario")
    aspectos = datos.get("aspectos")

    if type(id) is not int or id <= 0:
        return jsonify({"error": "ID de película inválido"}), 400

    if type(nota) is not int or not 1 <= nota <= 5:
        return jsonify({"error": "La calificación debe estar entre 1 y 5"}), 400

    if comentario is not None:
        if not isinstance(comentario, str) or len(comentario) > 500:
            return jsonify({"error": "Comentario inválido"}), 400

    if aspectos is not None:
        if not isinstance(aspectos, list):
            return jsonify({"error": "Los aspectos deben ser una lista"}), 400

        if len(aspectos) > 10 or any(
            not isinstance(a, str) or not a.strip() or len(a) > 50
            for a in aspectos
        ):
            return jsonify({"error": "Aspectos inválidos"}), 400

    db = conectar()

    try:
        with db.cursor() as cur:
            cur.execute(
                "SELECT id FROM peliculas WHERE id = %s",
                (id,)
            )
            pelicula = cur.fetchone()

        if pelicula is None:
            return jsonify({"error": "Película no encontrada"}), 404
    finally:
        db.close()

    resena = {
        "pelicula_id": id,
        "calificacion": nota
    }

    if comentario is not None:
        resena["comentario"] = comentario

    if aspectos is not None:
        resena["aspectos"] = aspectos

    cliente, mongo = conectar_mongo()

    try:
        resultado = mongo.resenas.insert_one(resena)
        resena["id"] = str(resultado.inserted_id)
        resena.pop("_id", None)

        return jsonify(resena), 201
    finally:
        cliente.close()


@rutas.route("/api/peliculas/<int:id>/resenas", methods=["GET"])
def obtener_resenas_pelicula(id):
    db = conectar()

    try:
        with db.cursor() as cur:
            cur.execute(
                "SELECT * FROM peliculas WHERE id = %s",
                (id,)
            )
            pelicula = cur.fetchone()
    finally:
        db.close()

    if pelicula is None:
        return jsonify({"error": "Película no encontrada"}), 404

    cliente, mongo = conectar_mongo()

    try:
        datos = mongo.resenas.find({"pelicula_id": id})
        resenas = []

        for resena in datos:
            resena["id"] = str(resena.pop("_id"))
            resenas.append(resena)

    finally:
        cliente.close()

    return jsonify({
        "pelicula": pelicula,
        "resenas": resenas,
        "total_resenas": len(resenas)
    }), 200
