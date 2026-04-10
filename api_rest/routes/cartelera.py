from flask import Blueprint, request, jsonify

# Creamos el Blueprint para la cartelera
cartelera_bp = Blueprint("cartelera_bp", __name__)


# ==========================================
# TRAER TODA LA CARTELERA (GET)
# ==========================================
@cartelera_bp.route("/cartelera", methods=["GET"])
def obtener_cartelera():
    from app_cartelera import mysql

    try:
        cur = mysql.connection.cursor()
        # Usamos JOIN para traer el título de la película y el nombre del cine
        cur.execute(
            """
            SELECT c.id_cartelera, p.titulo, cin.nombreCine, cin.ciudadCine, 
                   c.fecha_horaCartelera, c.idioma_proyeccionCartelera 
            FROM Carteleras c
            INNER JOIN Peliculas p ON c.id_peliculaCartelera = p.id_pelicula
            INNER JOIN Cines cin ON c.id_cineCartelera = cin.id_cine
            ORDER BY c.fecha_horaCartelera ASC
        """
        )

        datos = cur.fetchall()
        cur.close()

        funciones = []
        for fila in datos:
            funciones.append(
                {
                    "id_cartelera": fila[0],
                    "pelicula": fila[1],
                    "cine": fila[2],
                    "ciudad": fila[3],
                    "fecha_hora": fila[4].strftime("%Y-%m-%d %H:%M:%S"),
                    "idioma": fila[5],
                }
            )

        return jsonify({"cartelera": funciones}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# AGREGAR NUEVA FUNCIÓN (POST)
# ==========================================
@cartelera_bp.route("/cartelera", methods=["POST"])
def crear_funcion():
    from app_cartelera import mysql

    datos = request.json

    # Validación estricta de campos obligatorios
    if not datos or not all(
        k in datos for k in ("id_pelicula", "id_cine", "fecha_hora", "idioma")
    ):
        return (
            jsonify(
                {
                    "error": "Faltan datos. Requiere: id_pelicula, id_cine, fecha_hora, idioma"
                }
            ),
            400,
        )

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO Carteleras (id_peliculaCartelera, id_cineCartelera, fecha_horaCartelera, idioma_proyeccionCartelera) 
            VALUES (%s, %s, %s, %s)
        """,
            (
                datos["id_pelicula"],
                datos["id_cine"],
                datos["fecha_hora"],
                datos["idioma"],
            ),
        )

        mysql.connection.commit()
        cur.close()

        return jsonify({"mensaje": "Función programada en cartelera exitosamente"}), 201
    except Exception as e:
        # Por si envían un ID de película o cine que no existe (Error de llave foránea)
        if "foreign key constraint fails" in str(e).lower():
            return jsonify({"error": "El ID de la película o del cine no existe"}), 400
        return jsonify({"error": str(e)}), 500


# ==========================================
# UPDATE: ACTUALIZAR FUNCIÓN (PUT)
# ==========================================
@cartelera_bp.route("/cartelera/<int:id_cartelera>", methods=["PUT"])
def actualizar_funcion(id_cartelera):
    from app_cartelera import mysql

    datos = request.json

    # Validamos qué enviaron
    if not datos or not all(
        k in datos for k in ("id_pelicula", "id_cine", "fecha_hora", "idioma")
    ):
        return jsonify({"error": "Faltan datos para actualizar"}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE Carteleras 
            SET id_peliculaCartelera=%s, id_cineCartelera=%s, fecha_horaCartelera=%s, idioma_proyeccionCartelera=%s 
            WHERE id_cartelera=%s
        """,
            (
                datos["id_pelicula"],
                datos["id_cine"],
                datos["fecha_hora"],
                datos["idioma"],
                id_cartelera,
            ),
        )

        mysql.connection.commit()

        # Validamos si realmente se actualizó algo
        if cur.rowcount == 0:
            return jsonify({"error": "La función en cartelera no existe"}), 404

        cur.close()
        return (
            jsonify({"mensaje": "Función en cartelera actualizada correctamente"}),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ELIMINAR FUNCIÓN (DELETE)
# ==========================================
@cartelera_bp.route("/cartelera/<int:id_cartelera>", methods=["DELETE"])
def eliminar_funcion(id_cartelera):
    from app_cartelera import mysql

    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Carteleras WHERE id_cartelera = %s", (id_cartelera,))
        mysql.connection.commit()

        # Validamos si existía el registro antes de borrarlo
        if cur.rowcount == 0:
            return jsonify({"error": "La función que intentas borrar no existe"}), 404

        cur.close()
        return (
            jsonify({"mensaje": "Función eliminada de la cartelera exitosamente"}),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# BUSCAR FUNCIONES POR FECHA (GET)
# ==========================================
@cartelera_bp.route("/cartelera/fecha", methods=["GET"])
def buscar_por_fecha():
    from app_cartelera import mysql

    # Capturamos la fecha enviada en la URL (ej: /cartelera/fecha?q=2026-04-18)
    fecha_buscada = request.args.get("q")

    if not fecha_buscada:
        return (
            jsonify(
                {
                    "error": "Debes enviar una fecha. Ejemplo: /cartelera/fecha?q=2026-04-18"
                }
            ),
            400,
        )

    try:
        cur = mysql.connection.cursor()
        # La función DATE() de SQL extrae solo la fecha (A-M-D) ignorando la hora
        cur.execute(
            """
            SELECT c.id_cartelera, p.titulo, cin.nombreCine, cin.ciudadCine, 
                   c.fecha_horaCartelera, c.idioma_proyeccionCartelera 
            FROM Carteleras c
            INNER JOIN Peliculas p ON c.id_peliculaCartelera = p.id_pelicula
            INNER JOIN Cines cin ON c.id_cineCartelera = cin.id_cine
            WHERE DATE(c.fecha_horaCartelera) = %s
            ORDER BY c.fecha_horaCartelera ASC
        """,
            (fecha_buscada,),
        )

        datos = cur.fetchall()
        cur.close()

        funciones = []
        for fila in datos:
            funciones.append(
                {
                    "id_cartelera": fila[0],
                    "pelicula": fila[1],
                    "cine": fila[2],
                    "ciudad": fila[3],
                    "fecha_hora": fila[4].strftime("%Y-%m-%d %H:%M:%S"),
                    "idioma": fila[5],
                }
            )

        if not funciones:
            return (
                jsonify(
                    {
                        "mensaje": f"No hay funciones programadas para la fecha: {fecha_buscada}"
                    }
                ),
                404,
            )

        return jsonify({"cartelera": funciones}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# BUSCAR FUNCIONES POR CINE (GET)
# ==========================================
@cartelera_bp.route("/cartelera/cine", methods=["GET"])
def buscar_por_cine():
    from app_cartelera import mysql

    # Capturamos el nombre del cine (ej: /cartelera/cine?q=Royal)
    cine_buscado = request.args.get("q")

    if not cine_buscado:
        return (
            jsonify(
                {
                    "error": "Debes enviar el nombre de un cine. Ejemplo: /cartelera/cine?q=Royal"
                }
            ),
            400,
        )

    try:
        cur = mysql.connection.cursor()
        # Usamos LIKE para que encuentre coincidencias parciales ("Royal" encontrará "Royal Films")
        cur.execute(
            """
            SELECT c.id_cartelera, p.titulo, cin.nombreCine, cin.ciudadCine, 
                   c.fecha_horaCartelera, c.idioma_proyeccionCartelera 
            FROM Carteleras c
            INNER JOIN Peliculas p ON c.id_peliculaCartelera = p.id_pelicula
            INNER JOIN Cines cin ON c.id_cineCartelera = cin.id_cine
            WHERE cin.nombreCine LIKE %s
            ORDER BY c.fecha_horaCartelera ASC
        """,
            (f"%{cine_buscado}%",),
        )

        datos = cur.fetchall()
        cur.close()

        funciones = []
        for fila in datos:
            funciones.append(
                {
                    "id_cartelera": fila[0],
                    "pelicula": fila[1],
                    "cine": fila[2],
                    "ciudad": fila[3],
                    "fecha_hora": fila[4].strftime("%Y-%m-%d %H:%M:%S"),
                    "idioma": fila[5],
                }
            )

        if not funciones:
            return (
                jsonify(
                    {
                        "mensaje": f"No encontramos funciones para el cine que contenga: {cine_buscado}"
                    }
                ),
                404,
            )

        return jsonify({"cartelera": funciones}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
