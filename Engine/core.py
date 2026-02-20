import sqlite3, re, json, traceback, threading, webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# --- DATABASE LAYER ---
class Database:
    def __init__(self, db_name="system_data.db"):
        self.db_name = db_name
        self.lock = threading.Lock()
        self._init_db()

    def _init_db(self):
        with self.lock:
            with sqlite3.connect(self.db_name, check_same_thread=False) as conn:
                conn.execute("CREATE TABLE IF NOT EXISTS storage (key TEXT PRIMARY KEY, value TEXT, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

    def save(self, key, data):
        with self.lock:
            with sqlite3.connect(self.db_name, check_same_thread=False) as conn:
                conn.execute("INSERT OR REPLACE INTO storage (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)", (key, json.dumps(data)))

    def load(self, key, default=None):
        with self.lock:
            with sqlite3.connect(self.db_name, check_same_thread=False) as conn:
                row = conn.execute("SELECT value FROM storage WHERE key = ?", (key,)).fetchone()
                return json.loads(row[0]) if row else default

    def get_last_update(self):
        with self.lock:
            with sqlite3.connect(self.db_name, check_same_thread=False) as conn:
                res = conn.execute("SELECT MAX(updated_at) FROM storage").fetchone()
                return res[0] if res and res[0] else "0"

# --- CORE ENGINE ---
class ShadowEngine(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/__poll__':
            self.send_response(200); self.end_headers()
            self.wfile.write(str(self.server.app_instance.db.get_last_update()).encode())
            return
        self.handle_request()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        params = {k: v[0] for k, v in parse_qs(self.rfile.read(length).decode()).items()}
        func, args = self.find_route(urlparse(self.path).path)
        if func: func(self.server.app_instance, params, *args, is_post=True)
        self.send_response(303); self.send_header('Location', self.headers.get('Referer', '/')); self.end_headers()

    def handle_request(self):
        func, args = self.find_route(urlparse(self.path).path)
        params = {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}
        self.send_response(200); self.send_header("Content-type", "text/html"); self.end_headers()
        try:
            content = func(self.server.app_instance, params, *args) if func else "<h1>404</h1>"
        except:
            content = f"<pre style='color:red;'>{traceback.format_exc()}</pre>"
        self.wfile.write(self.server.app_instance._wrap(content).encode())

    def find_route(self, path):
        for pattern, func in self.server.app_instance.routes:
            match = pattern.match(path)
            if match: return func, match.groups()
        return None, []

class WebApp:
    def __init__(self, name="ShadowUI"):
        self.name = name
        self.db = Database()
        self.routes = []
    
    def store(self, k, v): self.db.save(k, v)
    def fetch(self, k, d=None): return self.db.load(k, d)
    def page(self, path):
        def d(f): self.routes.append((re.compile(f"^{path}$"), f)); return f
        return d

    def _wrap(self, content):
        return f"<html><head><style>body{{margin:0;background:#0e1117;color:#fff;font-family:sans-serif;}} *{{box-sizing:border-box;}}</style><script>let last=null;setInterval(async()=>{{let r=await fetch('/__poll__');let t=await r.text();if(last&&t!==last)location.reload();last=t;}},1500);</script></head><body>{content}</body></html>"

    def start(self, port=8080):
        srv = HTTPServer(("0.0.0.0", port), ShadowEngine)
        srv.app_instance = self
        print(f"Running on port {port}"); srv.serve_forever()

class Component:
    def __init__(self, style=None):
        # Initialize with standard dictionary or empty
        self._styles = style or {}

    def css(self):
        """Converts the internal style dict to a CSS string."""
        return "; ".join([f"{k.replace('_', '-')}:{v}" for k, v in self._styles.items()])
    def set(self, prop, val):
        """Set any CSS property dynamically."""
        self._styles[prop] = val
        return self
    # --- STYLE BUILDER METHODS ---
    # These return 'self' so you can chain them: .padding("10px").margin("5px")
    def padding(self, val): self._styles['padding'] = val; return self
    def margin(self, val): self._styles['margin'] = val; return self
    def bg(self, val): self._styles['background'] = val; return self
    def color(self, val): self._styles['color'] = val; return self
    def width(self, val): self._styles['width'] = val; return self
    def height(self, val): self._styles['height'] = val; return self
    def radius(self, val): self._styles['border-radius'] = val; return self
    def border(self, val): self._styles['border'] = val; return self
    def font_size(self, val): self._styles['font-size'] = val; return self
    def weight(self, val): self._styles['font-weight'] = val; return self
    def align(self, val): self._styles['text-align'] = val; return self
    def shadow(self, val): self._styles['box-shadow'] = val; return self
    def flex(self, val): self._styles['flex'] = val; return self
    def hide(self): self._styles['display'] = 'none'; return self
    def border_bottom(self, val): self._styles['border-bottom'] = val; return self
    def border_top(self, val): self._styles['border-top'] = val; return self
    def opacity(self, val): self._styles['opacity'] = val; return self
    def cursor(self, val): self._styles['cursor'] = val; return self
    def display(self, val): self._styles['display'] = val; return self

    
    def render(self): return ""

class Group(Component):
    def __init__(self, items):
        super().__init__()
        self.items = items
    def render(self):
        return "".join([i.render() if hasattr(i, 'render') else str(i) for i in self.items])

class Container(Component):
    def __init__(self, items):
        super().__init__()
        self.items = items
    def render(self):
        # Default container styles can still be overridden by chaining
        style = {"max-width":"1000px", "margin":"0 auto", "padding":"40px"}
        style.update(self._styles)
        self._styles = style
        return f'<div style="{self.css()}">{Group(self.items).render()}</div>'

class Card(Component):
    def __init__(self, items):
        super().__init__()
        self.items = items
    def render(self):
        style = {"background":"#1a1d23", "padding":"20px", "border-radius":"12px", "border":"1px solid #333"}
        style.update(self._styles)
        self._styles = style
        return f'<div style="{self.css()}">{Group(self.items).render()}</div>'

class Text(Component):
    def __init__(self, text):
        super().__init__()
        self.text = text
    def render(self):
        return f'<div style="{self.css()}">{self.text}</div>'

class Button(Component):
    def __init__(self, text, primary=True):
        super().__init__()
        self.text, self.p = text, primary
    def render(self):
        bg = "#6366f1" if self.p else "#333"
        base = {"background":bg, "color":"#fff", "border":"none", "padding":"10px 20px", "border-radius":"8px", "cursor":"pointer", "font-weight":"bold"}
        base.update(self._styles)
        self._styles = base
        return f'<button type="submit" style="{self.css()}">{self.text}</button>'

class Row(Component):
    def __init__(self, items, gap="20px"):
        super().__init__()
        self.items, self.gap = items, gap
    def render(self):
        base = {"display":"flex", "flex-direction":"row", "gap":self.gap, "align-items":"center"}
        base.update(self._styles)
        self._styles = base
        return f'<div style="{self.css()}">{Group(self.items).render()}</div>'
class TextInput(Component):
    def __init__(self, label, name, placeholder="", type="text", value=""):
        super().__init__()
        self.label, self.name, self.ph, self.type, self.val = label, name, placeholder, type, value

    def render(self):
        base = {"width": "100%", "padding": "12px", "background": "#000", "border": "1px solid #333", 
                "color": "#fff", "border-radius": "8px", "outline": "none", "margin-top": "5px"}
        base.update(self._styles)
        self._styles = base
        return f'''
        <div style="margin-bottom:15px; width:100%;">
            <label style="color:#888; font-size:12px; font-weight:bold;">{self.label}</label>
            <input type="{self.type}" name="{self.name}" placeholder="{self.ph}" value="{self.val}" style="{self.css()}">
        </div>'''

class Form(Component):
    def __init__(self, action, items, method="POST"):
        super().__init__()
        self.action, self.items, self.method = action, items, method
    def render(self):
        # Forms usually just need standard padding or margins
        return f'<form action="{self.action}" method="{self.method}" style="{self.css()}">{Group(self.items).render()}</form>'    

class Column(Component):
    def __init__(self, items, gap="10px"):
        super().__init__()
        self.items, self.gap = items, gap
    def render(self):
        base = {"display": "flex", "flex-direction": "column", "gap": self.gap}
        base.update(self._styles)
        self._styles = base
        return f'<div style="{self.css()}">{Group(self.items).render()}</div>'

class Grid(Component):
    def __init__(self, items, columns=3, gap="20px"):
        super().__init__()
        self.items, self.cols, self.gap = items, columns, gap
    def render(self):
        base = {"display": "grid", "grid-template-columns": f"repeat({self.cols}, 1fr)", "gap": self.gap}
        base.update(self._styles)
        self._styles = base
        return f'<div style="{self.css()}">{Group(self.items).render()}</div>'


class Navbar(Component):
    def __init__(self, brand_name, links):
        """links: list of tuples [("Home", "/"), ("Settings", "/settings")]"""
        super().__init__()
        self.brand, self.links = brand_name, links
    def render(self):
        base = {"padding": "15px 40px", "background": "#000", "border-bottom": "1px solid #333", 
                "display": "flex", "justify-content": "space-between", "align-items": "center", "position":"sticky", "top":"0"}
        base.update(self._styles)
        self._styles = base
        btns = "".join([f'<a href="{u}" style="color:#888; margin-left:20px; text-decoration:none; font-size:14px; font-weight:500;">{n}</a>' for n, u in self.links])
        return f'''
        <nav style="{self.css()}">
            <div style="font-weight:bold; font-size:20px; color:#6366f1;">{self.brand}</div>
            <div>{btns}</div>
        </nav>'''

class Image(Component):
    def __init__(self, src, alt="image"):
        super().__init__()
        self.src, self.alt = src, alt
    def render(self):
        base = {"max-width": "100%", "height": "auto", "border-radius": "8px"}
        base.update(self._styles)
        self._styles = base
        return f'<img src="{self.src}" alt="{self.alt}" style="{self.css()}">'


class Badge(Component):
    def __init__(self, text, color="#6366f1"):
        super().__init__()
        self.text, self.color = text, color
    def render(self):
        base = {"background": f"{self.color}22", "color": self.color, "padding": "4px 10px", 
                "border-radius": "6px", "font-size": "11px", "font-weight": "bold", "display": "inline-block"}
        base.update(self._styles)
        self._styles = base
        return f'<span style="{self.css()}">{self.text}</span>'

class Spacer(Component):
    def __init__(self, h="20px", w="20px"):
        super().__init__()
        self.h, self.w = h, w
    def render(self):
        return f'<div style="height:{self.h}; width:{self.w};"></div>'



























