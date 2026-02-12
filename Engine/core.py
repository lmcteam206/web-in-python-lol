import json
import os
import mimetypes
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
            return {} # Start with an empty generic dictionary
        with open(self.filename, "r") as f:
            return json.load(f)
            
class ShadowEngine(BaseHTTPRequestHandler):
    """General Purpose Web Engine."""
    routes = {} 

    def do_GET(self):
        """Serves files, handles routes, and parses query parameters."""
        
        # 1. PARSE PATH AND QUERY
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        # This makes ?name=JinWoo accessible to the user's function
        query_params = parse_qs(parsed_url.query)
        # Clean up query_params (convert lists to single values)
        query_params = {k: v[0] for k, v in query_params.items()}

        # 2. STATIC FILE CHECK
        requested_file = path.lstrip("/")
        if requested_file and os.path.isfile(requested_file):
            self.send_response(200)
            mime_type, _ = mimetypes.guess_type(requested_file)
            self.send_header("Content-type", mime_type or "application/octet-stream")
            self.end_headers()
            with open(requested_file, "rb") as f:
                self.wfile.write(f.read())
            return 

        # 3. ROUTE HANDLING
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        if path in ShadowEngine.routes:
            # We now pass query_params to the function!
            page_content = ShadowEngine.routes[path](query_params)
        else:
            page_content = "<h1 style='text-align:center; margin-top:50px;'>404: Gate Not Found</h1>"

        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                * {{ box-sizing: border-box; }}
                body {{
                    margin: 0; padding: 0; background: #0e1117; color: white;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    display: flex; flex-direction: column; min-height: 100vh;
                }}
            </style>
        </head>
        <body>{page_content}</body>
        </html>
        """
        self.wfile.write(bytes(full_html, "utf-8"))

    def do_POST(self):
        """Handles generic form submissions."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = {k: v[0] for k, v in parse_qs(post_data).items()}
        
        # Determine where to send the POST data based on the path
        path = self.path.split("?")[0]
        
        if hasattr(self, 'server') and hasattr(self.server, 'app_instance'):
            # The User handles logic inside their specific POST route
            # For simplicity, we trigger the route function if it exists
            if path in ShadowEngine.routes:
                ShadowEngine.routes[path](params, is_post=True)

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

class WebApp:
    def __init__(self, storage_file="save.json"):
        self.app_logic = Application(storage_file) 
        self.data = self.app_logic.load()

    def page(self, path):
        def wrapper(func):
            ShadowEngine.routes[path] = func
            return func
        return wrapper
    
    def build_page(self, components):
        return "".join([c.render() for c in components])
    
    def start(self, port=8080):
        print(f"Engine Online. Gate open at http://localhost:{port}")
        server = HTTPServer(("localhost", port), ShadowEngine)
        server.app_instance = self 
        threading.Timer(1, lambda: webbrowser.open(f"http://localhost:{port}")).start()
        server.serve_forever()