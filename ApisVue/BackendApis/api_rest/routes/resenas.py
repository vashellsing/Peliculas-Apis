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

    if not datos or not all(
        k in datos for k in ("id_pelicula", "titulo", "comentario", "calificacion")
    ):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    id_pelicula = datos["id_pelicula"]

    try:
        cur = mysql.connection.cursor()

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
                return (
                    jsonify({"error": "Solo puedes dejar una reseña por película"}),
                    403,
                )

        # AÑADIDO: 'tituloComentario' en el INSERT
        sql = """
            INSERT INTO Comentarios 
            (id_peliculaComentario, id_usuarioComentario, calificacionComentario, tituloComentario, textoComentario)
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(
            sql,
            (
                id_pelicula,
                usuario_id,
                datos["calificacion"],
                datos["titulo"],
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


# ==========================================
# GET: OBTENER TODAS LAS RESEÑAS DE UNA PELÍCULA
# ==========================================


@resenas_bp.route("/resenas/<int:id_pelicula>", methods=["GET"])
@require_api_key
def obtener_resenas(id_pelicula):
    from app_peliculas import mysql

    try:
        cur = mysql.connection.cursor()

        # AQUÍ ESTÁ LA MAGIA: u.nombreUsuario y c.tituloComentario
        sql = """
            SELECT c.id_comentario, c.id_usuarioComentario, u.nombreUsuario, 
                   c.calificacionComentario, c.tituloComentario, c.textoComentario, c.fecha_creacion
            FROM comentarios c
            LEFT JOIN usuarios u ON c.id_usuarioComentario = u.id_usuario
            WHERE c.id_peliculaComentario = %s
            ORDER BY c.fecha_creacion DESC
        """
        cur.execute(sql, (id_pelicula,))
        datos = cur.fetchall()
        cur.close()

        comentarios = []
        for fila in datos:
            comentarios.append(
                {
                    "id": fila[0],
                    "id_usuario": fila[1],
                    "usuario": fila[2]
                    or f"Usuario #{fila[1]}",  # fila[2] ahora es u.nombreUsuario
                    "calificacion": fila[3],
                    "titulo": fila[4],
                    "texto": fila[5],
                    "fecha": fila[6].strftime("%d %b %Y") if fila[6] else "",
                }
            )

        return jsonify({"comentarios": comentarios}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# PUT: EDITAR UNA RESEÑA
# ==========================================
@resenas_bp.route("/resenas/<int:id_comentario>", methods=["PUT"])
@require_api_key
@require_jwt
@require_role(["usuario", "admin"])
def editar_resena(id_comentario):
    from app_peliculas import mysql

    datos = request.json
    usuario_id = request.current_user.get("id")

    try:
        cur = mysql.connection.cursor()

        # 1. Verificar que el comentario exista y pertenezca al usuario
        cur.execute(
            "SELECT id_usuarioComentario FROM Comentarios WHERE id_comentario = %s",
            (id_comentario,),
        )
        comentario = cur.fetchone()

        if not comentario:
            return jsonify({"error": "Comentario no encontrado"}), 404

        # Permitimos editar solo si es el dueño
        if comentario[0] != usuario_id:
            return (
                jsonify({"error": "No tienes permiso para editar este comentario"}),
                403,
            )

        # 2. Actualizar los datos
        sql = """
            UPDATE Comentarios 
            SET calificacionComentario = %s, tituloComentario = %s, textoComentario = %s 
            WHERE id_comentario = %s
        """
        cur.execute(
            sql,
            (
                datos["calificacion"],
                datos["titulo"],
                datos["comentario"],
                id_comentario,
            ),
        )
        mysql.connection.commit()
        cur.close()

        return jsonify({"mensaje": "Comentario actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# DELETE: ELIMINAR UNA RESEÑA
# ==========================================
@resenas_bp.route("/resenas/<int:id_comentario>", methods=["DELETE"])
@require_api_key
@require_jwt
@require_role(["usuario", "admin"])
def eliminar_resena(id_comentario):
    from app_peliculas import mysql

    usuario_id = request.current_user.get("id")
    usuario_rol = request.current_user.get("rol")

    try:
        cur = mysql.connection.cursor()

        # Verificar a quién pertenece el comentario
        cur.execute(
            "SELECT id_usuarioComentario FROM Comentarios WHERE id_comentario = %s",
            (id_comentario,),
        )
        comentario = cur.fetchone()

        if not comentario:
            return jsonify({"error": "Comentario no encontrado"}), 404

        # Solo el dueño o un admin pueden borrarlo
        if usuario_rol != "admin" and comentario[0] != usuario_id:
            return (
                jsonify({"error": "No tienes permiso para eliminar este comentario"}),
                403,
            )

        cur.execute(
            "DELETE FROM Comentarios WHERE id_comentario = %s", (id_comentario,)
        )
        mysql.connection.commit()
        cur.close()

        return jsonify({"mensaje": "Comentario eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
