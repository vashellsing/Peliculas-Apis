from flask import Blueprint, request, jsonify
from utils.auth import require_api_key, require_jwt, require_role

# Creamos el Blueprint para las pelculas
peliculas_bp = Blueprint("peliculas_bp", __name__)


# Traer TODAS las películas
@peliculas_bp.route("/peliculas", methods=["GET"])
@require_api_key
def obtener_peliculas():
    from app_peliculas import mysql

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT id_pelicula, titulo, titulo_originalPelicula, sinopsis, 
                   anio, actoresPelicula, generoPelicula, idiomaPelicula 
            FROM Peliculas
        """
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
                }
            )

        return jsonify({"peliculas": peliculas}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Buscar películas por coincidencia parcial
# ==========================================
# ENDPOINTS DE BUSQUEDA Usando Query ?q=
# ==========================================


# Buscar películas por TÍTULO
@peliculas_bp.route("/peliculas/buscar", methods=["GET"])
@require_api_key
def buscar_por_titulo():
    from app_peliculas import mysql

    titulo_buscado = request.args.get("q")

    # validamos que se envio de manera correcta
    if not titulo_buscado:
        return (
            jsonify(
                {
                    "error": "Debes enviar un término de búsqueda. Ejemplo: /peliculas/buscar?q=shrek"
                }
            ),
            400,
        )

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT id_pelicula, titulo, titulo_originalPelicula, sinopsis, 
                   anio, actoresPelicula, generoPelicula, idiomaPelicula 
            FROM Peliculas 
            WHERE titulo LIKE %s
        """,
            (f"%{titulo_buscado}%",),
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
                }
            )

        if not peliculas:
            return (
                jsonify({"mensaje": "No se encontraron películas con ese título"}),
                404,
            )

        return jsonify({"peliculas": peliculas}), 200
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
        cur.execute(
            """
            SELECT id_pelicula, titulo, titulo_originalPelicula, sinopsis, 
                   anio, actoresPelicula, generoPelicula, idiomaPelicula 
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
