class Component:
    """Base class for all UI elements."""
    def render(self):
        return ""


# --- BASIC TYPOGRAPHY ---

class Text(Component):
    """Renders text with flexible levels (h1, p, span)."""
    def __init__(self, content, size="16px", color="white", bold=False, align="left"):
        self.content = content
        self.size = size
        self.color = color
        self.weight = "bold" if bold else "normal"
        self.align = align

    def render(self):
        return f"""
        <div style="color: {self.color}; font-size: {self.size}; font-weight: {self.weight}; 
                    text-align: {self.align}; font-family: sans-serif; margin: 10px 0;">
            {self.content}
        </div>
        """

# --- LAYOUT CONTAINERS ---

class Container(Component):
    """Centers content and limits width."""
    def __init__(self, items, max_width="1200px"):
        self.items = items
        self.max_width = max_width

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f'<div style="max-width: {self.max_width}; margin: 0 auto; padding: 20px;">{content}</div>'

class Row(Component):
    """Flexbox row for side-by-side elements."""
    def __init__(self, items, gap="20px", justify="center"):
        self.items = items
        self.gap = gap
        self.justify = justify

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f"""
        <div style="display: flex; flex-wrap: wrap; justify-content: {self.justify}; 
                    gap: {self.gap}; width: 100%;">
            {content}
        </div>
        """

# --- FORM ELEMENTS ---
class FileUpload(Component):
    """A stylized file input field."""
    def __init__(self, label, name, accept="image/*"):
        self.label = label
        self.name = name
        self.accept = accept

    def render(self):
        return f"""
        <div style="margin: 10px; width: 100%; max-width: 300px; font-family: sans-serif;">
            <label style="display: block; font-size: 12px; margin-bottom: 5px; color: #888;">{self.label}</label>
            <input type="file" name="{self.name}" accept="{self.accept}" 
                   style="width: 100%; padding: 8px; border-radius: 4px; border: 1px dashed #555; background: #222; color: white; cursor: pointer;">
        </div>
        """
class Form(Component):
    """Generic POST form wrapper. Updated to support File Uploads."""
    def __init__(self, action_url, items, submit_text="Submit", has_files=False):
        self.action_url = action_url
        self.items = items
        self.submit_text = submit_text
        # If the form has a FileUpload component, we need this specific encoding
        self.enctype = 'enctype="multipart/form-data"' if has_files else ""

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f"""
        <form action="{self.action_url}" method="POST" {self.enctype} 
              style="display: flex; flex-direction: column; align-items: center;">
            {content}
            <button type="submit" style="margin-top: 20px; padding: 12px 30px; background: #444; 
                    color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
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
        <div style="margin: 10px; width: 100%; max-width: 300px; font-family: sans-serif;">
            <label style="display: block; font-size: 12px; margin-bottom: 5px; color: #888;">{self.label}</label>
            <input type="{self.type}" name="{self.name}" placeholder="{self.placeholder}" 
                   style="width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #444; background: #222; color: white;">
        </div>
        """

# --- MEDIA & VISUALS ---

class Image(Component):
    """Versatile image component."""
    def __init__(self, url, size="100%", circular=False, border=False):
        self.url = url
        self.size = size
        self.radius = "50%" if circular else "8px"
        self.border = "2px solid #555" if border else "none"

    def render(self):
        return f"""
        <img src="{self.url}" style="width: {self.size}; height: {self.size}; object-fit: cover; 
             border-radius: {self.radius}; border: {self.border};">
        """

class Card(Component):
    """A standard UI Card to hold content."""
    def __init__(self, items, bg="#1a1a1a", shadow=True):
        self.items = items
        self.bg = bg
        self.shadow = "0 4px 10px rgba(0,0,0,0.5)" if shadow else "none"

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f"""
        <div style="background: {self.bg}; padding: 20px; border-radius: 12px; 
                    box-shadow: {self.shadow}; margin: 10px;">
            {content}
        </div>
        """

# --- NAVIGATION ---

class Navbar(Component):
    """Top navigation bar."""
    def __init__(self, brand, links):
        self.brand = brand
        self.links = links # dict {"Name": "/url"}

    def render(self):
        link_html = "".join([f'<a href="{v}" style="color: white; margin: 0 15px; text-decoration: none;">{k}</a>' for k, v in self.links.items()])
        return f"""
        <nav style="display: flex; justify-content: space-between; align-items: center; 
                    padding: 15px 50px; background: #000; border-bottom: 1px solid #333;">
            <div style="font-size: 20px; font-weight: bold;">{self.brand}</div>
            <div>{link_html}</div>
        </nav>
        """