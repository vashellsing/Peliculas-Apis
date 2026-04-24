from flask import Blueprint, request, jsonify
from utils.auth import require_api_key, require_jwt, require_role

resenas_bp = Blueprint("resenas_bp", __name__)


@resenas_bp.route("/resenas", methods=["POST"])
@require_api_key
@require_jwt
@require_role(["cliente", "admin"])  # Ambos pueden comentar
def dejar_resena():
    from app_peliculas import (
        mysql,
    )  # Asegúrate de apuntar a la app que tiene la conexión

    datos = request.json
    usuario_id = request.current_user.get("id")

    if not datos or not all(
        k in datos for k in ("id_pelicula", "comentario", "calificacion")
    ):
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO Resenas (id_usuarioResena, id_peliculaResena, comentarioResena, calificacionResena)
            VALUES (%s, %s, %s, %s)
        """,
            (
                usuario_id,
                datos["id_pelicula"],
                datos["comentario"],
                datos["calificacion"],
            ),
        )

        mysql.connection.commit()
        cur.close()
        return jsonify({"mensaje": "Reseña publicada con éxito"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@resenas_bp.route("/resenas/<int:id_pelicula>", methods=["GET"])
@require_api_key
def ver_resenas(id_pelicula):
    from app_peliculas import mysql

    # Esta es pública, cualquiera con API Key la ve
    cur = mysql.connection.cursor()
    cur.execute(
        """
        SELECT u.nombreUsuario, r.comentarioResena, r.calificacionResena 
        FROM Resenas r
        JOIN Usuarios u ON r.id_usuarioResena = u.id_usuario
        WHERE r.id_peliculaResena = %s
    """,
        (id_pelicula,),
    )

    resultados = cur.fetchall()
    cur.close()

    resenas = [{"usuario": r[0], "comentario": r[1], "nota": r[2]} for r in resultados]
    return jsonify({"peliculas_id": id_pelicula, "resenas": resenas}), 200
