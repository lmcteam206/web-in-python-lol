class Component:
    """Base class for all UI elements."""
    def render(self):
        return ""

class Text(Component):
    """Renders text with flexible levels (h1, p, span)."""
    def __init__(self, content, size="16px", color="white", bold=False, align="left"):
        self.content = content
        self.size = size
        self.color = color
        self.weight = "bold" if bold else "normal"
        self.align = align

    def render(self):
        # Added box-sizing and line-height for better readability
        return f"""
        <div style="color: {self.color}; font-size: {self.size}; font-weight: {self.weight}; 
                    text-align: {self.align}; font-family: system-ui, sans-serif; 
                    margin: 10px 0; line-height: 1.5; box-sizing: border-box;">
            {self.content}
        </div>
        """

class Container(Component):
    """Centers content and limits width."""
    def __init__(self, items, max_width="1200px"):
        self.items = items
        self.max_width = max_width

    def render(self):
        content = "".join([i.render() for i in self.items])
        # box-sizing ensures padding doesn't break the max-width
        return f'<div style="max-width: {self.max_width}; margin: 0 auto; padding: 0 20px; box-sizing: border-box;">{content}</div>'

class Row(Component):
    """Flexbox row for side-by-side elements."""
    def __init__(self, items, gap="15px", justify="center"):
        self.items = items
        self.gap = gap
        self.justify = justify

    def render(self):
        content = "".join([i.render() for i in self.items])
        # Changed width: 100% to box-sizing: border-box to prevent overflow
        return f"""
        <div style="display: flex; flex-wrap: wrap; justify-content: {self.justify}; 
                    gap: {self.gap}; width: 100%; box-sizing: border-box;">
            {content}
        </div>
        """

class FileUpload(Component):
    """A stylized file input field."""
    def __init__(self, label, name, accept="image/*"):
        self.label = label
        self.name = name
        self.accept = accept

    def render(self):
        return f"""
        <div style="margin: 10px; width: 100%; max-width: 320px; font-family: system-ui, sans-serif;">
            <label style="display: block; font-size: 13px; margin-bottom: 8px; color: #bbb;">{self.label}</label>
            <input type="file" name="{self.name}" accept="{self.accept}" 
                   style="width: 100%; padding: 10px; border-radius: 6px; border: 2px dashed #444; 
                   background: #222; color: #ccc; cursor: pointer; box-sizing: border-box;">
        </div>
        """

class Form(Component):
    """Generic POST form wrapper."""
    def __init__(self, action_url, items, submit_text="Submit", has_files=False):
        self.action_url = action_url
        self.items = items
        self.submit_text = submit_text
        self.enctype = 'enctype="multipart/form-data"' if has_files else ""

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f"""
        <form action="{self.action_url}" method="POST" {self.enctype} 
              style="display: flex; flex-direction: column; align-items: center; width: 100%;">
            {content}
            <button type="submit" style="margin-top: 25px; padding: 12px 40px; background: #3b82f6; 
                    color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;
                    transition: opacity 0.2s;" onmouseover="this.style.opacity='0.8'" onmouseout="this.style.opacity='1'">
                {self.submit_text}
            </button>
        </form>
        """

class TextInput(Component):
    """Standard text input with label."""
    def __init__(self, label, name, placeholder="", type="text"):
        self.label = label
        self.name = name
        self.placeholder = placeholder
        self.type = type

    def render(self):
        return f"""
        <div style="margin: 10px; width: 100%; max-width: 320px; font-family: system-ui, sans-serif;">
            <label style="display: block; font-size: 13px; margin-bottom: 8px; color: #bbb;">{self.label}</label>
            <input type="{self.type}" name="{self.name}" placeholder="{self.placeholder}" 
                   style="width: 100%; padding: 12px; border-radius: 6px; border: 1px solid #444; 
                   background: #1a1a1a; color: white; box-sizing: border-box; outline: none;">
        </div>
        """

class Image(Component):
    """Versatile image component."""
    def __init__(self, url, size="100%", circular=False, border=False):
        self.url = url
        self.size = size
        self.radius = "50%" if circular else "12px"
        self.border = "2px solid #444" if border else "none"

    def render(self):
        # Added aspect-ratio and display: block to prevent unwanted spacing
        return f"""
        <img src="{self.url}" style="width: {self.size}; aspect-ratio: 1/1; object-fit: cover; 
             border-radius: {self.radius}; border: {self.border}; display: block; margin: 0 auto;">
        """

class Card(Component):
    """A standard UI Card to hold content."""
    def __init__(self, items, bg="#222", shadow=True):
        self.items = items
        self.bg = bg
        self.shadow = "0 10px 25px rgba(0,0,0,0.3)" if shadow else "none"

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f"""
        <div style="background: {self.bg}; padding: 24px; border-radius: 16px; 
                    box-shadow: {self.shadow}; margin: 15px; box-sizing: border-box; 
                    border: 1px solid #333;">
            {content}
        </div>
        """

class Navbar(Component):
    """Free Navbar that upgrades to Pro if a license is provided."""
    def __init__(self, brand, links, license_key=None):
        self.brand = brand
        self.links = links
        self.license_key = license_key

    def render(self):
        if self.license_key:
            # Try to fetch the "Sexy" animated Pro Navbar from your tablet
            try:
                payload = {"license_key": self.license_key, "comp_type": "ProNav", "props": {"brand": self.brand}}
                # Replace with your actual Ngrok or Cloudflare Tunnel URL
                r = requests.post("https://your-public-link.ngrok-free.app/request_pro_render", json=payload, timeout=2)
                if r.status_code == 200:
                    return r.json().get("html")
            except:
                pass # Fallback to free version if tablet is offline
        
        # Standard Free Navbar Logic
        link_html = "".join([f'<a href="{v}" style="color: #ccc; margin-left: 20px; text-decoration: none;">{k}</a>' for k, v in self.links.items()])
        return f'<nav style="padding: 20px; background: #111; color: white; display: flex; justify-content: space-between;"><div>{self.brand}</div><div>{link_html}</div></nav>'
    
class RemoteComponent:
    # IMPORTANT: Update this URL to your Cloudflare or Ngrok link
    CORE_URL = "http://YOUR_TABLET_IP:5000/request_pro_render"

    @staticmethod
    def fetch(key, c_type, props=None):
        try:
            payload = {"license_key": key, "comp_type": c_type, "props": props or {}}
            response = requests.post(RemoteComponent.CORE_URL, json=payload, timeout=2)
            if response.status_code == 200:
                return response.json().get("html")
            return f""
        except:
            return ""

class ProNav(Component):
    """A Premium Navbar only for paying users."""
    def __init__(self, license_key, brand="My App"):
        self.key = license_key
        self.brand = brand

    def render(self):
        # Fetch the real HTML from the tablet
        html = RemoteComponent.fetch(self.key, "ProNav", {"brand": self.brand})
        # If tablet is offline or key is bad, return a simple fallback so the site doesn't crash
        return html or f"<nav style='background:#111; color:white; padding:20px;'>{self.brand}</nav>"

class ProCard(Component):
    """A Glassmorphism card from the remote server."""
    def __init__(self, license_key, title):
        self.key = license_key
        self.title = title

    def render(self):
        return RemoteComponent.fetch(self.key, "GlassCard", {"title": self.title}) or "<div>Card Error</div>"