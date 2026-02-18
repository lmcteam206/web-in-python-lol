import sqlite3
import os
import re
import mimetypes
import cgi
import traceback
import threading
import webbrowser
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class Database:
    """A 'Smart Dictionary' style database that handles JSON automatically."""
    def __init__(self, db_name="system_data.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_name, check_same_thread=False) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS storage (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save(self, key, data):
        """Save anything (list, dict, string) without worrying about JSON."""
        # Convert to JSON string automatically
        serialized_data = json.dumps(data)
        with sqlite3.connect(self.db_name, check_same_thread=False) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO storage (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)", 
                (key, serialized_data)
            )
            conn.commit()

    def load(self, key, default=None):
        """Load data and turn it back into a Python object automatically."""
        with sqlite3.connect(self.db_name, check_same_thread=False) as conn:
            cursor = conn.execute("SELECT value FROM storage WHERE key = ?", (key,))
            row = cursor.fetchone()
            if row:
                try:
                    # Convert back from JSON string to Python list/dict
                    return json.loads(row[0])
                except:
                    return row[0]
            return default

    def get_last_update(self):
        with sqlite3.connect(self.db_name, check_same_thread=False) as conn:
            cursor = conn.execute("SELECT MAX(updated_at) FROM storage")
            res = cursor.fetchone()
            return res[0] if res else "0"

class ShadowEngine(BaseHTTPRequestHandler):
    routes = [] 

    def do_GET(self):
        if self.path == '/__poll__':
            self.send_response(200)
            self.end_headers()
            last_ts = self.server.app_instance.db.get_last_update()
            self.wfile.write(bytes(str(last_ts), "utf-8"))
            return

        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}
        func, args = self.find_route(path)
        app_instance = self.server.app_instance

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if func:
            try:
                page_content = func(app_instance, query_params, *args)
            except Exception as e:
                page_content = f"<div style='color:red;'>{traceback.format_exc()}</div>"
        else:
            page_content = "<h1>404 Not Found</h1>"

        realtime_script = """
        <script>
            let lastUpdate = null;
            async function poll() {
                try {
                    // Using cache: "no-store" ensures Cloudflare doesn't cache the poll response
                    const res = await fetch(window.location.origin + '/__poll__', { cache: "no-store" });
                    if (res.ok) {
                        const ts = await res.text();
                        if (lastUpdate && ts !== lastUpdate) {
                            location.reload();
                        }
                        lastUpdate = ts;
                    }
                } catch (e) { console.log("Tunnel connection lost..."); }
            }
            setInterval(poll, 2000); 
        </script>
        """
        
        full_html = f"<!DOCTYPE html><html><head>{realtime_script}<style>body{{margin:0;background:#0e1117;color:white;font-family:sans-serif;}}</style></head><body>{page_content}</body></html>"
        self.wfile.write(bytes(full_html, "utf-8"))

    def do_POST(self):
        length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(length).decode('utf-8')
        params = {k: v[0] for k, v in parse_qs(body).items()}
        
        path = urlparse(self.path).path
        func, args = self.find_route(path)
        
        if func:
            func(self.server.app_instance, params, *args, is_post=True)
        
        self.send_response(303)
        self.send_header('Location', self.headers.get('Referer', '/'))
        self.end_headers()

    def find_route(self, path):
        for pattern, _, func in self.routes:
            match = pattern.match(path)
            if match: return func, match.groups()
        return None, []

class WebApp:
    def __init__(self, storage_file="work_tracker.db"):
        self.db = Database(storage_file)

    def store(self, key, value):
        """Easy-to-remember name for saving data."""
        self.db.save(key, value)

    def fetch(self, key, default=None):
        """Easy-to-remember name for getting data."""
        return self.db.load(key, default)

    def page(self, path):
        def wrapper(func):
            ShadowEngine.routes.append((re.compile(f"^{path}$"), path, func))
            return func
        return wrapper

    def build_page(self, components):
        return "".join([c.render() for c in components])

    def start(self, port=8080, open_browser=False):
        # Change "localhost" to "0.0.0.0" to allow external tunnel traffic
        server = HTTPServer(("0.0.0.0", port), ShadowEngine) 
        server.app_instance = self 
        
        if open_browser: 
            threading.Timer(1, lambda: webbrowser.open(f"http://localhost:{port}")).start()
        
        print(f"ShadowEngine running on port {port} (Cloudflare Tunnel Ready)")
        server.serve_forever()

######################################################################
######################################################################        
######################################################################
####################### COMPONENTS ###################################
######################################################################
######################################################################
######################################################################

class Component:
    def __init__(self, style=None): self.user_style = style or {}
    def get_style(self): return "; ".join([f"{k}: {v}" for k, v in self.user_style.items()])

class Text(Component):
    def __init__(self, content, bold=False, size="16px", color="#fff", style=None):
        super().__init__(style)
        self.content, self.bold, self.size, self.color = content, bold, size, color
    def render(self): return f'<div style="color:{self.color}; font-size:{self.size}; font-weight:{"bold" if self.bold else "normal"}; {self.get_style()}">{self.content}</div>'

class TextInput(Component):
    def __init__(self, label, name, placeholder="", type="text", value=None):
        super().__init__()
        self.label, self.name, self.placeholder, self.type, self.value = label, name, placeholder, type, value
    def render(self):
        val_attr = f'value="{self.value}"' if self.value is not None else ""
        if self.type == "hidden":
            return f'<input type="hidden" name="{self.name}" {val_attr}>'
        return f'<div style="margin-bottom:15px;"><label style="display:block;margin-bottom:5px;font-size:12px;color:#888;">{self.label}</label><input type="{self.type}" name="{self.name}" placeholder="{self.placeholder}" {val_attr} style="width:100%;padding:10px;background:#000;border:1px solid #333;color:#fff;border-radius:5px;"></div>'

class Card(Component):
    def __init__(self, items, style=None):
        super().__init__(style)
        self.items = items
    def render(self):
        content = "".join([i.render() for i in self.items])
        return f'<div style="background:rgba(255,255,255,0.05); padding:20px; border-radius:12px; border:1px solid #333; {self.get_style()}">{content}</div>'

class Button(Component):
    def __init__(self, text, primary=True, style=None):
        super().__init__(style)
        self.text, self.primary = text, primary
    def render(self):
        bg = "#6366f1" if self.primary else "#444"
        return f'<button type="submit" style="background:{bg}; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer; font-weight:bold; {self.get_style()}">{self.text}</button>'

class Form(Component):
    def __init__(self, action, items, style=None):
        super().__init__(style)
        self.action, self.items = action, items
    def render(self):
        content = "".join([i.render() for i in self.items])
        return f'<form action="{self.action}" method="POST" style="{self.get_style()}">{content}</form>'

class Row(Component):
    def __init__(self, items, style=None):
        super().__init__(style)
        self.items = items
    def render(self):
        content = "".join([f'<div style="flex:1;">{i.render()}</div>' for i in self.items])
        return f'<div style="display:flex; gap:20px; {self.get_style()}">{content}</div>'

class Container(Component):
    def __init__(self, items, style=None):
        super().__init__(style)
        self.items = items
    def render(self):
        content = "".join([i.render() for i in self.items])
        return f'<div style="max-width:1000px; margin:0 auto; padding:40px; {self.get_style()}">{content}</div>'

class Navbar(Component):
    def __init__(self, active, links):
        super().__init__()
        self.active, self.links = active, links
    def render(self):
        btns = "".join([f'<a href="{u}" style="color:{"#fff" if self.active==u else "#666"}; text-decoration:none; font-weight:bold; font-size:14px; padding: 10px;">{n}</a>' for n, u in self.links])
        return f'<nav style="padding:20px 40px; border-bottom:1px solid #333; display:flex; justify-content:space-between; align-items:center;"><b>SHADOW<span style="color:#6366f1">UI</span></b><div style="display:flex; gap:10px;">{btns}</div></nav>'

class Spacer(Component):
    def __init__(self, size): super().__init__(); self.size = size
    def render(self): return f'<div style="height:{self.size};"></div>'