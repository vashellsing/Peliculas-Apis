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
                sql_insertar = "INSERT INTO Usuarios (nombreUsuario, correoUsuario, contrasenaUsuario, rol) VALUES (%s, %s, %s, 'cliente')"
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
                # IMPORTANTE: Ahora pedimos el ID y el ROL
                sql_buscar = "SELECT id_usuario, nombreUsuario, rol FROM Usuarios WHERE correoUsuario = %s AND contrasenaUsuario = %s"
                ejecutarConsulta.execute(sql_buscar, (correoUsuario, contrasenaUsuario))
                usuario = ejecutarConsulta.fetchone()

                if usuario:
                    id_user, nombre, rol = usuario

                    # Generamos el JWT
                    payload = {
                        "id": id_user,
                        "nombre": nombre,
                        "rol": rol,
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
                    }

                    token = jwt.encode(
                        payload, Config.JWT_SECRET_KEY, algorithm="HS256"
                    )

                    # Devolvemos el token. El cliente SOAP deberá guardarlo.
                    return token
                else:
                    return "Error: Credenciales incorrectas."
        finally:
            conexion.close()


application = Application(
    [ServicioAutenticacion],
    tns="spyne.api.autenticacion.Prueba",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

if __name__ == "__main__":
    wsgi_app = WsgiApplication(application)

    server = make_server("0.0.0.0", 8000, wsgi_app)

    print("API en http://127.0.0.1:8000")
    print("WSDL disponible en http://127.0.0.1:8000/?wsdl")

    server.serve_forever()
