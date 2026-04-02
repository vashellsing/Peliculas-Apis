import pymysql
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Iterable, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '', 
    'db': 'webpeliculasDB',
    'cursorclass': pymysql.cursors.DictCursor
}


class Resena(ComplexModel):
    id_comentario = Integer
    id_pelicula = Integer
    id_usuario = Integer
    calificacion = Integer
    texto = Unicode
    fecha = Unicode 

class ServicioResenas(ServiceBase):
    
    # =========================================================
    # READ: Obtener las reseñas de una película
    # =========================================================
    @rpc(Integer, _returns=Iterable(Resena))
    def obtener_resenas(ctx, id_pelicula):
        conn = pymysql.connect(**DB_CONFIG)
        try:
            with conn.cursor() as cursor:
                # Traemos los datos, ordenados del más nuevo al más viejo
                sql = "SELECT id_comentario, id_peliculaComentario, id_usuarioComentario, calificacionComentario, textoComentario, fecha_creacion FROM Comentarios WHERE id_peliculaComentario = %s ORDER BY fecha_creacion DESC"
                cursor.execute(sql, (id_pelicula,))
                result = cursor.fetchall()
                
                for row in result:
                    yield Resena(
                        id_comentario=row['id_comentario'],
                        id_pelicula=row['id_peliculaComentario'],
                        id_usuario=row['id_usuarioComentario'],
                        calificacion=row['calificacionComentario'],
                        texto=row['textoComentario'],
                        fecha=str(row['fecha_creacion']) # Convertimos la fecha de la BD a texto legible
                    )
        finally:
            conn.close()

    # =========================================================
    # CREATE: Agregar reseña (CON REGLA ANTI-SPAM)
    # =========================================================
    @rpc(Integer, Integer, Integer, Unicode, _returns=Unicode)
    def agregar_resena(ctx, id_pelicula, id_usuario, calificacion, texto):
        conn = pymysql.connect(**DB_CONFIG)
        try:
            with conn.cursor() as cursor:
                # REGLA ANTI-BOT: ¿Este usuario ya comentó esta película?
                sql_verificar = "SELECT id_comentario FROM Comentarios WHERE id_peliculaComentario = %s AND id_usuarioComentario = %s"
                cursor.execute(sql_verificar, (id_pelicula, id_usuario))
                
                if cursor.fetchone():
                    return "Error de Seguridad: Ya publicaste una reseña para esta película. No se permite spam."
                
                # Si no ha comentado, guardamos (MySQL pone las fechas solo)
                sql_insert = "INSERT INTO Comentarios (id_peliculaComentario, id_usuarioComentario, calificacionComentario, textoComentario) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_insert, (id_pelicula, id_usuario, calificacion, texto))
            conn.commit() 
            return "Éxito: Reseña publicada correctamente."
        finally:
            conn.close()

    # =========================================================
    # UPDATE: Modificar una reseña
    # =========================================================
    @rpc(Integer, Integer, Integer, Unicode, _returns=Unicode)
    def actualizar_resena(ctx, id_comentario, id_usuario, nueva_calificacion, nuevo_texto):
        conn = pymysql.connect(**DB_CONFIG)
        try:
            with conn.cursor() as cursor:
                # Verificamos id_usuario para que nadie edite lo que no es suyo
                sql = "UPDATE Comentarios SET calificacionComentario=%s, textoComentario=%s WHERE id_comentario=%s AND id_usuarioComentario=%s"
                cursor.execute(sql, (nueva_calificacion, nuevo_texto, id_comentario, id_usuario))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    return "Éxito: Reseña actualizada correctamente."
                else:
                    return "Error: La reseña no existe o no tienes permiso para editarla."
        finally:
            conn.close()

    # =========================================================
    # DELETE: Eliminar una reseña
    # =========================================================
    @rpc(Integer, Integer, _returns=Unicode)
    def eliminar_resena(ctx, id_comentario, id_usuario):
        conn = pymysql.connect(**DB_CONFIG)
        try:
            with conn.cursor() as cursor:
                # Verificamos id_usuario para que nadie borre lo de otros
                sql = "DELETE FROM Comentarios WHERE id_comentario=%s AND id_usuarioComentario=%s"
                cursor.execute(sql, (id_comentario, id_usuario))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    return "Éxito: Reseña eliminada."
                else:
                    return "Error: La reseña no existe o no tienes permiso para borrarla."
        finally:
            conn.close()

# 3. Configuración para arrancar el servidor
application = Application([ServicioResenas],
    tns='spyne.cine.resenas',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    # ATENCIÓN: Usamos el puerto 8001 para que no choque con tu otra API
    server = make_server('0.0.0.0', 8001, wsgi_app)
    print("--- API CRUD de Reseñas LISTA ---")
    print("Escuchando en http://127.0.0.1:8001")
    print("WSDL en http://127.0.0.1:8001/?wsdl")
    server.serve_forever()