from flask import Flask
from flask_mysqldb import MySQL
from config import Config

# Inicializamos la aplicacion Flask
app = Flask(__name__)

# Cargamos la configuracion de la base de datos
app.config.from_object(Config)

# Inicializamos la conexion a MySQL
mysql = MySQL(app)

# -------------------------------------------------------------
# Importamos y registramos los Blueprints (Nuestras APIs)
# -------------------------------------------------------------
from routes.peliculas import peliculas_bp
app.register_blueprint(peliculas_bp)


# Encendemos el servidor
if __name__ == '__main__':
    print("Iniciando la API REST de Peliculas en el puerto 5000...")
    app.run(debug=True, port=5000)