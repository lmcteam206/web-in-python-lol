import requests

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

# --- REMOTE CORE (PRO) LOGIC ---

class RemoteComponent:
    CORE_URL = "http://192.168.1.2:5000/request_pro_render"

    @staticmethod
    def fetch(key, c_type, props=None):
        if not key: return None
        try:
            payload = {"license_key": key, "comp_type": c_type, "props": props or {}}
            response = requests.post(RemoteComponent.CORE_URL, json=payload, timeout=2)
            if response.status_code == 200:
                return response.json().get("html")
            return None
        except:
            return None

class ProNav(Component):
    def __init__(self, license_key, brand="FAMILY_OS", links=None):
        self.key = license_key
        self.brand = brand
        self.links = links or {"DASHBOARD": "/", "SETTINGS": "/settings"}

    def render(self):
        remote_html = RemoteComponent.fetch(self.key, "ProNav", {"brand": self.brand})
        if remote_html: return remote_html

        link_items = "".join([
            f'<a href="{url}" style="color: #666; text-decoration: none; font-size: 13px; margin-left: 25px; font-weight: 500;">{name}</a>' 
            for name, url in self.links.items()
        ])
        return f"""
        <nav style="display: flex; justify-content: space-between; align-items: center; padding: 0 60px; 
                    height: 85px; background: #000; border-bottom: 1px solid #1a1a1a; font-family: sans-serif;">
            <div style="color: #fff; font-weight: 800; font-size: 20px; letter-spacing: -1px;">{self.brand.upper()}</div>
            <div style="display: flex; align-items: center;">
                {link_items}
                <div style="margin-left: 25px; font-size: 9px; color: #444; border: 1px solid #222; 
                            padding: 4px 10px; border-radius: 6px; font-weight: bold;">OFFLINE_CORE</div>
            </div>
        </nav>
        """

class ProAnalytics(Component):
    def __init__(self, license_key, value):
        self.key = license_key
        self.value = value

    def render(self):
        return RemoteComponent.fetch(self.key, "PremiumAnalytics", {"value": self.value}) or \
               f"<div style='color:#555; padding: 20px; border: 1px dashed #333; border-radius: 15px; text-align: center;'>Pro Analytics Locked</div>"

class ProCard(Component):
    def __init__(self, license_key, title):
        self.key = license_key
        self.title = title

    def render(self):
        return RemoteComponent.fetch(self.key, "GlassCard", {"title": self.title}) or \
               f"<div style='color:#444; font-size: 12px;'>{self.title} (Requires Pro)</div>"