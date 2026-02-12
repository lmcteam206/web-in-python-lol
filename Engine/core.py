import json
import os
import mimetypes
import re
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
    """Upgraded Web Engine with Dynamic Routing."""
    # routes now stores (compiled_regex, original_path, function)
    routes = [] 

    def find_route(self, path):
        """Matches a URL path against registered regex patterns."""
        for pattern, _, func in self.routes:
            match = pattern.match(path)
            if match:
                return func, match.groups()
        return None, []

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}

        # 1. STATIC FILE CHECK
        requested_file = path.lstrip("/")
        if requested_file and os.path.isfile(requested_file):
            self.send_response(200)
            mime_type, _ = mimetypes.guess_type(requested_file)
            self.send_header("Content-type", mime_type or "application/octet-stream")
            self.end_headers()
            with open(requested_file, "rb") as f:
                self.wfile.write(f.read())
            return 

        # 2. DYNAMIC ROUTE HANDLING
        func, args = self.find_route(path)
        
        if func:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # Pass query params AND any URL variables (slugs)
            page_content = func(query_params, *args)
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            page_content = "<h1 style='text-align:center; margin-top:50px;'>404: Gate Not Found</h1>"

        full_html = f"<!DOCTYPE html><html><head><style>body{{margin:0;padding:0;background:#0e1117;color:white;font-family:sans-serif;}}</style></head><body>{page_content}</body></html>"
        self.wfile.write(bytes(full_html, "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = {k: v[0] for k, v in parse_qs(post_data).items()}
        
        path = urlparse(self.path).path
        func, args = self.find_route(path)
        
        if func:
            # Execute logic with is_post flag
            func(params, *args, is_post=True)

        # Redirect to home after POST to prevent "Form Resubmission" errors
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

class WebApp:
    def __init__(self, storage_file="save.json"):
        self.app_logic = Application(storage_file) 
        self.data = self.app_logic.load()

    def page(self, path):
        """
        Decorator that supports dynamic variables.
        Example: @web.page("/profile/([a-zA-Z0-9]+)")
        """
        def wrapper(func):
            # Compile the path into a Regex pattern
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