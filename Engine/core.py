import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import webbrowser

class Application:
    """
    Handles data persistence for the System. 
    Manages saving and loading state from a local JSON file.
    
    Args:
        filename (str): The name of the file used for storage. Defaults to 'save.json'.
    """
    def __init__(self, filename="save.json"):
        self.filename = filename

    def save(self, data):
        """
        Serializes a Python dictionary to the JSON storage file.
        
        Args:
            data (dict): The dictionary containing system state/stats to save.
        """
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        """
        Loads the system data from the JSON file. 
        If the file does not exist, returns a default 'New Hunter' starting state.
        
        Returns:
            dict: The loaded data or the default initial dictionary.
        """
        if not os.path.exists(self.filename):
            return {
                "level": 1, 
                "xp": 0, 
                "rank": "E",
                "str": 10,
                "agi": 10,
                "int": 10,
                "videos": []
            }
        with open(self.filename, "r") as f:
            return json.load(f)
            
class ShadowEngine(BaseHTTPRequestHandler):
    """
    The Custom HTTP Request Handler. 
    Processes incoming GET requests and injects rendered components into a 
    pre-styled HTML shell with a Flexbox layout.
    """
    routes = {} 

    def do_GET(self):
        """Handles incoming HTTP GET requests, performs routing, and returns HTML."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # Path parsing to ignore query strings
        path = self.path.split("?")[0]
        
        if path in ShadowEngine.routes:
            page_content = ShadowEngine.routes[path]()
        else:
            page_content = "<h1 style='text-align:center; margin-top:50px;'>404: Gate Not Found</h1>"

        # Global System CSS Shell
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
                    min-height: 100vh;
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
    """
    The main interface for creating web applications. 
    Provides decorators for routing and methods for building pages.
    """
    def __init__(self):
        self.app_logic = Application() 
        self.data = self.app_logic.load()

    def page(self, path):
        """
        A decorator to register a function as a view for a specific URL path.
        
        Args:
            path (str): The URL endpoint (e.g., '/', '/profile').
        """
        def wrapper(func):
            ShadowEngine.routes[path] = func
            return func
        return wrapper
    
    def build_page(self, components):
        """
        Renders a list of components into a single string of HTML.
        
        Args:
            components (list[Component]): The UI elements to render on the page.
            
        Returns:
            str: The final concatenated HTML.
        """
        return "".join([c.render() for c in components])
    
    def start(self):
        """
        Initializes the HTTPServer, opens the default web browser, 
        and begins listening for requests at http://localhost:8080.
        """
        print("System Initialized. Accessing Gate at http://localhost:8080")
        server = HTTPServer(("localhost", 8080), ShadowEngine)
        threading.Timer(1, lambda: webbrowser.open("http://localhost:8080")).start()
        server.serve_forever()