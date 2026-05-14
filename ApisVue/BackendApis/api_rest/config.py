class Config:
    # Conexion a la bd
    
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '' 
    MYSQL_DB = 'webpeliculasDB'

# Esta llave la deben conocer las apps que consumen tu API
    API_KEY = 'mi_super_api_key_fija_123'
    
    # Esta llave es solo del servidor para firmar los tokens
    JWT_SECRET_KEY = 'firma_secreta_para_usuarios_abc'