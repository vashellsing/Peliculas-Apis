from flask import Blueprint, request, jsonify

# Creamos el Blueprint para las pelculas
peliculas_bp = Blueprint('peliculas_bp', __name__)

# Traer TODAS las películas
@peliculas_bp.route('/peliculas', methods=['GET'])
def obtener_peliculas():
    from app import mysql 
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id_pelicula, titulo, titulo_originalPelicula, sinopsis, 
                   anio, actoresPelicula, generoPelicula, idiomaPelicula 
            FROM Peliculas
        """)
        datos = cur.fetchall()
        cur.close()

        peliculas = []
        for fila in datos:
            peliculas.append({
                "id": fila[0], "titulo": fila[1], "titulo_original": fila[2],
                "sinopsis": fila[3], "anio": fila[4], "actores": fila[5],
                "genero": fila[6], "idioma": fila[7]
            })

        return jsonify({"peliculas": peliculas}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Buscar películas por coincidencia parcial
# ==========================================
# ENDPOINTS DE BÚSQUEDA (Usando Query Parameters ?q=)
# ==========================================

# Buscar películas por TÍTULO
@peliculas_bp.route('/peliculas/buscar', methods=['GET'])
def buscar_por_titulo():
    from app import mysql 
    
    
    titulo_buscado = request.args.get('q')
    
    # validamos que se envio de manera correcta
    if not titulo_buscado:
        return jsonify({"error": "Debes enviar un término de búsqueda. Ejemplo: /peliculas/buscar?q=shrek"}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id_pelicula, titulo, titulo_originalPelicula, sinopsis, 
                   anio, actoresPelicula, generoPelicula, idiomaPelicula 
            FROM Peliculas 
            WHERE titulo LIKE %s
        """, (f"%{titulo_buscado}%",))
        
        datos = cur.fetchall()
        cur.close()

        peliculas = []
        for fila in datos:
            peliculas.append({
                "id": fila[0], "titulo": fila[1], "titulo_original": fila[2],
                "sinopsis": fila[3], "anio": fila[4], "actores": fila[5],
                "genero": fila[6], "idioma": fila[7]
            })

        if not peliculas:
            return jsonify({"mensaje": "No se encontraron películas con ese título"}), 404

        return jsonify({"peliculas": peliculas}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Buscar películas por CATEGORÍA
@peliculas_bp.route('/peliculas/categoria', methods=['GET'])
def buscar_por_genero():
    from app import mysql 
    
  
    genero_buscado = request.args.get('q')
    
    if not genero_buscado:
        return jsonify({"error": "Debes enviar una categoría. Ejemplo: /peliculas/categoria?q=Accion"}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id_pelicula, titulo, titulo_originalPelicula, sinopsis, 
                   anio, actoresPelicula, generoPelicula, idiomaPelicula 
            FROM Peliculas 
            WHERE generoPelicula = %s
        """, (genero_buscado,))
        
        datos = cur.fetchall()
        cur.close()

        peliculas = []
        for fila in datos:
            peliculas.append({
                "id": fila[0], "titulo": fila[1], "titulo_original": fila[2],
                "sinopsis": fila[3], "anio": fila[4], "actores": fila[5],
                "genero": fila[6], "idioma": fila[7]
            })

        if not peliculas:
            return jsonify({"mensaje": "No se encontraron películas en esa categoría"}), 404

        return jsonify({"peliculas": peliculas}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


# ENDPOINT PARA REGISTRAR PELICULAS (Admin)


@peliculas_bp.route('/peliculas/agregar', methods=['POST'])
def crear_pelicula():
    from app import mysql
    datos = request.json
    
    # Validación básica: Al menos el título y el año son obligatorios
    if not datos or not datos.get('titulo') or not datos.get('anio'):
        return jsonify({"error": "El título y el año son obligatorios"}), 400

    try:
        cur = mysql.connection.cursor()
        # Usamos .get() con valores por defecto por si el usuario no envía todos los datos
        cur.execute("""
            INSERT INTO Peliculas (titulo, titulo_originalPelicula, sinopsis, anio, 
                                   actoresPelicula, generoPelicula, idiomaPelicula) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            datos['titulo'], 
            datos.get('titulo_original', 'No especificado'), 
            datos.get('sinopsis', ''), 
            datos['anio'], 
            datos.get('actores', ''), 
            datos.get('genero', 'Otro'), 
            datos.get('idioma', 'Otro')
        ))
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify({"mensaje": "Película registrada exitosamente"}), 201
        
    except Exception as e:
        return jsonify({"error": "Error al registrar la película", "detalle": str(e)}), 500
    
    
    # ---------------------------------------------------------------------------------------------------
    # -------------------AHORA LOS ENDPOINTS PARA FAVORITOS----------------------------------------------
    # ---------------------------------------------------------------------------------------------------