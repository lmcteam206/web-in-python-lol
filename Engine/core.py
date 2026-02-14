import requests
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
class Component:
    """Base class for all UI elements."""
    def render(self):
        return ""

# --- FREE COMPONENTS (Enhanced Aesthetics) ---

class Text(Component):
    def __init__(self, content, size="16px", color="#ffffff", bold=False, align="left"):
        self.content = content
        self.size = size
        self.color = color
        self.weight = "700" if bold else "400"
        self.align = align

    def render(self):
        return f"""
        <div style="color: {self.color}; font-size: {self.size}; font-weight: {self.weight}; 
                    text-align: {self.align}; font-family: 'Inter', -apple-system, sans-serif; 
                    margin: 12px 0; line-height: 1.6; letter-spacing: -0.01em;">
            {self.content}
        </div>
        """

class Container(Component):
    def __init__(self, items, max_width="1100px"):
        self.items = items
        self.max_width = max_width

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f'<div style="max-width: {self.max_width}; margin: 0 auto; padding: 40px 20px;">{content}</div>'

class Row(Component):
    def __init__(self, items, gap="20px", justify="center"):
        self.items = items
        self.gap = gap
        self.justify = justify

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f"""
        <div style="display: flex; flex-wrap: wrap; justify-content: {self.justify}; 
                    gap: {self.gap}; width: 100%; align-items: stretch;">
            {content}
        </div>
        """

class Card(Component):
    def __init__(self, items, bg="#161616", shadow=True):
        self.items = items
        self.bg = bg
        self.shadow = "0 20px 40px rgba(0,0,0,0.4)" if shadow else "none"

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f"""
        <div style="background: {self.bg}; padding: 30px; border-radius: 20px; 
                    box-shadow: {self.shadow}; border: 1px solid #2a2a2a;
                    transition: transform 0.3s ease, border-color 0.3s ease;
                    flex: 1; min-width: 280px; max-width: 100%;">
            {content}
        </div>
        """

class Image(Component):
    def __init__(self, url, size="120px", circular=False, border=True):
        self.url = url
        self.size = size
        self.radius = "50%" if circular else "16px"
        self.border = "3px solid #333" if border else "none"

    def render(self):
        return f"""
        <div style="width: {self.size}; height: {self.size}; margin: 0 auto 15px auto;">
            <img src="{self.url}" style="width: 100%; height: 100%; object-fit: cover; 
                   border-radius: {self.radius}; border: {self.border}; display: block;">
        </div>
        """

# --- FORM COMPONENTS (Modern Dark Mode UI) ---

class TextInput(Component):
    def __init__(self, label, name, placeholder="", type="text"):
        self.label = label
        self.name = name
        self.placeholder = placeholder
        self.type = type

    def render(self):
        return f"""
        <div style="margin-bottom: 20px; width: 100%; font-family: sans-serif;">
            <label style="display: block; font-size: 12px; font-weight: 600; margin-bottom: 8px; 
                          color: #666; text-transform: uppercase; letter-spacing: 1px;">{self.label}</label>
            <input type="{self.type}" name="{self.name}" placeholder="{self.placeholder}" 
                   style="width: 100%; padding: 14px; border-radius: 10px; border: 1px solid #333; 
                   background: #0f0f0f; color: white; font-size: 15px; outline: none; transition: border 0.3s;">
        </div>
        """

class Form(Component):
    def __init__(self, action_url, items, submit_text="Continue", has_files=False):
        self.action_url = action_url
        self.items = items
        self.submit_text = submit_text
        self.enctype = 'enctype="multipart/form-data"' if has_files else ""

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f"""
        <form action="{self.action_url}" method="POST" {self.enctype} 
              style="display: flex; flex-direction: column; width: 100%; max-width: 400px; margin: 0 auto;">
            {content}
            <button type="submit" style="margin-top: 10px; padding: 16px; background: #fff; 
                    color: #000; border: none; border-radius: 12px; cursor: pointer; 
                    font-weight: 700; font-size: 15px; transition: opacity 0.2s;">
                {self.submit_text}
            </button>
        </form>
        """

