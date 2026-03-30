from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import mimetypes
import os

class ChatHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/chat/'):
            # SPA route — serve index.html and let the client handle it
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read().encode()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content)
        elif self.path.startswith('/asset/'):
            # /asset/<conv_id>/<file_id>  — serve media by filename prefix
            remainder = self.path[7:]  # strip '/asset/'
            slash = remainder.find('/')
            if slash == -1:
                self.send_error(400, "Bad request")
                return
            conv_id = remainder[:slash]
            file_id = remainder[slash + 1:]
            # Search conv subdir first, then chats root
            search_roots = [os.path.join('chats', conv_id), 'chats']
            found = None
            for search_root in search_roots:
                if not os.path.isdir(search_root):
                    continue
                for dirpath, _, filenames in os.walk(search_root):
                    for fname in filenames:
                        if fname.startswith(file_id):
                            found = os.path.join(dirpath, fname)
                            break
                    if found:
                        break
                if found:
                    break
            if not found:
                self.send_error(404, "Asset not found")
                return
            content_type, _ = mimetypes.guess_type(found)
            if not content_type:
                content_type = 'application/octet-stream'
            with open(found, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        elif self.path == '/list_chats':
            chats = []
            for filename in os.listdir('chats'):
                if not filename.endswith('.json'):
                    continue
                filepath = os.path.join('chats', filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    chats.append({
                        'id': filename,
                        'title': data.get('title') or filename.replace('.json', ''),
                        'create_time': data.get('create_time'),
                    })
                except Exception:
                    chats.append({'id': filename, 'title': filename.replace('.json', ''), 'create_time': None})
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(chats).encode())
        elif self.path.startswith('/chats/'):
            # Handle request for specific chat
            chat_file = self.path[7:]  # Remove '/chats/' from path
            chat_path = os.path.join('chats', chat_file)
            
            if os.path.exists(chat_path):
                with open(chat_path, 'r', encoding='utf-8') as f:
                    chat_data = json.load(f)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(chat_data).encode())
            else:
                self.send_error(404, "Chat not found")
        else:
            # Use default handler for all other requests
            return SimpleHTTPRequestHandler.do_GET(self)

    def end_headers(self):
        # Добавляем CORS заголовки
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        SimpleHTTPRequestHandler.end_headers(self)

def run(server_class=HTTPServer, handler_class=ChatHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Запуск сервера на порту {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run() 