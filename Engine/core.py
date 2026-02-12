import json
import os
import mimetypes
import re
import cgi 
import traceback # Added to capture error details
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import webbrowser
from urllib.parse import parse_qs, urlparse

class Application:
    """Handles generic JSON data persistence."""
    def __init__(self, filename="save.json"):
        self.filename = filename

    def save(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
            
class ShadowEngine(BaseHTTPRequestHandler):
    routes = [] 

    def render_error(self, err, tb_info):
        """Beautifully renders a system crash page."""
        return f"""
        <div style="max-width: 800px; margin: 50px auto; background: #1a1a1a; border-left: 5px solid #ff4b4b; padding: 30px; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <h1 style="color: #ff4b4b; margin-top: 0; font-family: 'Courier New', Courier, monospace;">[SYSTEM_CRASH]</h1>
            <p style="color: #eee; font-size: 18px;">The engine encountered a logic error while rendering this gate.</p>
            <div style="background: #000; padding: 20px; border-radius: 4px; overflow-x: auto;">
                <code style="color: #ff4b4b; font-weight: bold;">Error: {err}</code>
                <pre style="color: #888; font-size: 12px; margin-top: 15px; white-space: pre-wrap;">{tb_info}</pre>
            </div>
            <p style="margin-top: 20px;"><a href="/" style="color: #00ffcc; text-decoration: none;">&larr; Return to Dashboard</a></p>
        </div>
        """

    def find_route(self, path):
        for pattern, _, func in self.routes:
            match = pattern.match(path)
            if match:
                return func, match.groups()
        return None, []

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}

        requested_file = path.lstrip("/")
        if requested_file and os.path.isfile(requested_file):
            self.send_response(200)
            mime_type, _ = mimetypes.guess_type(requested_file)
            self.send_header("Content-type", mime_type or "application/octet-stream")
            self.end_headers()
            with open(requested_file, "rb") as f:
                self.wfile.write(f.read())
            return 

        func, args = self.find_route(path)
        
        # --- START ERROR BOUNDARY ---
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if func:
            try:
                page_content = func(query_params, *args)
            except Exception as e:
                # Catch the error and the traceback
                tb_info = traceback.format_exc()
                page_content = self.render_error(e, tb_info)
        else:
            page_content = "<h1 style='text-align:center; margin-top:50px;'>404: Gate Not Found</h1>"

        full_html = f"<!DOCTYPE html><html><head><style>body{{margin:0;padding:0;background:#0e1117;color:white;font-family:sans-serif;}}</style></head><body>{page_content}</body></html>"
        self.wfile.write(bytes(full_html, "utf-8"))

    def do_POST(self):
        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type']}
            )

            params = {}
            for key in form.keys():
                field_item = form[key]
                if field_item.filename:
                    file_data = field_item.file.read()
                    with open(field_item.filename, "wb") as f:
                        f.write(file_data)
                    params[key] = field_item.filename
                else:
                    params[key] = field_item.value
            
            path = urlparse(self.path).path
            func, args = self.find_route(path)
            
            if func:
                func(params, *args, is_post=True)

            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        except Exception as e:
            # If POST fails, we show the error instead of redirecting
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            tb_info = traceback.format_exc()
            err_page = f"<!DOCTYPE html><html><body style='background:#0e1117;color:white;font-family:sans-serif;'>{self.render_error(e, tb_info)}</body></html>"
            self.wfile.write(bytes(err_page, "utf-8"))

class WebApp:
    def __init__(self, storage_file="save.json"):
        self.app_logic = Application(storage_file) 
        self.data = self.app_logic.load()

    def page(self, path):
        def wrapper(func):
            regex_path = re.compile(f"^{path}$")
            ShadowEngine.routes.append((regex_path, path, func))
            return func
        return wrapper
    
    def build_page(self, components):
        return "".join([c.render() for c in components])
    
    def start(self, port=8080):
        print(f"Engine Online. Access at http://localhost:{port}")
        server = HTTPServer(("localhost", port), ShadowEngine)
        server.app_instance = self 
        threading.Timer(1, lambda: webbrowser.open(f"http://localhost:{port}")).start()
        server.serve_forever()