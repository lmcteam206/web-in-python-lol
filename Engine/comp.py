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

