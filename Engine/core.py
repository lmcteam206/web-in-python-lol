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
        if self.path == '/__ping__':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"pong")
            return
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

        auto_refresh_script = """
        <script>
            let lastCheck = Date.now();
            setInterval(async () => {
                try {
                    const response = await fetch('/__ping__');
                    if (response.ok) {
                        // Optional: You could compare a server-side timestamp here 
                        // to trigger reload only on code changes.
                    }
                } catch (e) {
                    // Server is likely restarting...
                    console.log("Server unreachable, waiting to reconnect...");
                    setTimeout(() => location.reload(), 1000);
                }
            }, 1000);
        </script>
        """
        full_html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <style>body{{margin:0;padding:0;background:#0e1117;color:white;font-family:sans-serif;}}</style>
                {auto_refresh_script}
            </head>
            <body>{page_content}</body>
        </html>
        """
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
    
    def start(self, port=8080,open_browser=False):
        print(f"Engine Online. Access at http://localhost:{port}")
        server = HTTPServer(("localhost", port), ShadowEngine)
        server.app_instance = self 
        if open_browser:
            threading.Timer(1, lambda: webbrowser.open(f"http://localhost:{port}")).start()
        server.serve_forever()

class Component:
    """Base class with a helper to merge style dictionaries."""
    def __init__(self, style=None):
        self.base_style = {}
        self.user_style = style or {}

    def get_style(self):
        # Merges defaults with user overrides into a CSS string
        final_style = {**self.base_style, **self.user_style}
        return "; ".join([f"{k.replace('_', '-')}: {v}" for k, v in final_style.items()])

class Text(Component):
    def __init__(self, content, bold=False, style=None):
        super().__init__(style)
        self.content = content
        self.base_style = {
            "color": "#ffffff",
            "font-size": "16px",
            "font-family": "'Inter', sans-serif",
            "font-weight": "700" if bold else "400",
            "margin": "10px 0",
            "line-height": "1.6"
        }

    def render(self):
        return f'<div style="{self.get_style()}">{self.content}</div>'

class Card(Component):
    def __init__(self, items, style=None):
        super().__init__(style)
        self.items = items
        self.base_style = {
            "background": "#161616",
            "padding": "30px",
            "border-radius": "20px",
            "border": "1px solid #2a2a2a",
            "box-shadow": "0 10px 30px rgba(0,0,0,0.3)",
            "flex": "1"
        }

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f'<div style="{self.get_style()}">{content}</div>'

class Image(Component):
    def __init__(self, url, circular=False, style=None):
        super().__init__(style)
        self.url = url
        self.base_style = {
            "width": "100%",
            "height": "auto",
            "border-radius": "50%" if circular else "12px",
            "display": "block",
            "object-fit": "cover"
        }

    def render(self):
        # Wrapping image in a div to allow easier positioning via style
        return f'<img src="{self.url}" style="{self.get_style()}">'

class Spacer(Component):
    def __init__(self, height="20px"):
        self.height = height
    def render(self):
        return f'<div style="height: {self.height}; width: 100%;"></div>'
    
class TextInput(Component):
    def __init__(self, label, name, placeholder="", type="text", style=None):
        super().__init__(style)
        self.label = label
        self.name = name
        self.placeholder = placeholder
        self.type = type
        self.base_style = {
            "width": "100%",
            "padding": "12px",
            "border-radius": "8px",
            "border": "1px solid #333",
            "background": "#000",
            "color": "#fff",
            "margin-bottom": "15px",
            "box-sizing": "border-box"
        }

    def render(self):
        return f"""
        <div style="margin-bottom: 15px;">
            <label style="color:#888; font-size:12px; display:block; margin-bottom:5px;">{self.label}</label>
            <input type="{self.type}" name="{self.name}" placeholder="{self.placeholder}" style="{self.get_style()}">
        </div>
        """

class Button(Component):
    def __init__(self, text, style=None):
        super().__init__(style)
        self.text = text
        self.base_style = {
            "background": "#ffffff",
            "color": "#000000",
            "padding": "12px 24px",
            "border": "none",
            "border-radius": "8px",
            "font-weight": "bold",
            "cursor": "pointer",
            "width": "100%"
        }

    def render(self):
        return f'<button type="submit" style="{self.get_style()}">{self.text}</button>'    

class Container(Component):
    def __init__(self, items, style=None):
        super().__init__(style)
        self.items = items
        self.base_style = {
            "max-width": "1100px",
            "margin": "0 auto",
            "padding": "40px 20px",
            "box-sizing": "border-box"
        }

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f'<div style="{self.get_style()}">{content}</div>'

class Row(Component):
    def __init__(self, items, style=None):
        super().__init__(style)
        self.items = items
        self.base_style = {
            "display": "flex",
            "flex-wrap": "wrap",
            "gap": "20px",
            "justify-content": "center",
            "align-items": "stretch",
            "width": "100%"
        }

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f'<div style="{self.get_style()}">{content}</div>'

class Form(Component):
    def __init__(self, action_url, items, submit_text="Continue", has_files=False, style=None):
        super().__init__(style)
        self.action_url = action_url
        self.items = items
        self.submit_text = submit_text
        self.enctype = 'enctype="multipart/form-data"' if has_files else ""
        self.base_style = {
            "display": "flex",
            "flex-direction": "column",
            "width": "100%",
            "max-width": "400px",
            "margin": "0 auto"
        }

    def render(self):
        # We reuse the Button component for the submit action
        content = "".join([i.render() for i in self.items])
        submit_btn = Button(self.submit_text).render()
        
        return f"""
        <form action="{self.action_url}" method="POST" {self.enctype} style="{self.get_style()}">
            {content}
            {submit_btn}
        </form>
        """    