from flask import Blueprint, request, jsonify
from utils.auth import require_api_key, require_jwt, require_role

# Creamos el Blueprint para la cartelera
cartelera_bp = Blueprint("cartelera_bp", __name__)


# ==========================================
# TRAER TODA LA CARTELERA (GET)
# ==========================================
@cartelera_bp.route("/cartelera", methods=["GET"])
@require_api_key
def obtener_cartelera():
    from app_cartelera import mysql

    try:
        cur = mysql.connection.cursor()
        # 1. Agregamos cin.linkWeb (o el nombre exacto de tu columna en la DB) al SELECT
        cur.execute("""
            SELECT c.id_cartelera, p.titulo, cin.nombreCine, cin.ciudadCine, 
                   c.fecha_horaCartelera, c.idioma_proyeccionCartelera, cin.linkWeb 
            FROM Carteleras c
            INNER JOIN Peliculas p ON c.id_peliculaCartelera = p.id_pelicula
            INNER JOIN Cines cin ON c.id_cineCartelera = cin.id_cine
            ORDER BY c.fecha_horaCartelera ASC
        """)

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
                    "link_cine": fila[
                        6
                    ],  # <-- 2. Lo mapeamos aquí como la posición fila[6]
                }
            )

        return jsonify({"cartelera": funciones}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# BUSCAR FUNCIONES POR PELÍCULA (GET)
# ==========================================
@cartelera_bp.route("/cartelera/pelicula/<int:id_pelicula>", methods=["GET"])
@require_api_key
def buscar_por_pelicula(id_pelicula):
    from app_cartelera import mysql

    try:
        cur = mysql.connection.cursor()
        # Asegúrate de que 'direccionCine' exista en tu tabla Cines. Si se llama distinto, cámbialo aquí.
        cur.execute(
            """
            SELECT c.id_cartelera, p.titulo, cin.nombreCine, cin.ciudadCine, cin.direccionCine,
                   c.fecha_horaCartelera, c.idioma_proyeccionCartelera 
            FROM Carteleras c
            INNER JOIN Peliculas p ON c.id_peliculaCartelera = p.id_pelicula
            INNER JOIN Cines cin ON c.id_cineCartelera = cin.id_cine
            WHERE c.id_peliculaCartelera = %s
            ORDER BY c.fecha_horaCartelera ASC
            """,
            (id_pelicula,),
        )

        datos = cur.fetchall()
        cur.close()

        funciones = []
        for fila in datos:
            funciones.append(
                {
                    "id_cartelera": fila[0],
                    "pelicula": fila[1],
                    "nombreCine": fila[2],
                    "ciudadCine": fila[3],
                    "direccionCine": fila[4],
                    "fecha_hora": fila[5].strftime(
                        "%Y-%m-%d %H:%M"
                    ),  # Le quité los segundos para que se vea mejor en pantalla
                    "idioma": fila[6],
                }
            )

        return jsonify({"cartelera": funciones}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# AGREGAR NUEVA FUNCIÓN (POST)
# ==========================================
@cartelera_bp.route("/cartelera", methods=["POST"])
@require_api_key
@require_jwt
@require_role(["admin"])
def crear_funcion():
    # Segundo: ¿Es administrador?
    usuario = request.current_user

    if usuario.get("rol") != "admin":
        return (
            jsonify(
                {
                    "error": "No tienes permisos de administrador para programar funciones"
                }
            ),
            403,
        )
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
@require_api_key
@require_jwt
@require_role(["admin"])
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
            return (
                jsonify({"error": "No se realizo ningún cambio para actualizarla "}),
                404,
            )

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
@require_api_key  #  ¿Viene de una App autorizada?
@require_jwt  #  ¿El usuario está logueado?
@require_role(["admin"])  #  ¿Es administrador?
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
@require_api_key
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
@require_api_key
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


# -------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------- CINES
# --------------------------------------------------------------------------------------------
# ==========================================
# OBTENER TODOS LOS CINES (GET)
# ==========================================
# ==========================================
# OBTENER TODOS LOS CINES (GET)
# ==========================================
@cartelera_bp.route("/cines", methods=["GET"])
@require_api_key
def obtener_cines():
    # Asegúrate de importar tu instancia de mysql correspondiente (ej: app_cines)
    from app_cartelera import mysql

    try:
        cur = mysql.connection.cursor()
        # 1. ¡Agregamos linkWeb a la consulta SQL!
        cur.execute(
            "SELECT id_cine, nombreCine, direccionCine, ciudadCine, linkWeb FROM cines"
        )
        datos = cur.fetchall()
        cur.close()

        lista_cines = []
        for fila in datos:
            lista_cines.append(
                {
                    "id_cine": fila[0],
                    "nombreCine": fila[1],
                    "direccionCine": fila[2],
                    "ciudadCine": fila[3],
                    "linkWeb": fila[
                        4
                    ],  # 2. ¡Lo agregamos al paquete que se envía a Vue!
                }
            )
        return jsonify({"cines": lista_cines}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# AGREGAR NUEVO CINE (POST)
# ==========================================
@cartelera_bp.route("/cines", methods=["POST"])
@require_api_key
@require_jwt
@require_role(["admin"])
def agregar_cine():
    from app_cartelera import mysql

    datos = request.json

    if not datos or not all(k in datos for k in ("nombreCine",)):
        return jsonify({"error": "El nombre del cine es obligatorio"}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO cines (nombreCine, direccionCine, ciudadCine, linkWeb) 
            VALUES (%s, %s, %s, %s)
            """,
            (
                datos.get("nombreCine"),
                datos.get("direccionCine", ""),
                datos.get("ciudadCine", ""),
                datos.get("linkWeb", ""),
            ),
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({"mensaje": "Cine agregado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ACTUALIZAR CINE (PUT)
# ==========================================
@cartelera_bp.route("/cines/<int:id_cine>", methods=["PUT"])
@require_api_key
@require_jwt
@require_role(["admin"])
def actualizar_cine(id_cine):
    from app_cartelera import mysql

    datos = request.json

    if not datos or not all(k in datos for k in ("nombreCine",)):
        return jsonify({"error": "El nombre del cine es obligatorio"}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE cines 
            SET nombreCine=%s, direccionCine=%s, ciudadCine=%s, linkWeb=%s 
            WHERE id_cine=%s
            """,
            (
                datos.get("nombreCine"),
                datos.get("direccionCine", ""),
                datos.get("ciudadCine", ""),
                datos.get("linkWeb", ""),  # <-- AQUÍ AGREGAMOS EL LINK
                id_cine,
            ),
        )
        mysql.connection.commit()

        # Recuerda: Si mandas los mismos datos sin cambiar nada, rowcount será 0
        if cur.rowcount == 0:
            return (
                jsonify({"error": "No se realizó ningún cambio o el cine no existe"}),
                404,
            )

        cur.close()
        return jsonify({"mensaje": "Cine actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ELIMINAR CINE (DELETE)
# ==========================================
@cartelera_bp.route("/cines/<int:id_cine>", methods=["DELETE"])
@require_api_key
@require_jwt
@require_role(["admin"])
def eliminar_cine(id_cine):
    from app_cartelera import mysql

    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM cines WHERE id_cine = %s", (id_cine,))
        mysql.connection.commit()

        if cur.rowcount == 0:
            return jsonify({"error": "El cine que intentas borrar no existe"}), 404

        cur.close()
        return jsonify({"mensaje": "Cine eliminado exitosamente"}), 200
    except Exception as e:
        # Controlar error por si hay carteleras atadas a este cine
        if "foreign key constraint fails" in str(e).lower():
            return (
                jsonify(
                    {
                        "error": "No puedes eliminar este cine porque tiene funciones programadas en la cartelera."
                    }
                ),
                400,
            )
        return jsonify({"error": str(e)}), 500
