from flask import Blueprint, request, jsonify

# Creamos el Blueprint para las pelculas
peliculas_bp = Blueprint("peliculas_bp", __name__)


# Traer TODAS las películas
@peliculas_bp.route("/peliculas", methods=["GET"])
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
def crear_pelicula():
    from app_peliculas import mysql

    datos = request.json

    # Validación básica: Al menos el título y el año son obligatorios
    if not datos or not datos.get("titulo") or not datos.get("anio"):
        return jsonify({"error": "El título y el año son obligatorios"}), 400

    try:
        cur = mysql.connection.cursor()
        # Usamos .get() con valores por defecto por si el usuario no envía todos los datos
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

        return jsonify({"mensaje": "Película registrada exitosamente"}), 201

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
def agregar_favorito(id_pelicula):
    from app_peliculas import mysql

    datos = request.json
    id_usuario = datos.get("id_usuario")

    if not id_usuario:
        return jsonify({"error": "El id_usuario es obligatorio"}), 400

    try:
        cur = mysql.connection.cursor()
        # Insertamos la relación entre el usuario (del JSON) y la película (de la URL)
        cur.execute(
            "INSERT INTO Favoritos (id_usuarioFavorito, id_peliculaFavorito) VALUES (%s, %s)",
            (id_usuario, id_pelicula),
        )
        mysql.connection.commit()
        cur.close()

        return jsonify({"mensaje": "Película agregada a favoritos con éxito"}), 201
    except Exception as e:
        # Manejo de error por si ya existe el favorito (Duplicate entry)
        if "Duplicate entry" in str(e):
            return jsonify({"error": "Esta película ya está en tus favoritos"}), 409
        return jsonify({"error": str(e)}), 500


# Mostrar favoritos de un usuario
@peliculas_bp.route("/favoritos/usuario/<int:id_usuario>", methods=["GET"])
def obtener_favoritos(id_usuario):
    from app_peliculas import mysql

    try:
        cur = mysql.connection.cursor()
        # Hacemos un JOIN para mostrar información útil de la película
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

        favoritos = []
        for fila in datos:
            favoritos.append(
                {
                    "id_pelicula": fila[0],
                    "titulo": fila[1],
                    "genero": fila[2],
                    "agregado_el": fila[3],
                }
            )

        return jsonify({"favoritos": favoritos}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Eliminar de favoritos
@peliculas_bp.route("/favorito/borrar/<int:id_pelicula>", methods=["DELETE"])
def eliminar_favorito(id_pelicula):
    from app_peliculas import mysql

    datos = request.json
    id_usuario = datos.get("id_usuario")

    if not id_usuario:
        return (
            jsonify(
                {"error": "El id_usuario es obligatorio para eliminar el favorito"}
            ),
            400,
        )

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "DELETE FROM Favoritos WHERE id_usuarioFavorito = %s AND id_peliculaFavorito = %s",
            (id_usuario, id_pelicula),
        )
        mysql.connection.commit()

        if cur.rowcount == 0:
            return (
                jsonify({"error": "No tiene registrada la pelicula en favoritos"}),
                404,
            )

        cur.close()
        return jsonify({"mensaje": "Película eliminada de favoritos exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# Ver que mas mira el usuario segun su favorito
# ==========================================
@peliculas_bp.route("/favoritos/analitica/<int:id_usuario>", methods=["GET"])
def analitica_favoritos(id_usuario):
    import requests
    import pandas as pd
    import matplotlib.pyplot as plt

    try:

        # Hacemos una petición GET a nuestro PROPIO endpoint de favoritos
        url_api_favoritos = f"http://127.0.0.1:5000/favoritos/usuario/{id_usuario}"

        print(f"Consultando intermediario: {url_api_favoritos}...")
        respuesta = requests.get(url_api_favoritos)

        # Validamos si la otra API respondió bien
        if respuesta.status_code != 200:
            return (
                jsonify({"error": "No se pudo obtener la información del usuario"}),
                respuesta.status_code,
            )

        # EL JSON (El intermediario)
        datos_json = respuesta.json()
        lista_favoritos = datos_json.get("favoritos", [])

        if not lista_favoritos:
            return (
                jsonify(
                    {
                        "mensaje": "El usuario no tiene películas en favoritos para analizar"
                    }
                ),
                404,
            )

        # ANALÍTICA CON PANDAS
        df = pd.DataFrame(lista_favoritos)

        #  la llave "genero", contamos por esa columna
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
        plt.title(f"Tu Perfil de Cinéfilo (Usuario {id_usuario})")

        # Mostramos la ventana emergente
        print("Abriendo gráfica de Matplotlib...")
        plt.show()

        return (
            jsonify(
                {
                    "id_usuario": id_usuario,
                    "mensaje": "Análisis completado. Gráfica mostrada en el servidor.",
                    "datos_utilizados": len(lista_favoritos),
                }
            ),
            200,
        )

    except requests.exceptions.RequestException as e:
        return (
            jsonify(
                {
                    "error": "Fallo la comunicación con la API de favoritos",
                    "detalle": str(e),
                }
            ),
            500,
        )
    except Exception as e:
        return (
            jsonify(
                {"error": "Error interno al generar la analítica", "detalle": str(e)}
            ),
            500,
        )
