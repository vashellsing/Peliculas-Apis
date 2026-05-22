from flask import Blueprint, request, jsonify
from utils.auth import require_api_key, require_jwt, require_role

# Mantenemos el nombre del blueprint pero apuntamos a la tabla 'Comentarios'
resenas_bp = Blueprint("resenas_bp", __name__)



# ==========================================
# POST: DEJAR UN COMENTARIO / RESEÑA (ACTUALIZADO PARA PELÍCULAS Y SERIES)
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

    # Validamos que venga el contenido básico y al menos uno de los dos IDs
    if not datos or not all(
        k in datos for k in ("titulo", "comentario", "calificacion")
    ):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    if "id_pelicula" not in datos and "id_serie" not in datos:
        return jsonify({"error": "Debe especificar id_pelicula o id_serie"}), 400

    id_pelicula = datos.get("id_pelicula")
    id_serie = datos.get("id_serie")

    try:
        cur = mysql.connection.cursor()

        # LÓGICA DE NEGOCIO: Solo 1 reseña por usuario (si no es admin)
        if usuario_rol == "usuario":
            if id_pelicula:
                cur.execute(
                    "SELECT id_comentario FROM Comentarios WHERE id_usuarioComentario = %s AND id_peliculaComentario = %s",
                    (usuario_id, id_pelicula),
                )
            else:
                cur.execute(
                    "SELECT id_comentario FROM Comentarios WHERE id_usuarioComentario = %s AND id_serieComentario = %s",
                    (usuario_id, id_serie),
                )

            if cur.fetchone():
                cur.close()
                return (
                    jsonify({"error": "Ya has dejado una reseña aquí anteriormente"}),
                    403,
                )

        # INSERT: Usamos None para el campo que no se usa
        sql = """
            INSERT INTO Comentarios 
            (id_peliculaComentario, id_serieComentario, id_usuarioComentario, calificacionComentario, tituloComentario, textoComentario)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(
            sql,
            (
                id_pelicula,
                id_serie,
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
        return jsonify({"error": str(e)}), 500


# ==========================================
# GET: OBTENER TODAS LAS RESEÑAS DE UNA SERIE
# ==========================================
@resenas_bp.route("/resenas/serie/<int:id_serie>", methods=["GET"])
@require_api_key
def obtener_resenas_serie(id_serie):
    from app_peliculas import mysql

    try:
        cur = mysql.connection.cursor()
        sql = """
            SELECT c.id_comentario, c.id_usuarioComentario, u.nombreUsuario, 
                   c.calificacionComentario, c.tituloComentario, c.textoComentario, c.fecha_creacion
            FROM comentarios c
            LEFT JOIN usuarios u ON c.id_usuarioComentario = u.id_usuario
            WHERE c.id_serieComentario = %s
            ORDER BY c.fecha_creacion DESC
        """
        cur.execute(sql, (id_serie,))
        datos = cur.fetchall()
        cur.close()

        comentarios = [
            {
                "id": f[0],
                "id_usuario": f[1],
                "usuario": f[2] or f"Usuario #{f[1]}",
                "calificacion": f[3],
                "titulo": f[4],
                "texto": f[5],
                "fecha": f[6].strftime("%d %b %Y") if f[6] else "",
            }
            for f in datos
        ]

        return jsonify({"comentarios": comentarios}), 200
    except Exception as e:
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
