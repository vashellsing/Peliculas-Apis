from flask import Blueprint, request, jsonify
from utils.auth import require_api_key, require_jwt, require_role

# Mantenemos el nombre del blueprint pero apuntamos a la tabla 'Comentarios'
resenas_bp = Blueprint("resenas_bp", __name__)


# ==========================================
# POST: DEJAR UN COMENTARIO / RESEÑA
# ==========================================
@resenas_bp.route("/resenas", methods=["POST"])
@require_api_key
@require_jwt
@require_role(["usuario", "admin"])  
def dejar_resena():
    from app_peliculas import mysql

    datos = request.json
    usuario_id = request.current_user.get("id")
    usuario_rol = request.current_user.get("rol") 

    if not datos or not all(k in datos for k in ("id_pelicula", "comentario", "calificacion")):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    id_pelicula = datos["id_pelicula"]

    try:
        cur = mysql.connection.cursor()

        # Solo aplicamos la restricción si el rol es 'usuario'
        # Los 'admin' se saltan esta validación automáticamente
        if usuario_rol == "usuario":
            query_check = """
                SELECT id_peliculaComentario 
                FROM Comentarios 
                WHERE id_usuarioComentario = %s AND id_peliculaComentario = %s
            """
            cur.execute(query_check, (usuario_id, id_pelicula))
            existe = cur.fetchone()

            if existe:
                cur.close()
                return jsonify({"error": "Solo puedes dejar una reseña por película"}), 403

        # Inserción de la reseña
        sql = """
            INSERT INTO Comentarios 
            (id_peliculaComentario, id_usuarioComentario, calificacionComentario, textoComentario)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(
            sql,
            (
                id_pelicula,
                usuario_id,
                datos["calificacion"],
                datos["comentario"],
            ),
        )

        mysql.connection.commit()
        cur.close()
        return jsonify({"mensaje": "Comentario publicado con éxito"}), 201

    except Exception as e:
        if "foreign key constraint fails" in str(e).lower():
            return jsonify({"error": "La película no existe"}), 400
        return jsonify({"error": str(e)}), 500