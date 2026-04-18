from flask import request, jsonify
from functools import wraps
from config import Config


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Buscamos el API key en los headers de la petición
        api_key_header = request.headers.get("X-API-KEY")

        if api_key_header and api_key_header == Config.API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Acceso denegado. API Key inválida."}), 401

    return decorated_function
