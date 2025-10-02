#Adding basic authentication for our main.py file
import base64

USERS = {
    "admin": "pass123",}

def check_auth(handler):
    auth_header = handler.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Basic '):
        handler._send_json({'error': 'authorization required'}, status=401)
        return False

    encoded = auth_header.split(" ", 1)[1]
    try:
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
        return USERS.get(username) == password
    except Exception:
        return False
    
def require_auth(handler):
    if not check_auth(handler.headers.get("Authorization")):
        handler.send_response(401)
        handler.send_header("WWW-Authenticate", 'Basic realm="Access to API"')
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(b'{"error": "Unauthorized"}')
        return False
    return True

