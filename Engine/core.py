import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import webbrowser

class Application:
    def __init__(self, filename="save.json"):
        self.filename = filename

    def save(self, data):
        """Saves any Python dictionary to the JSON file."""
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        if not os.path.exists(self.filename):
            # EVERYTHING you use in your UI must be defined here!
            return {
                "level": 1, 
                "xp": 0, 
                "rank": "E",
                "str": 10,  # Added this
                "agi": 10,  # Added this
                "int": 10   # Added this
            }
        with open(self.filename, "r") as f:
            return json.load(f)
            
class ShadowEngine(BaseHTTPRequestHandler):
    routes = {} 

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # Check if requested URL exists
        # Basic parsing to handle query parameters (like ?id=1)
        path = self.path.split("?")[0]
        
        if path in ShadowEngine.routes:
            page_content = ShadowEngine.routes[path]()
        else:
            page_content = "<h1 style='text-align:center; margin-top:50px;'>404: Gate Not Found</h1>"

        # THE MAGIC HAPPENS HERE:
        # We set min-height: 100vh and display: flex on the body.
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                * {{ box-sizing: border-box; }}
                body {{
                    margin: 0;
                    padding: 0;
                    background: #0e1117;
                    color: white;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    display: flex;
                    flex-direction: column;
                    min-height: 100vh; /* Forces body to be at least screen height */
                }}
            </style>
        </head>
        <body>
            {page_content}
        </body>
        </html>
        """
        self.wfile.write(bytes(full_html, "utf-8"))

class WebApp:
    def __init__(self):
        self.app_logic = Application() 
        self.data = self.app_logic.load()

    def page(self, path):
        def wrapper(func):
            ShadowEngine.routes[path] = func
            return func
        return wrapper
    
    def build_page(self, components):
        # We wrap the components. If a Footer has margin-top: auto, 
        # it will now stick to the bottom because of the flex body above.
        return "".join([c.render() for c in components])
    
    def start(self):
        print("System Initialized. Accessing Gate at http://localhost:8080")
        server = HTTPServer(("localhost", 8080), ShadowEngine)
        threading.Timer(1, lambda: webbrowser.open("http://localhost:8080")).start()
        server.serve_forever()