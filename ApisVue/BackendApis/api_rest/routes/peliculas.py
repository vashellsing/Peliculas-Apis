from flask import Blueprint, request, jsonify
from utils.auth import require_api_key, require_jwt, require_role
import json

# Creamos el Blueprint para las pelculas
peliculas_bp = Blueprint("peliculas_bp", __name__)


# Traer TODAS las películas (Con promedio de calificación)
@peliculas_bp.route("/peliculas", methods=["GET"])
@require_api_key
def obtener_peliculas():
    from app_peliculas import mysql

    try:
        cur = mysql.connection.cursor()
        # AÑADIMOS EL LEFT JOIN PARA CALCULAR EL PROMEDIO DE ESTRELLAS
        cur.execute("""
            SELECT p.id_pelicula, p.titulo, p.titulo_originalPelicula, p.sinopsis, 
                   p.anio, p.actoresPelicula, p.generoPelicula, p.idiomaPelicula, p.poster,
                   COALESCE(ROUND(AVG(c.calificacionComentario), 1), 0.0) AS calificacion
            FROM Peliculas p
            LEFT JOIN Comentarios c ON p.id_pelicula = c.id_peliculaComentario
            GROUP BY p.id_pelicula
            """)
        datos = cur.fetchall()
        cur.close()

        peliculas = []
        for fila in datos:
            peliculas.append(
                {
                    "id": fila[0],
                    "titulo": fila[1],
                    "titulo_original": fila[2],
                    "sinopsis": fila[3],
                    "anio": fila[4],
                    "actores": fila[5],
                    "genero": fila[6],
                    "idioma": fila[7],
                    "poster": fila[8],
                    "calificacion": float(
                        fila[9]
                    ),  # <-- Agregamos la calificación al JSON
                }
            )

        return jsonify({"peliculas": peliculas}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Buscar UNA sola película por su ID (Con promedio de calificación)
@peliculas_bp.route("/peliculas/<int:id_pelicula>", methods=["GET"])
@require_api_key
def obtener_pelicula_por_id(id_pelicula):
    from app_peliculas import mysql
    import json  # Ya lo tienes arriba en tu archivo, pero aseguramos

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT p.id_pelicula, p.titulo, p.titulo_originalPelicula, p.sinopsis, 
                   p.anio, p.actoresPelicula, p.generoPelicula, p.idiomaPelicula, 
                   p.poster, p.lema, p.trailer,
                   COALESCE(ROUND(AVG(c.calificacionComentario), 1), 0.0) AS calificacion
            FROM Peliculas p
            LEFT JOIN Comentarios c ON p.id_pelicula = c.id_peliculaComentario
            WHERE p.id_pelicula = %s
            GROUP BY p.id_pelicula
            """,
            (id_pelicula,),
        )
        fila = cur.fetchone()
        cur.close()
        cur.close()

        if not fila:
            return jsonify({"error": "Película no encontrada"}), 404

        actores_lista = []
        if fila[5]:
            try:
                actores_lista = json.loads(fila[5])
            except Exception:
                actores_lista = []

        pelicula = {
            "id": fila[0],
            "titulo": fila[1],
            "titulo_original": fila[2],
            "sinopsis": fila[3],
            "anio": fila[4],
            "actores": actores_lista,
            "genero": fila[6],
            "idioma": fila[7],
            "poster": fila[8],
            "lema": fila[9],
            "trailer": fila[10],
            "calificacion": float(fila[11]),  # <-- Promedio extraído de la posición 11
        }

        return jsonify({"pelicula": pelicula}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Buscar películas por CATEGORÍA
@peliculas_bp.route("/peliculas/categoria", methods=["GET"])
@require_api_key
def buscar_por_genero():
    from app_peliculas import mysql

    genero_buscado = request.args.get("q")

    if not genero_buscado:
        return (
            jsonify(
                {
                    "error": "Debes enviar una categoría. Ejemplo: /peliculas/categoria?q=Accion"
                }
            ),
            400,
        )

    try:
        cur = mysql.connection.cursor()
        # AÑADIMOS EL CAMPO 'poster' AL SELECT
        cur.execute(
            """
            SELECT id_pelicula, titulo, titulo_originalPelicula, sinopsis, 
                   anio, actoresPelicula, generoPelicula, idiomaPelicula, poster 
            FROM Peliculas 
            WHERE generoPelicula = %s
            """,
            (genero_buscado,),
        )

        datos = cur.fetchall()
        cur.close()

        peliculas = []
        for fila in datos:
            peliculas.append(
                {
                    "id": fila[0],
                    "titulo": fila[1],
                    "titulo_original": fila[2],
                    "sinopsis": fila[3],
                    "anio": fila[4],
                    "actores": fila[5],
                    "genero": fila[6],
                    "idioma": fila[7],
                    "poster": fila[8],
                }
            )

        if not peliculas:
            return (
                jsonify({"mensaje": "No se encontraron películas en esa categoría"}),
                404,
            )

        return jsonify({"peliculas": peliculas}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ENDPOINT PARA REGISTRAR PELICULAS (Admin)


@peliculas_bp.route("/peliculas/agregar", methods=["POST"])
@require_api_key
@require_jwt
@require_role(["admin"])
def crear_pelicula():
    from app_peliculas import mysql

    datos = request.json
    if not datos or not datos.get("titulo") or not datos.get("anio"):
        return jsonify({"error": "El título y el año son obligatorios"}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO Peliculas (titulo, titulo_originalPelicula, sinopsis, anio, 
                                   actoresPelicula, generoPelicula, idiomaPelicula) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
            (
                datos["titulo"],
                datos.get("titulo_original", "No especificado"),
                datos.get("sinopsis", ""),
                datos["anio"],
                datos.get("actores", ""),
                datos.get("genero", "Otro"),
                datos.get("idioma", "Otro"),
            ),
        )
        mysql.connection.commit()
        cur.close()
        return (
            jsonify(
                {
                    "mensaje": "Película registrada exitosamente",
                    "por": request.current_user.get("nombre"),
                }
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return (
            jsonify({"error": "Error al registrar la película", "detalle": str(e)}),
            500,
        )


# ---------------------------------------------------------------------------------------------------
# -------------------AHORA LOS ENDPOINTS PARA FAVORITOS----------------------------------------------
# ---------------------------------------------------------------------------------------------------


# Agregar a favoritos


@peliculas_bp.route("/favorito/add/<int:id_pelicula>", methods=["POST"])
@require_api_key
@require_jwt
def agregar_favorito(id_pelicula):
    from app_peliculas import mysql

    # SEGURIDAD: El ID viene del Token
    id_usuario = request.current_user.get("id")

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO Favoritos (id_usuarioFavorito, id_peliculaFavorito) VALUES (%s, %s)",
            (id_usuario, id_pelicula),
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({"mensaje": "Agregada a TUS favoritos"}), 201
    except Exception as e:
        if "Duplicate entry" in str(e):
            return jsonify({"error": "Ya está en tus favoritos"}), 409
        return jsonify({"error": str(e)}), 500


# Mostrar favoritos de un usuario
@peliculas_bp.route(
    "/favoritos/mio", methods=["GET"]
)  # Cambiado de /usuario/<id> a /mio
@require_api_key
@require_jwt
def obtener_favoritos():
    from app_peliculas import mysql

    id_usuario = request.current_user.get("id")

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT p.id_pelicula, p.titulo, p.generoPelicula, f.fecha_agregado 
            FROM Favoritos f
            JOIN Peliculas p ON f.id_peliculaFavorito = p.id_pelicula
            WHERE f.id_usuarioFavorito = %s
        """,
            (id_usuario,),
        )
        datos = cur.fetchall()
        cur.close()

        favoritos = [
            {
                "id_pelicula": f[0],
                "titulo": f[1],
                "genero": f[2],
                "agregado_el": str(f[3]),
            }
            for f in datos
        ]
        return jsonify({"favoritos": favoritos}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Eliminar de favoritos
@peliculas_bp.route("/favorito/borrar/<int:id_pelicula>", methods=["DELETE"])
@require_api_key
@require_jwt
def eliminar_favorito(id_pelicula):
    from app_peliculas import mysql

    id_usuario = request.current_user.get("id")

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "DELETE FROM Favoritos WHERE id_usuarioFavorito = %s AND id_peliculaFavorito = %s",
            (id_usuario, id_pelicula),
        )
        mysql.connection.commit()
        if cur.rowcount == 0:
            return jsonify({"error": "No estaba en favoritos"}), 404
        cur.close()
        return jsonify({"mensaje": "Eliminado de favoritos"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# Ver que mas mira el usuario segun su favorito
# ==========================================
@peliculas_bp.route("/favoritos/analitica", methods=["GET"])
@require_api_key
@require_jwt
def analitica_favoritos():
    # Ya no necesitamos recibir id_usuario por la URL
    import pandas as pd
    import matplotlib.pyplot as plt
    from app_peliculas import mysql

    # Extraemos el ID del dueño del token
    id_usuario = request.current_user.get("id")
    nombre_usuario = request.current_user.get("nombre")

    try:
        cur = mysql.connection.cursor()

        # Consultamos directamente los géneros de los favoritos del usuario
        query = """
            SELECT p.generoPelicula 
            FROM Favoritos f
            JOIN Peliculas p ON f.id_peliculaFavorito = p.id_pelicula
            WHERE f.id_usuarioFavorito = %s
        """
        cur.execute(query, (id_usuario,))
        datos = cur.fetchall()
        cur.close()

        if not datos:
            return (
                jsonify({"mensaje": "No tienes películas en favoritos para analizar"}),
                404,
            )

        # ANALÍTICA CON PANDAS
        # Convertimos la lista de tuplas en un DataFrame
        df = pd.DataFrame(datos, columns=["genero"])
        conteo_generos = df["genero"].value_counts()

        # GRAFICA CON MATPLOTLIB
        plt.figure(figsize=(6, 6))
        plt.pie(
            conteo_generos,
            labels=conteo_generos.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=plt.cm.Paired.colors,
        )
        plt.title(f"Perfil de Cinéfilo: {nombre_usuario}")

        # Guardamos o mostramos (plt.show() abre ventana en el servidor)
        print(f"Generando gráfica para {nombre_usuario}...")
        plt.show()

        return (
            jsonify(
                {
                    "id_usuario": id_usuario,
                    "nombre": nombre_usuario,
                    "mensaje": "Análisis completado exitosamente.",
                    "total_favoritos": len(df),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {"error": "Error interno al generar la analítica", "detalle": str(e)}
            ),
            500,
        )


# Endpoint para mostrar el póster de una película aleatoriamente filtrando los nulls
# En routes/peliculas.py — agrega esta ruta


@peliculas_bp.route("/peliculas/poster-aleatorio", methods=["GET"])
@require_api_key
def obtener_poster_aleatorio():
    from app_peliculas import mysql

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT poster 
            FROM Peliculas
            WHERE poster IS NOT NULL 
              AND poster != ''
            ORDER BY RAND()
            LIMIT 1
        """)
        dato = cur.fetchone()
        cur.close()

        if dato is None:
            return jsonify({"poster": None}), 200

        return jsonify({"poster": dato[0]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
