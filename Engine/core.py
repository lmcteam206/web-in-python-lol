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
        # Get the Host (e.g., 'blog.lmcworld.com:8080' or 'localhost:8080')
        host = self.headers.get('Host', '')
        subdomain = host.split('.')[0] if '.' in host else 'www'
        
        # Optional: If you are running locally (localhost), the split might catch 'localhost'
        if 'localhost' in subdomain or '127.0.0.1' in subdomain:
            subdomain = 'www'

        func, args = self.find_route(urlparse(self.path).path)
        params = {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}
        
        self.send_response(200); self.send_header("Content-type", "text/html"); self.end_headers()
        
        try:
            # Pass the detected subdomain into your page function
            content = func(self.server.app_instance, params, subdomain, *args) if func else "<h1>404</h1>"
        except Exception:
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
        return f"""
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://unpkg.com/lucide@latest"></script>
            <style>
                body {{ margin:0; background:#0e1117; color:#fff; font-family:sans-serif; overflow-x: hidden; }}
                * {{ box-sizing:border-box; }}
                
                .nav-links {{ display: flex; align-items: center; }}
                .menu-toggle {{ 
                    display: none; cursor: pointer; color: #6366f1; 
                    background: none; border: none; padding: 5px;
                }}
                /* Fix icon centering */
                .menu-toggle i {{ display: block; }}

                @media (max-width: 768px) {{
                    .nav-links {{ 
                        display: none; flex-direction: column; width: 100%; 
                        position: absolute; top: 60px; left: 0; 
                        background: #000; padding: 20px; border-bottom: 1px solid #333;
                    }}
                    .nav-links.active {{ display: flex; }}
                    .nav-links a {{ margin: 10px 0 !important; width: 100%; text-align: center; }}
                    .menu-toggle {{ display: block; }}
                }}
                div[style*="max-width:1000px"] {{ max-width: 100% !important; padding: 20px !important; }}
            </style>
            <script>
                function toggleMenu() {{
                    const nav = document.getElementById('mobile-nav');
                    nav.classList.toggle('active');
                }}
                // Initialize icons after page load
                window.onload = () => lucide.createIcons();
                
                let last=null;
                setInterval(async()=>{{
                    let r=await fetch('/__poll__');
                    let t=await r.text();
                    if(last&&t!==last)location.reload();
                    last=t;
                }},1500);
            </script>
        </head>
        <body>{content}</body>
        </html>"""

    def start(self, port=8080):
        srv = HTTPServer(("0.0.0.0", port), ShadowEngine)
        srv.app_instance = self
        print(f"Running on port {port}"); srv.serve_forever()


   
class Component:
    def __init__(self, style=None):
        self._styles = style or {}

    def css(self):
        return "; ".join([f"{k.replace('_', '-')}:{v}" for k, v in self._styles.items()])

    # --- HELPER ---
    def set_style(self, prop, val):
        self._styles[prop] = val
        return self
    def on_click(self, js_code):
        return self.set_style("onclick", js_code)

    # --- 1. LAYOUT & FLEXBOX (The most used) ---
    def display(self, v): return self.set_style('display', v)
    def flex(self, v): return self.set_style('flex', v)
    def flex_direction(self, v): return self.set_style('flex-direction', v)
    def justify_content(self, v): return self.set_style('justify-content', v)
    def align_items(self, v): return self.set_style('align-items', v)
    def gap(self, v): return self.set_style('gap', v)
    def flex_wrap(self, v): return self.set_style('flex-wrap', v)
    def flex_grow(self, v): return self.set_style('flex-grow', v)
    def order(self, v): return self.set_style('order', v)

    # --- 2. SPACING ---
    def padding(self, v): return self.set_style('padding', v)
    def p_top(self, v): return self.set_style('padding-top', v)
    def p_bottom(self, v): return self.set_style('padding-bottom', v)
    def p_left(self, v): return self.set_style('padding-left', v)
    def p_right(self, v): return self.set_style('padding-right', v)
    def margin(self, v): return self.set_style('margin', v)
    def m_top(self, v): return self.set_style('margin-top', v)
    def m_bottom(self, v): return self.set_style('margin-bottom', v)
    def m_left(self, v): return self.set_style('margin-left', v)
    def m_right(self, v): return self.set_style('margin-right', v)

    # --- 3. SIZING ---
    def width(self, v): return self.set_style('width', v)
    def min_width(self, v): return self.set_style('min-width', v)
    def max_width(self, v): return self.set_style('max-width', v)
    def height(self, v): return self.set_style('height', v)
    def min_height(self, v): return self.set_style('min-height', v)
    def max_height(self, v): return self.set_style('max-height', v)

    # --- 4. COLOR & BACKGROUND ---
    def bg(self, v): return self.set_style('background', v)
    def bg_color(self, v): return self.set_style('background-color', v)
    def bg_image(self, v): return self.set_style('background-image', v)
    def bg_size(self, v): return self.set_style('background-size', v)
    def color(self, v): return self.set_style('color', v)
    def opacity(self, v): return self.set_style('opacity', v)

    # --- 5. BORDERS & RADIUS ---
    def border(self, v): return self.set_style('border', v)
    def border_top(self, v): return self.set_style('border-top', v)
    def border_bottom(self, v): return self.set_style('border-bottom', v)
    def border_left(self, v): return self.set_style('border-left', v)
    def border_right(self, v): return self.set_style('border-right', v)
    def border_color(self, v): return self.set_style('border-color', v)
    def border_style(self, v): return self.set_style('border-style', v)
    def radius(self, v): return self.set_style('border-radius', v)
    def r_top_left(self, v): return self.set_style('border-top-left-radius', v)
    def r_top_right(self, v): return self.set_style('border-top-right-radius', v)
    def outline(self, v): return self.set_style('outline', v)

    # --- 6. TYPOGRAPHY ---
    def font_size(self, v): return self.set_style('font-size', v)
    def weight(self, v): return self.set_style('font-weight', v)
    def font_family(self, v): return self.set_style('font-family', v)
    def align(self, v): return self.set_style('text-align', v)
    def decoration(self, v): return self.set_style('text-decoration', v)
    def transform(self, v): return self.set_style('text-transform', v)
    def line_height(self, v): return self.set_style('line-height', v)
    def letter_spacing(self, v): return self.set_style('letter-spacing', v)
    def white_space(self, v): return self.set_style('white-space', v)

    # --- 7. POSITIONING ---
    def position(self, v): return self.set_style('position', v)
    def top(self, v): return self.set_style('top', v)
    def bottom(self, v): return self.set_style('bottom', v)
    def left(self, v): return self.set_style('left', v)
    def right(self, v): return self.set_style('right', v)
    def z_index(self, v): return self.set_style('z-index', v)
    def overflow(self, v): return self.set_style('overflow', v)

    # --- 8. EFFECTS & TRANSITIONS ---
    def shadow(self, v): return self.set_style('box-shadow', v)
    def transition(self, v): return self.set_style('transition', v)
    def cursor(self, v): return self.set_style('cursor', v)
    def filter(self, v): return self.set_style('filter', v)
    def blur(self, v): return self.set_style('backdrop-filter', f'blur({v})')
    def transform_effect(self, v): return self.set_style('transform', v)

    # --- 9. GRID SPECIFIC ---
    def grid_cols(self, v): return self.set_style('grid-template-columns', v)
    def grid_rows(self, v): return self.set_style('grid-template-rows', v)
    def grid_area(self, v): return self.set_style('grid-area', v)
    
    # --- 10. UTILITIES ---
    def hide(self): return self.set_style('display', 'none')
    def show(self): return self.set_style('display', 'block')
    def pointer(self): return self.set_style('cursor', 'pointer')


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
        self._content = text # Changed from self.text to avoid killing .text() method
    def render(self):
        return f'<div style="{self.css()}">{self._content}</div>'

class Button(Component):
    def __init__(self, text, primary=True):
        super().__init__()
        self.text, self.p = text, primary
        
    def render(self):
        bg = "#6366f1" if self.p else "#333"
        base = {"background":bg, "color":"#fff", "border":"none", "padding":"10px 20px", "border-radius":"8px", "cursor":"pointer", "font-weight":"bold"}
        base.update(self._styles)
        
        # --- NEW LOGIC: Separate JS Events from CSS ---
        js_events = " ".join([f'{k}="{v}"' for k, v in base.items() if k.startswith("on")])
        css_only = "; ".join([f"{k.replace('_', '-')}:{v}" for k, v in base.items() if not k.startswith("on")])
        
        return f'<button {js_events} style="{css_only}">{self.text}</button>'

class Row(Component):
    def __init__(self, items, gap="20px"):
        super().__init__()
        self.items = items
        self._internal_gap = gap

    def render(self):
        g = self._styles.get('gap', self._internal_gap)
        # Added flex-wrap: wrap
        base = {"display": "flex", "flex-direction": "row", "flex-wrap": "wrap", "gap": g, "align-items": "center"}
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
        self.items = items
        self._internal_gap = gap # Changed from self.gap

    def render(self):
        # Allow the .gap() method to override the default constructor gap
        g = self._styles.get('gap', self._internal_gap)
        base = {"display": "flex", "flex-direction": "column", "gap": g}
        base.update(self._styles)
        self._styles = base
        return f'<div style="{self.css()}">{Group(self.items).render()}</div>'
    
class Grid(Component):
    def __init__(self, items, columns=3, gap="20px", min_width="250px"):
        super().__init__()
        self.items, self.cols, self.gap, self.min_w = items, columns, gap, min_width

    def render(self):
        # Instead of fixed columns, we use repeat(auto-fit) for responsiveness
        base = {
            "display": "grid", 
            "grid-template-columns": f"repeat(auto-fit, minmax({self.min_w}, 1fr))", 
            "gap": self.gap
        }
        base.update(self._styles)
        self._styles = base
        return f'<div style="{self.css()}">{Group(self.items).render()}</div>'


class Navbar(Component):
    def __init__(self, brand_name, links):
        super().__init__()
        self.brand, self.links = brand_name, links
        
    def render(self):
        base = {
            "padding": "15px 40px", "background": "#000", "border-bottom": "1px solid #333", 
            "display": "flex", "justify-content": "space-between", "align-items": "center", 
            "position":"sticky", "top":"0", "z-index": "1000"
        }
        base.update(self._styles)
        self._styles = base
        
        btns = "".join([
            f'<a href="{u}" style="color:#888; margin-left:20px; text-decoration:none; font-size:14px; font-weight:500;">{n}</a>' 
            for n, u in self.links
        ])
        
        return f'''
        <nav style="{self.css()}">
            <div style="font-weight:bold; font-size:20px; color:#6366f1;">{self.brand}</div>
            
            <button class="menu-toggle" onclick="toggleMenu()">
                <i data-lucide="menu"></i>
            </button>
            
            <div id="mobile-nav" class="nav-links">
                {btns}
            </div>
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

class Icon(Component):
    def __init__(self, name, size=20, color="currentColor"):
        super().__init__()
        self.name, self.size, self.color = name, size, color
    def render(self):
        return f'<i data-lucide="{self.name}" style="width:{self.size}px; height:{self.size}px; color:{self.color}; {self.css()}"></i>'

























