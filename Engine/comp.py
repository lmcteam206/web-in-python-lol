import requests

class Component:
    """Base class for all UI elements."""
    def render(self):
        return ""

# --- FREE COMPONENTS (Standard Logic) ---

class Text(Component):
    def __init__(self, content, size="16px", color="white", bold=False, align="left"):
        self.content = content
        self.size = size
        self.color = color
        self.weight = "bold" if bold else "normal"
        self.align = align

    def render(self):
        return f"""
        <div style="color: {self.color}; font-size: {self.size}; font-weight: {self.weight}; 
                    text-align: {self.align}; font-family: system-ui, sans-serif; 
                    margin: 10px 0; line-height: 1.5; box-sizing: border-box;">
            {self.content}
        </div>
        """

class Container(Component):
    def __init__(self, items, max_width="1200px"):
        self.items = items
        self.max_width = max_width

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f'<div style="max-width: {self.max_width}; margin: 0 auto; padding: 0 20px; box-sizing: border-box;">{content}</div>'

class Row(Component):
    def __init__(self, items, gap="15px", justify="center"):
        self.items = items
        self.gap = gap
        self.justify = justify

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f"""
        <div style="display: flex; flex-wrap: wrap; justify-content: {self.justify}; 
                    gap: {self.gap}; width: 100%; box-sizing: border-box;">
            {content}
        </div>
        """

class Card(Component):
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

class Image(Component):
    def __init__(self, url, size="100%", circular=False, border=False):
        self.url = url
        self.size = size
        self.radius = "50%" if circular else "12px"
        self.border = "2px solid #444" if border else "none"

    def render(self):
        return f"""
        <img src="{self.url}" style="width: {self.size}; aspect-ratio: 1/1; object-fit: cover; 
               border-radius: {self.radius}; border: {self.border}; display: block; margin: 0 auto;">
        """

# --- FORM COMPONENTS ---

class TextInput(Component):
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

class FileUpload(Component):
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
                    color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">
                {self.submit_text}
            </button>
        </form>
        """

# --- REMOTE CORE (PRO) LOGIC ---

class RemoteComponent:
    """Static handler for communicating with your Termux Tablet."""
    CORE_URL = "http://YOUR_TABLET_IP:5000/request_pro_render"

    @staticmethod
    def fetch(key, c_type, props=None):
        if not key: return None
        try:
            payload = {"license_key": key, "comp_type": c_type, "props": props or {}}
            response = requests.post(RemoteComponent.CORE_URL, json=payload, timeout=2)
            if response.status_code == 200:
                return response.json().get("html")
            return f""
        except Exception as e:
            return f""

class ProNav(Component):
    """
    A Premium Navigation Bar.
    Requires an active license key to fetch high-end styles from the Remote Core.
    """
    def __init__(self, license_key, brand="FAMILY_OS"):
        self.key = license_key
        self.brand = brand

    def render(self):
        # We use the fetcher to get the 'Secret' HTML from your tablet
        remote_html = RemoteComponent.fetch(
            key=self.key, 
            c_type="ProNav", 
            props={"brand": self.brand}
        )

        # SUCCESS: Return the beautiful ProNav
        if remote_html and "