import logging
import jwt
import datetime
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api_rest"))
)


# Añadimos la ruta para poder importar config.py que está en api_rest

from config import Config

from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import pymysql


def obtener_conexion():
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB,
    )


class ServicioAutenticacion(ServiceBase):

    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def registrar_usuario(ctx, nombreUsuario, correoUsuario, contrasenaUsuario):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as ejecutarConsulta:
                sql_verificar = (
                    "SELECT id_usuario FROM Usuarios WHERE correoUsuario = %s"
                )
                ejecutarConsulta.execute(sql_verificar, (correoUsuario,))
                if ejecutarConsulta.fetchone():
                    return "Error: Ese correo ya existe."

                # Por defecto registramos como 'cliente'
                sql_insertar = "INSERT INTO Usuarios (nombreUsuario, correoUsuario, contrasenaUsuario, rol) VALUES (%s, %s, %s, 'usuario')"
                ejecutarConsulta.execute(
                    sql_insertar, (nombreUsuario, correoUsuario, contrasenaUsuario)
                )
                conexion.commit()
                return "exito: usuario registrado como cliente."
        finally:
            conexion.close()

    @rpc(Unicode, Unicode, _returns=Unicode)
    def iniciar_sesion(ctx, correoUsuario, contrasenaUsuario):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as ejecutarConsulta:
                # 1. ACTUALIZADO: Pedimos también el correoUsuario y el avatarUrl
                sql_buscar = """
                    SELECT id_usuario, nombreUsuario, correoUsuario, rol, avatarUrl, fecha_registro 
                    FROM Usuarios 
                    WHERE correoUsuario = %s AND contrasenaUsuario = %s
                """
                ejecutarConsulta.execute(sql_buscar, (correoUsuario, contrasenaUsuario))
                usuario = ejecutarConsulta.fetchone()

                if usuario:
                    # 2. ACTUALIZADO: Desempaquetamos los 6 valores exactos que pedimos en el SELECT
                    id_user, nombre, correo, rol, avatar, fecha_reg = usuario
                    fecha_limpia = (
                        fecha_reg.strftime("%Y-%m-%d") if fecha_reg else "Reciente"
                    )  # Formateamos la fecha a un string legible

                    # 3. ACTUALIZADO: Metemos los datos nuevos al Payload del token
                    payload = {
                        "id": id_user,
                        "nombre": nombre,
                        "correo": correo,  # <-- Ya viaja el correo
                        "rol": rol,
                        "avatarUrl": avatar,  # <-- Ya viaja el avatar
                        "miembroDesde": fecha_limpia,  # <-- Enviamos la fecha formateada
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
                    }

                    token = jwt.encode(
                        payload, Config.JWT_SECRET_KEY, algorithm="HS256"
                    )

                    return token
                else:
                    return "Error: Credenciales incorrectas."
        finally:
            conexion.close()

    @rpc(Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def actualizar_perfil(ctx, id_usuario, nombreUsuario, correoUsuario, avatarUrl):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as ejecutarConsulta:
                # 1. Actualizamos los datos del usuario en la BD
                sql_actualizar = """
                    UPDATE Usuarios 
                    SET nombreUsuario = %s, correoUsuario = %s, avatarUrl = %s 
                    WHERE id_usuario = %s
                """
                ejecutarConsulta.execute(
                    sql_actualizar,
                    (nombreUsuario, correoUsuario, avatarUrl, id_usuario),
                )
                conexion.commit()

                # 2. Buscamos los datos actualizados junto con el rol y fecha para re-generar el token
                sql_buscar = """
                    SELECT id_usuario, nombreUsuario, correoUsuario, rol, avatarUrl, fecha_registro 
                    FROM Usuarios 
                    WHERE id_usuario = %s
                """
                ejecutarConsulta.execute(sql_buscar, (id_usuario,))
                usuario = ejecutarConsulta.fetchone()

                if usuario:
                    id_user, nombre, correo, rol, avatar, fecha_reg = usuario
                    fecha_limpia = (
                        fecha_reg.strftime("%Y-%m-%d") if fecha_reg else "Reciente"
                    )

                    # 3. Creamos el nuevo Payload con los cambios hechos
                    payload = {
                        "id": id_user,
                        "nombre": nombre,
                        "correo": correo,
                        "rol": rol,
                        "avatarUrl": avatar,
                        "miembroDesde": fecha_limpia,
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
                    }

                    # 4. Encriptamos el nuevo token
                    nuevo_token = jwt.encode(
                        payload, Config.JWT_SECRET_KEY, algorithm="HS256"
                    )
                    return nuevo_token
                else:
                    return "Error: Usuario no encontrado tras la actualización."
        except Exception as e:
            return f"Error interno: {str(e)}"
        finally:
            conexion.close()


application = Application(
    [ServicioAutenticacion],
    tns="spyne.api.autenticacion.Prueba",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)


class CORSMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Si el navegador pregunta por los permisos (petición OPTIONS)
        if environ.get("REQUEST_METHOD") == "OPTIONS":
            start_response(
                "200 OK",
                [
                    ("Access-Control-Allow-Origin", "*"),
                    ("Access-Control-Allow-Methods", "POST, GET, OPTIONS"),
                    ("Access-Control-Allow-Headers", "Content-Type, SOAPAction"),
                ],
            )
            return [b""]

        # Interceptamos la respuesta normal para añadirle la cabecera de permiso
        def cors_start_response(status, headers, exc_info=None):
            headers.append(("Access-Control-Allow-Origin", "*"))
            return start_response(status, headers, exc_info)

        return self.app(environ, cors_start_response)


# ------------------------------------------------

if __name__ == "__main__":
    wsgi_app = WsgiApplication(application)

    # Envolvemos nuestra app con el CORS
    app_con_cors = CORSMiddleware(wsgi_app)

    # Encendemos el servidor con la app protegida
    server = make_server("0.0.0.0", 8000, app_con_cors)

    print("API SOAP iniciada en http://127.0.0.1:8000")
    print("WSDL disponible en http://127.0.0.1:8000/?wsdl")

    server.serve_forever()
