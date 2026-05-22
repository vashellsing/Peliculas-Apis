from flask import Blueprint, request, jsonify
from utils.auth import require_api_key
import json

# Creamos el Blueprint para las series
series_bp = Blueprint("series_bp", __name__)


# ==========================================
# Trae todas las series
# ==========================================
@series_bp.route("/series", methods=["GET"])
@require_api_key
def obtener_series():
    from app_series import mysql

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id_serie, tituloSerie, titulo_originalSerie, sinopsisSerie, 
                   anio_lanzamientoSerie, temporadasSerie, actoresSerie, generoSerie, idiomaSerie,
                   posterSerie, calificacionSerie 
            FROM Series
            """)
        datos = cur.fetchall()
        cur.close()

        series = []
        for fila in datos:
            series.append(
                {
                    "id": fila[0],
                    "titulo": fila[1],
                    "titulo_original": fila[2],
                    "sinopsis": fila[3],
                    "anio": fila[4],
                    "temporadas": fila[5],
                    "actores": fila[6],
                    "genero": fila[7],
                    "idioma": fila[8],
                    "imagenUrl": fila[9],  # Mapeamos el poster
                    "calificacion": fila[10],  # Mapeamos la calificación
                }
            )

        return jsonify({"series": series}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@series_bp.route("/series/<int:id_serie>", methods=["GET"])
@require_api_key
def obtener_serie_por_id(id_serie):
    from app_series import mysql
    import json

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT id_serie, tituloSerie, titulo_originalSerie, sinopsisSerie, 
                   anio_lanzamientoSerie, temporadasSerie, actoresSerie, episodiosSerie, generoSerie, idiomaSerie,
                   posterSerie, calificacionSerie, trailerSerie
            FROM Series
            WHERE id_serie = %s
            """,
            (id_serie,),
        )
        fila = cur.fetchone()
        cur.close()

        if not fila:
            return jsonify({"error": "Serie no encontrada"}), 404

        # Procesar JSONs (Actores y Episodios)
        actores_lista = []
        episodios_lista = []
        if fila[6]:
            try:
                actores_lista = json.loads(fila[6])
            except:
                pass
        if fila[7]:  # <--- AQUÍ LEEMOS LOS EPISODIOS REALES
            try:
                episodios_lista = json.loads(fila[7])
            except:
                pass

        serie = {
            "id": fila[0],
            "titulo": fila[1],
            "titulo_original": fila[2],
            "sinopsis": fila[3],
            "anio": fila[4],
            "temporadas_totales": fila[5],
            "actores": actores_lista,
            "temporadas_info": episodios_lista,  # <--- SE LO MANDAMOS AL FRONT
            "genero": fila[8],
            "idioma": fila[9],
            "imagenUrl": fila[10],
            "calificacion": fila[11],
            "trailer": fila[12],
        }

        return jsonify({"serie": serie}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ENDPOINT PARA BUSCAR SERIES POR IDIOMA
# ==========================================
@series_bp.route("/series/idioma", methods=["GET"])
@require_api_key
def buscar_por_idioma():
    from app_series import mysql

    # Capturamos el idioma enviado en la URL, ej: /series/idioma?q=Ingles
    idioma_buscado = request.args.get("q")

    # Validamos que el usuario haya enviado el parámetro
    if not idioma_buscado:
        return (
            jsonify(
                {
                    "error": "Debes enviar un idioma válido. Ejemplo: /series/idioma?q=Espanol"
                }
            ),
            400,
        )

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT id_serie, tituloSerie, titulo_originalSerie, sinopsisSerie, 
                   anio_lanzamientoSerie, temporadasSerie, actoresSerie, generoSerie, idiomaSerie 
            FROM Series 
            WHERE idiomaSerie = %s
            """,
            (idioma_buscado,),
        )

        datos = cur.fetchall()
        cur.close()

        series = []
        for fila in datos:
            series.append(
                {
                    "id": fila[0],
                    "titulo": fila[1],
                    "titulo_original": fila[2],
                    "sinopsis": fila[3],
                    "anio": fila[4],
                    "temporadas": fila[5],
                    "actores": fila[6],
                    "genero": fila[7],
                    "idioma": fila[8],
                    "imagenUrl": fila[9],  # Mapeamos el poster
                    "calificacion": fila[10],  # Mapeamos la calificación
                }
            )

        # Si el array esta vacio, significa que no hay series en ese idioma
        if not series:
            return (
                jsonify(
                    {
                        "mensaje": f"No se encontraron series en el idioma: {idioma_buscado}"
                    }
                ),
                404,
            )

        return jsonify({"series": series}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ENDPOINT PARA BUSCAR SERIES POR AÑO
# ==========================================
@series_bp.route("/series/anio", methods=["GET"])
@require_api_key
def buscar_por_anio():
    from app_series import mysql

    # Capturamos el año enviado en la URL, ej: /series/anio?q=2017
    anio_buscado = request.args.get("q")

    # Validamos que el usuario haya enviado el parámetro
    if not anio_buscado:
        return (
            jsonify(
                {"error": "Debes enviar un año válido. Ejemplo: /series/anio?q=2021"}
            ),
            400,
        )

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT id_serie, tituloSerie, titulo_originalSerie, sinopsisSerie, 
                   anio_lanzamientoSerie, temporadasSerie, actoresSerie, generoSerie, idiomaSerie 
            FROM Series 
            WHERE anio_lanzamientoSerie = %s
            """,
            (anio_buscado,),
        )

        datos = cur.fetchall()
        cur.close()

        series = []
        for fila in datos:
            series.append(
                {
                    "id": fila[0],
                    "titulo": fila[1],
                    "titulo_original": fila[2],
                    "sinopsis": fila[3],
                    "anio": fila[4],
                    "temporadas": fila[5],
                    "actores": fila[6],
                    "genero": fila[7],
                    "idioma": fila[8],
                    "imagenUrl": fila[9],  # Mapeamos el poster
                    "calificacion": fila[10],  # Mapeamos la calificación
                }
            )

        # Si el array está vacío, significa que no hay series de ese año
        if not series:
            return (
                jsonify(
                    {
                        "mensaje": f"No se encontraron series lanzadas en el año: {anio_buscado}"
                    }
                ),
                404,
            )

        return jsonify({"series": series}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ENDPOINT PARA BUSCAR SERIES POR GÉNERO
# ==========================================
@series_bp.route("/series/genero", methods=["GET"])
@require_api_key
def buscar_por_genero():
    from app_series import mysql

    # Capturamos el género enviado en la URL, ej: /series/genero?q=Drama
    genero_buscado = request.args.get("q")

    # Validamos que el usuario haya enviado el parámetro
    if not genero_buscado:
        return (
            jsonify(
                {
                    "error": "Debes enviar un género válido. Ejemplo: /series/genero?q=Ciencia Ficcion"
                }
            ),
            400,
        )

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT id_serie, tituloSerie, titulo_originalSerie, sinopsisSerie, 
                   anio_lanzamientoSerie, temporadasSerie, actoresSerie, generoSerie, idiomaSerie 
            FROM Series 
            WHERE generoSerie = %s
            """,
            (genero_buscado,),
        )

        datos = cur.fetchall()
        cur.close()

        series = []
        for fila in datos:
            series.append(
                {
                    "id": fila[0],
                    "titulo": fila[1],
                    "titulo_original": fila[2],
                    "sinopsis": fila[3],
                    "anio": fila[4],
                    "temporadas": fila[5],
                    "actores": fila[6],
                    "genero": fila[7],
                    "idioma": fila[8],
                    "imagenUrl": fila[9],  # Mapeamos el poster
                    "calificacion": fila[10],  # Mapeamos la calificación
                }
            )

        # Si el array está vacío, significa que no hay series en ese género
        if not series:
            return (
                jsonify(
                    {
                        "mensaje": f"No se encontraron series en el género: {genero_buscado}"
                    }
                ),
                404,
            )

        return jsonify({"series": series}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
