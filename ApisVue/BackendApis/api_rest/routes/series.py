from flask import Blueprint, request, jsonify
from utils.auth import require_api_key
import json

# Creamos el Blueprint para las series
series_bp = Blueprint("series_bp", __name__)


# ==========================================
# Trae todas las series (Con promedio de calificación)
# ==========================================
@series_bp.route("/series", methods=["GET"])
@require_api_key
def obtener_series():
    from app_series import mysql

    try:
        cur = mysql.connection.cursor()
        # Añadimos el LEFT JOIN y COALESCE igual que en películas
        cur.execute("""
            SELECT s.id_serie, s.tituloSerie, s.titulo_originalSerie, s.sinopsisSerie, 
                   s.anio_lanzamientoSerie, s.temporadasSerie, s.actoresSerie, s.generoSerie, s.idiomaSerie,
                   s.posterSerie, COALESCE(ROUND(AVG(c.calificacionComentario), 1), 0.0) AS calificacion
            FROM Series s
            LEFT JOIN Comentarios c ON s.id_serie = c.id_serieComentario
            GROUP BY s.id_serie
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
                    "imagenUrl": fila[9],
                    "calificacion": float(fila[10]),  # Convertimos a float
                }
            )

        return jsonify({"series": series}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# Buscar UNA sola serie por su ID (Con promedio de calificación)
# ==========================================
@series_bp.route("/series/<int:id_serie>", methods=["GET"])
@require_api_key
def obtener_serie_por_id(id_serie):
    from app_series import mysql
    import json

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT s.id_serie, s.tituloSerie, s.titulo_originalSerie, s.sinopsisSerie, 
                   s.anio_lanzamientoSerie, s.temporadasSerie, s.actoresSerie, s.episodiosSerie, s.generoSerie, s.idiomaSerie,
                   s.posterSerie, s.trailerSerie, COALESCE(ROUND(AVG(c.calificacionComentario), 1), 0.0) AS calificacion
            FROM Series s
            LEFT JOIN Comentarios c ON s.id_serie = c.id_serieComentario
            WHERE s.id_serie = %s
            GROUP BY s.id_serie
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
        if fila[7]:
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
            "temporadas_info": episodios_lista,
            "genero": fila[8],
            "idioma": fila[9],
            "imagenUrl": fila[10],
            "trailer": fila[11],
            "calificacion": float(fila[12]),  # Promedio calculado extraído
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

    idioma_buscado = request.args.get("q")

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
            SELECT s.id_serie, s.tituloSerie, s.titulo_originalSerie, s.sinopsisSerie, 
                   s.anio_lanzamientoSerie, s.temporadasSerie, s.actoresSerie, s.generoSerie, s.idiomaSerie, s.posterSerie,
                   COALESCE(ROUND(AVG(c.calificacionComentario), 1), 0.0) AS calificacion
            FROM Series s
            LEFT JOIN Comentarios c ON s.id_serie = c.id_serieComentario
            WHERE s.idiomaSerie = %s
            GROUP BY s.id_serie
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
                    "imagenUrl": fila[9],
                    "calificacion": float(fila[10]),
                }
            )

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

    anio_buscado = request.args.get("q")

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
            SELECT s.id_serie, s.tituloSerie, s.titulo_originalSerie, s.sinopsisSerie, 
                   s.anio_lanzamientoSerie, s.temporadasSerie, s.actoresSerie, s.generoSerie, s.idiomaSerie, s.posterSerie,
                   COALESCE(ROUND(AVG(c.calificacionComentario), 1), 0.0) AS calificacion
            FROM Series s
            LEFT JOIN Comentarios c ON s.id_serie = c.id_serieComentario
            WHERE s.anio_lanzamientoSerie = %s
            GROUP BY s.id_serie
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
                    "imagenUrl": fila[9],
                    "calificacion": float(fila[10]),
                }
            )

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

    genero_buscado = request.args.get("q")

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
            SELECT s.id_serie, s.tituloSerie, s.titulo_originalSerie, s.sinopsisSerie, 
                   s.anio_lanzamientoSerie, s.temporadasSerie, s.actoresSerie, s.generoSerie, s.idiomaSerie, s.posterSerie,
                   COALESCE(ROUND(AVG(c.calificacionComentario), 1), 0.0) AS calificacion
            FROM Series s
            LEFT JOIN Comentarios c ON s.id_serie = c.id_serieComentario
            WHERE s.generoSerie = %s
            GROUP BY s.id_serie
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
                    "imagenUrl": fila[9],
                    "calificacion": float(fila[10]),
                }
            )

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
