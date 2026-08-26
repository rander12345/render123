import json
import os
import sqlite3
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).parent
DATABASE = ROOT / 'school_registrations.db'


def load_environment_file():
    environment_file = ROOT / '.env'
    if not environment_file.exists():
        return
    for line in environment_file.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        name, value = line.split('=', 1)
        os.environ.setdefault(name.strip(), value.strip().strip('"').strip("'"))


load_environment_file()


def send_telegram_notification(message):
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    if not token or not chat_id:
        return False

    endpoint = f'https://api.telegram.org/bot{token}/sendMessage'
    request_body = urlencode({'chat_id': chat_id, 'text': message}).encode('utf-8')
    request = Request(endpoint, data=request_body, method='POST')
    try:
        with urlopen(request, timeout=5) as response:
            return response.status == 200
    except OSError as error:
        print(f'Telegram notification failed: {error}')
        return False


def connect_database():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            school TEXT NOT NULL,
            registered_at TEXT NOT NULL
        )
    ''')
    connection.execute('''
        CREATE TABLE IF NOT EXISTS login_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identity TEXT NOT NULL,
            display_name TEXT NOT NULL,
            registered_at TEXT NOT NULL
        )
    ''')
    connection.execute('''
        CREATE TABLE IF NOT EXISTS ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            idea TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    connection.commit()
    return connection


class AppHandler(SimpleHTTPRequestHandler):
    def send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        # Allow cross-origin requests from the frontend (Netlify)
        self.send_header('Access-Control-Allow-Origin', os.environ.get('CORS_ALLOW_ORIGIN', '*'))
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        # Respond to CORS preflight requests
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', os.environ.get('CORS_ALLOW_ORIGIN', '*'))
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/registrations':
            with connect_database() as connection:
                rows = connection.execute(
                    'SELECT id, school, registered_at FROM registrations ORDER BY registered_at DESC'
                ).fetchall()
            self.send_json([dict(row) for row in rows])
            return
        if self.path == '/api/login-registrations':
            with connect_database() as connection:
                rows = connection.execute(
                    'SELECT id, identity, display_name, registered_at FROM login_registrations ORDER BY registered_at DESC'
                ).fetchall()
            self.send_json([dict(row) for row in rows])
            return
        if self.path == '/api/ideas':
            with connect_database() as connection:
                rows = connection.execute(
                    'SELECT id, name, idea, created_at FROM ideas ORDER BY created_at DESC'
                ).fetchall()
            self.send_json([dict(row) for row in rows])
            return
        super().do_GET()

    def do_POST(self):
        if self.path not in ('/api/registrations', '/api/login-registrations', '/api/ideas'):
            self.send_error(404)
            return

        try:
            length = int(self.headers.get('Content-Length', 0))
            payload = json.loads(self.rfile.read(length))
            if self.path == '/api/registrations':
                school = str(payload.get('school', '')).strip()
            elif self.path == '/api/login-registrations':
                identity = str(payload.get('identity', '')).strip()
                display_name = str(payload.get('display_name', '')).strip()
            else:
                name = str(payload.get('name', '')).strip() or 'Ẩn danh'
                idea = str(payload.get('idea', '')).strip()
        except (ValueError, json.JSONDecodeError):
            self.send_json({'error': 'Dữ liệu không hợp lệ.'}, 400)
            return

        if self.path == '/api/registrations' and (not school or len(school) > 200):
            self.send_json({'error': 'Tên trường học phải có từ 1 đến 200 ký tự.'}, 400)
            return
        if self.path == '/api/login-registrations' and (not identity or not display_name or len(identity) > 200 or len(display_name) > 200):
            self.send_json({'error': 'Thông tin đăng nhập không hợp lệ.'}, 400)
            return
        if self.path == '/api/ideas' and (not idea or len(name) > 200 or len(idea) > 2000):
            self.send_json({'error': 'Ý tưởng không hợp lệ.'}, 400)
            return

        registered_at = datetime.now(timezone.utc).isoformat()
        with connect_database() as connection:
            if self.path == '/api/registrations':
                cursor = connection.execute(
                    'INSERT INTO registrations (school, registered_at) VALUES (?, ?)',
                    (school, registered_at)
                )
            elif self.path == '/api/login-registrations':
                cursor = connection.execute(
                    'INSERT INTO login_registrations (identity, display_name, registered_at) VALUES (?, ?, ?)',
                    (identity, display_name, registered_at)
                )
            else:
                cursor = connection.execute(
                    'INSERT INTO ideas (name, idea, created_at) VALUES (?, ?, ?)',
                    (name, idea, registered_at)
                )
            registration_id = cursor.lastrowid

        if self.path == '/api/registrations':
            send_telegram_notification(
                f'Đăng ký trường học mới\nTrường: {school}\nThời gian: {registered_at}'
            )
            self.send_json({'id': registration_id, 'school': school, 'registered_at': registered_at}, 201)
        elif self.path == '/api/login-registrations':
            send_telegram_notification(
                f'Lượt đăng nhập/đăng ký mới\nTên: {display_name}\nĐịnh danh: {identity}\nThời gian: {registered_at}'
            )
            self.send_json({'id': registration_id, 'identity': identity, 'display_name': display_name, 'registered_at': registered_at}, 201)
        else:
            self.send_json({'id': registration_id, 'name': name, 'idea': idea, 'created_at': registered_at}, 201)

    def do_DELETE(self):
        if self.path not in ('/api/registrations', '/api/login-registrations', '/api/ideas'):
            self.send_error(404)
            return
        with connect_database() as connection:
            table = {
                '/api/registrations': 'registrations',
                '/api/login-registrations': 'login_registrations',
                '/api/ideas': 'ideas'
            }[self.path]
            connection.execute(f'DELETE FROM {table}')
        self.send_json({'success': True})


if __name__ == '__main__':
    connect_database().close()
    port = int(os.environ.get('PORT', '4173'))
    server = ThreadingHTTPServer(('0.0.0.0', port), AppHandler)
    print(f'Server running at http://localhost:{port}')
    server.serve_forever()
