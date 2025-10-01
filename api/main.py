from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import re
from urllib.parse import parse_qs, urlparse

PORT = 8000

_users = {}
_next_user_id = 1

# Transactions will mirror the 'sms' entities from database/xml_to_json.json
_transactions = {}
_next_transaction_counter = 1

def _load_transactions_from_file(path='database/xml_to_json.json'):
    global _transactions, _next_transaction_counter
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        sms_list = data.get('sms', [])
        for item in sms_list:
            # expect item has 'id'
            tid = item.get('id')
            if tid:
                _transactions[tid] = item
        # derive next counter from existing ids (numbers at end)
        max_num = 0
        for tid in _transactions.keys():
            m = re.search(r'(\d+)$', tid)
            if m:
                max_num = max(max_num, int(m.group(1)))
        _next_transaction_counter = max_num + 1
    except FileNotFoundError:
        # no file yet; start fresh
        _transactions = {}
        _next_transaction_counter = 1
    except Exception:
        _transactions = {}
        _next_transaction_counter = 1

def _next_transaction_id():
    global _next_transaction_counter
    nid = f'SMS_{_next_transaction_counter:04d}'
    _next_transaction_counter += 1
    return nid

def _save_transactions_to_file(path='database/xml_to_json.json'):
    # load existing file if present, replace 'sms' with current transactions list
    try:
        data = {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        data['sms'] = list(_transactions.values())
        # ensure other top-level keys exist
        for k in ('user','transaction_category','transaction','system_log','service_centre','backup'):
            data.setdefault(k, [])
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception:
        # on failure, skip persisting to avoid crashing the API
        pass

def _next_id():
    global _next_user_id
    uid = _next_user_id
    _next_user_id += 1
    return str(uid)

class SimpleRESTHandler(BaseHTTPRequestHandler):

    routes = []

    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _parse_json_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return 'BAD_JSON'

    def _send_json(self, obj, status=200):
        self._set_headers(status=status)
        payload = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.wfile.write(payload)

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_GET(self):
        self._dispatch('GET')

    def do_POST(self):
        self._dispatch('POST')

    def do_PUT(self):
        self._dispatch('PUT')

    def do_DELETE(self):
        self._dispatch('DELETE')

    def _dispatch(self, method):
        path = urlparse(self.path).path
        for (m, pattern, handler) in self.routes:
            if m != method:
                continue
            match = pattern.match(path)
            if match:
                try:
                    handler(self, **match.groupdict())
                except Exception as e:
                    self._send_json({'error': 'internal server error', 'detail': str(e)}, status=500)
                return
        self._send_json({'error': 'not found'}, status=404)

# Handlers for /users resource
def list_users(handler):
    handler._send_json({'users': list(_users.values())})

# --- Transactions handlers (map to sms entries) ---
def list_transactions(handler):
    handler._send_json({'transactions': list(_transactions.values())})

def get_transaction(handler, transaction_id):
    t = _transactions.get(transaction_id)
    if not t:
        handler._send_json({'error': 'transaction not found'}, status=404)
        return
    handler._send_json(t)

def create_transaction(handler):
    body = handler._parse_json_body()
    if body == 'BAD_JSON':
        handler._send_json({'error': 'invalid json'}, status=400)
        return
    if not isinstance(body, dict):
        handler._send_json({'error': 'invalid payload'}, status=400)
        return
    tid = _next_transaction_id()
    # allow caller to supply some fields; ensure id present
    record = {'id': tid}
    record.update(body)
    _transactions[tid] = record
    _save_transactions_to_file()
    handler._send_json(record, status=201)

def update_transaction(handler, transaction_id):
    body = handler._parse_json_body()
    if body == 'BAD_JSON':
        handler._send_json({'error': 'invalid json'}, status=400)
        return
    t = _transactions.get(transaction_id)
    if not t:
        handler._send_json({'error': 'transaction not found'}, status=404)
        return
    # apply partial updates except id
    for k, v in (body.items() if isinstance(body, dict) else []):
        if k == 'id':
            continue
        t[k] = v
    _save_transactions_to_file()
    handler._send_json(t)

def delete_transaction(handler, transaction_id):
    if transaction_id in _transactions:
        del _transactions[transaction_id]
        _save_transactions_to_file()
        handler._send_json({'deleted': transaction_id})
    else:
        handler._send_json({'error': 'transaction not found'}, status=404)

def get_user(handler, user_id):
    u = _users.get(user_id)
    if not u:
        handler._send_json({'error': 'user not found'}, status=404)
        return
    handler._send_json(u)

def create_user(handler):
    body = handler._parse_json_body()
    if body == 'BAD_JSON':
        handler._send_json({'error': 'invalid json'}, status=400)
        return
    if not isinstance(body, dict) or 'name' not in body:
        handler._send_json({'error': 'name required'}, status=400)
        return
    uid = _next_id()
    user = {'id': uid, 'name': body['name']}
    _users[uid] = user
    handler._send_json(user, status=201)

def update_user(handler, user_id):
    body = handler._parse_json_body()
    if body == 'BAD_JSON':
        handler._send_json({'error': 'invalid json'}, status=400)
        return
    user = _users.get(user_id)
    if not user:
        handler._send_json({'error': 'user not found'}, status=404)
        return
    # allow partial updates
    user.update({k: v for k, v in body.items() if k != 'id'})
    handler._send_json(user)

def delete_user(handler, user_id):
    if user_id in _users:
        del _users[user_id]
        handler._send_json({'deleted': user_id})
    else:
        handler._send_json({'error': 'user not found'}, status=404)

# register routes (regex with named groups)
SimpleRESTHandler.routes = [
    ('GET', re.compile(r'^/users/?$'), lambda h: list_users(h)),
    ('POST', re.compile(r'^/users/?$'), lambda h: create_user(h)),
    ('GET', re.compile(r'^/users/(?P<user_id>\d+)/?$'), lambda h, user_id: get_user(h, user_id)),
    ('PUT', re.compile(r'^/users/(?P<user_id>\d+)/?$'), lambda h, user_id: update_user(h, user_id)),
    ('DELETE', re.compile(r'^/users/(?P<user_id>\d+)/?$'), lambda h, user_id: delete_user(h, user_id)),
    # transactions endpoints
    ('GET', re.compile(r'^/transactions/?$'), lambda h: list_transactions(h)),
    ('POST', re.compile(r'^/transactions/?$'), lambda h: create_transaction(h)),
    ('GET', re.compile(r'^/transactions/(?P<transaction_id>[^/]+)/?$'), lambda h, transaction_id: get_transaction(h, transaction_id)),
    ('PUT', re.compile(r'^/transactions/(?P<transaction_id>[^/]+)/?$'), lambda h, transaction_id: update_transaction(h, transaction_id)),
    ('DELETE', re.compile(r'^/transactions/(?P<transaction_id>[^/]+)/?$'), lambda h, transaction_id: delete_transaction(h, transaction_id)),
]

def run(server_class=ThreadingHTTPServer, handler_class=SimpleRESTHandler, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port} ...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down...')
        httpd.server_close()

if __name__ == '__main__':
    # load transactions from the json file (if present) before starting
    _load_transactions_from_file()
    run()