from flask import request, jsonify, make_response
from itsdangerous import URLSafeTimedSerializer
from functools import wraps


# Configuración del token CSRF
secret_key = "bd18326f-fb1c-4266-8cc5-ae0f97dc58f9"
csrf_serializer = URLSafeTimedSerializer(secret_key)

class CSRFProvider:

    def generateCsrfToken():
        return csrf_serializer.dumps("csrf_token", salt="csrf-protection")

    def validateCsrfToken(token):
        try:
            csrf_serializer.loads(token, salt="csrf-protection", max_age=3600)
            return True
        except Exception:
            return False

    # Decorador para verificar CSRF en las solicitudes
    def csrf_protect( f ):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get("X-CSRF-Token")
            if not token or not CSRFProvider.validateCsrfToken(token):
                return jsonify({"error": "Invalid CSRF token"}), 403
            return f(*args, **kwargs)
        return decorated_function

    def getcsrftoken( self ):
        token = self.generateCsrfToken()
        response = make_response({"message": "CSRF token generated"})
        response.set_cookie('csrf_token', token, httponly=True, secure=True, samesite='Strict')
        return response