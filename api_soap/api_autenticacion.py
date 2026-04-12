import logging
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import pymysql
''' Conexión a la base de datos '''
# conexion a bd similar a php xd
def obtener_conexion():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='', 
        db='webpeliculasDB'
    )

#la clase del servicio, aca metemos las funciones
class ServicioAutenticacion(ServiceBase):
    
    # --- funcion de registrar usuario ---
    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def registrar_usuario(ctx, nombreUsuario, correoUsuario, contrasenaUsuario):
        conexion = obtener_conexion()
        
        try: 
           
            with conexion.cursor() as ejecutarConsulta:
                
               
                sql_verificar = "SELECT id_Usuario FROM Usuarios WHERE correoUsuario = %s"
                ejecutarConsulta.execute(sql_verificar, (correoUsuario,))
                resultado = ejecutarConsulta.fetchone()
                
                if resultado is not None:
                    return "Error: Ese correo ya existe en la base de datos."
                else:
                    sql_insertar = "INSERT INTO Usuarios (nombreUsuario, correoUsuario, contrasenaUsuario) VALUES (%s, %s, %s)"
                    ejecutarConsulta.execute(sql_insertar, (nombreUsuario, correoUsuario, contrasenaUsuario))
                    conexion.commit()
                    return "exito: usuario registrado correctamente."
                    
        finally:
            
            conexion.close() 

    # --- funcion de iniciar sesion ---
    @rpc(Unicode, Unicode, _returns=Unicode)
    def iniciar_sesion(ctx, correoUsuario, contrasenaUsuario):
        conexion = obtener_conexion()
        
        try:
            
            with conexion.cursor() as ejecutarConsulta:
                
                # Buscamos al usuario en la bd como en sql xd
                sql_buscar = "SELECT nombreUsuario FROM Usuarios WHERE correoUsuario = %s AND contrasenaUsuario = %s"
                ejecutarConsulta.execute(sql_buscar, (correoUsuario, contrasenaUsuario))
                usuario = ejecutarConsulta.fetchone()
                
                if usuario is not None:
                    # si el usuario existe inicia sesion
                    return "Bienvenido, " + usuario[0] + "! Has iniciado sesión."
                else:
                    return "Error: el usuario no existe o la contraseña es incorrecta."
                    
        finally:
            # Cerramos la conexión siempre
            conexion.close()

application = Application(
    [ServicioAutenticacion],
    tns='spyne.api.autenticacion.Prueba',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    
    server = make_server('0.0.0.0', 8000, wsgi_app) 
    
    print("API en http://127.0.0.1:8000")
    print("WSDL disponible en http://127.0.0.1:8000/?wsdl")
    
    server.serve_forever()