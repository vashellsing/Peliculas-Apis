import jwt
from functools import wraps
from flask import request, jsonify
from config import Config


# --- DECORADOR 1: SOLO API KEY ---
# Úsalo para rutas públicas que solo requieren que la APP esté autorizada
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if not api_key or api_key != Config.API_KEY:
            return jsonify({"error": "API Key inválida o faltante"}), 403
        return f(*args, **kwargs)

    return decorated_function


# --- DECORADOR 2: JWT CON ROLES ---
# Úsalo para proteger acciones de usuarios (clientes o admins)
def require_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Acceso denegado. Falta el token (Bearer)."}), 401

        try:
            # Aquí se decodifica y se extrae el ROL que viene dentro del token
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            request.current_user = payload  # <--- AQUÍ ESTÁ LA CLAVE
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "El token ha expirado."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido."}), 401

        return f(*args, **kwargs)

    return decorated_function


def require_role(roles_permitidos):
    """Verifica si el usuario tiene el permiso (admin/usuario) dentro del token"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            usuario = getattr(request, "current_user", None)
            if not usuario or usuario.get("rol") not in roles_permitidos:
                return (
                    jsonify(
                        {
                            "error": f"Permisos insuficientes. Se requiere rol: {roles_permitidos}"
                        }
                    ),
                    403,
                )
            return f(*args, **kwargs)

        return decorated_function

    return decorator
