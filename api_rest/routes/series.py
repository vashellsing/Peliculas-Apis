from flask import Blueprint, request, jsonify

# Creamos el Blueprint para las series
series_bp = Blueprint("series_bp", __name__)


# ==========================================
# ENDPOINT PARA TRAER TODO EL CATÁLOGO
# ==========================================
@series_bp.route("/series", methods=["GET"])
def obtener_series():
    from app_series import mysql

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT id_serie, tituloSerie, titulo_originalSerie, sinopsisSerie, 
                   anio_lanzamientoSerie, temporadasSerie, actoresSerie, generoSerie, idiomaSerie 
            FROM Series
            """
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
                }
            )

        return jsonify({"series": series}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ENDPOINT PARA BUSCAR SERIES POR IDIOMA
# ==========================================
@series_bp.route("/series/idioma", methods=["GET"])
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
                }
            )

        # Si el array está vacío, significa que no hay series en ese idioma
        if not series:
            return (
                jsonify({"mensaje": f"No se encontraron series en el idioma: {idioma_buscado}"}),
                404,
            )

        return jsonify({"series": series}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500