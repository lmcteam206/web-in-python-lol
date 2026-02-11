class Component:
    """Base class for all UI elements"""
    def render(self):
        return ""
    
class Text(Component):
    def __init__(self, content, size="16px", color="white", bold=False):
        self.content = content
        self.size = size
        self.color = color
        self.bold = "bold" if bold else "normal"

    def render(self):
        return f"""
        <p style="color: {self.color}; font-size: {self.size}; 
                  font-weight: {self.bold}; font-family: sans-serif; margin: 10px 0;">
            {self.content}
        </p>
        """
class TextInput(Component):
    def __init__(self, label, name, placeholder="Enter text..."):
        self.label = label
        self.name = name
        self.placeholder = placeholder

    def render(self):
        return f"""
        <div style="margin: 15px auto; max-width: 300px; text-align: left;">
            <label style="color: #00ffcc; font-size: 12px; display: block; margin-bottom: 5px;">{self.label.upper()}</label>
            <input type="text" name="{self.name}" placeholder="{self.placeholder}" 
                   style="width: 100%; padding: 10px; background: #111; border: 1px solid #444; 
                          color: white; border-radius: 4px; outline: none; border-bottom: 2px solid #00ffcc;">
        </div>
        """
class Form(Component):
    def __init__(self, action_url, items):
        self.action_url = action_url
        self.items = items

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f"""
        <form action="{self.action_url}" method="GET" style="text-align: center;">
            {content}
            <button type="submit" style="margin-top: 10px; padding: 10px 30px; 
                    background: #00ffcc; color: black; border: none; 
                    font-weight: bold; border-radius: 4px; cursor: pointer;">
                SUBMIT DATA
            </button>
        </form>
        """        
class StatCard(Component):
    def __init__(self, label, value, icon_name="fa-bolt"):
        self.label = label
        self.value = value
        self.icon_name = icon_name

    def render(self):
        return f"""
        <div style="background: #1a1a2e; padding: 20px; border-radius: 12px; 
                    border: 1px solid #00ffcc; min-width: 140px; text-align: center;">
            <i class="fas {self.icon_name}" style="color: #00ffcc; font-size: 24px; margin-bottom: 10px;"></i>
            <div style="color: #888; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">{self.label}</div>
            <div style="color: white; font-size: 28px; font-weight: bold;">{self.value}</div>
        </div>
        """

class ActionButton(Component):
    def __init__(self, text, url):
        self.text = text
        self.url = url

    def render(self):
        return f"""
        <a href="{self.url}" style="display: block; width: 200px; text-align: center; 
           background: transparent; color: #00ffcc; border: 2px solid #00ffcc; 
           padding: 15px; text-decoration: none; border-radius: 5px; font-weight: bold;
           transition: 0.3s; margin-top: 20px;">
           {self.text.upper()}
        </a>
        """
    
class Row(Component):
    def __init__(self, items):
        self.items = items

    def render(self):
        # This is the "Magic" that centers everything and puts them side-by-side
        content = "".join([i.render() for i in self.items])
        return f"""
        <div style="display: flex; flex-wrap: wrap; justify-content: center; 
                    gap: 15px; padding: 20px; width: 100%; max-width: 1000px; margin: 0 auto;">
            {content}
        </div>
        """
class Row_full(Component):
    def __init__(self, items):
        self.items = items

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f"""
        <div style="display: flex; 
                    flex-wrap: wrap; 
                    justify-content: flex-start; 
                    gap: 20px; 
                    padding: 20px; 
                    width: 95%; 
                    max-width: 1400px; 
                    margin: 0 auto;">
            {content}
        </div>
        """    
class HunterImage(Component):
    def __init__(self, url, size="200px"):
        self.url = url
        self.size = size

    def render(self):
        return f"""
        <div style="text-align: center; margin: 20px;">
            <img src="{self.url}" style="width: {self.size}; border-radius: 50%; 
                 border: 4px solid #00ffcc; box-shadow: 0 0 20px #00ffcc;">
        </div>
        """        
class Table(Component):
    def __init__(self, headers, rows):
        self.headers = headers
        self.rows = rows

    def render(self):
        head_html = "".join([f"<th style='padding: 12px; border-bottom: 2px solid #444; text-align: left;'>{h}</th>" for h in self.headers])
        body_html = ""
        for row in self.rows:
            cells = "".join([f"<td style='padding: 10px; border-bottom: 1px solid #333;'>{c}</td>" for c in row])
            body_html += f"<tr>{cells}</tr>"
            
        return f"""
        <table style="width: 100%; border-collapse: collapse; background: #1a1a2e; color: white; margin: 20px 0; font-family: sans-serif;">
            <thead><tr style="color: #00ffcc;">{head_html}</tr></thead>
            <tbody>{body_html}</tbody>
        </table>
        """
class Select(Component):
    def __init__(self, label, name, options):
        self.label = label
        self.name = name
        self.options = options # Expects list of strings

    def render(self):
        opt_html = "".join([f"<option value='{o}'>{o}</option>" for o in self.options])
        return f"""
        <div style="margin: 15px auto; max-width: 300px; text-align: left;">
            <label style="color: #888; font-size: 12px; display: block; margin-bottom: 5px;">{self.label}</label>
            <select name="{self.name}" style="width: 100%; padding: 10px; background: #111; color: white; border: 1px solid #444; border-radius: 4px;">
                {opt_html}
            </select>
        </div>
        """    
class ProgressBar(Component):
    def __init__(self, label, current, total, color="#00ffcc"):
        self.label = label
        self.current = current
        self.total = total
        self.color = color

    def render(self):
        # Calculate percentage (prevent division by zero)
        percent = (self.current / self.total) * 100 if self.total > 0 else 0
        
        return f"""
        <div style="width: 100%; max-width: 400px; margin: 20px auto; font-family: sans-serif;">
            <div style="display: flex; justify-content: space-between; color: white; font-size: 12px; margin-bottom: 5px;">
                <span>{self.label.upper()}</span>
                <span>{self.current} / {self.total} XP</span>
            </div>
            <div style="width: 100%; height: 10px; background: #333; border-radius: 5px; overflow: hidden; border: 1px solid #444;">
                <div style="width: {percent}%; height: 100%; background: {self.color}; 
                            box-shadow: 0 0 10px {self.color}; transition: width 0.5s ease-in-out;">
                </div>
            </div>
        </div>
        """    
    
class SystemLog(Component):
    def __init__(self, messages):
        self.messages = messages # This should be a list of strings

    def render(self):
        # Create a list of messages formatted with 'System' prefixes
        formatted_msgs = "".join([f"<div style='margin-bottom: 5px; color: #00ffcc;'>[SYSTEM]: <span style='color: white;'>{msg}</span></div>" for msg in self.messages])
        
        return f"""
        <div style="background: rgba(0, 0, 0, 0.8); border: 1px solid #444; 
                    padding: 15px; border-radius: 8px; font-family: 'Courier New', monospace; 
                    font-size: 13px; max-width: 500px; margin: 20px auto; 
                    height: 150px; overflow-y: auto; text-align: left;">
            {formatted_msgs}
        </div>
        """
class Card(Component):
    def __init__(self, title, content_items):
        self.title = title
        self.content_items = content_items

    def render(self):
        inner_content = "".join([item.render() for item in self.content_items])
        return f"""
        <div style="background: #ffffff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 20px; margin: 15px; color: #333; text-align: left;">
            <h2 style="margin-top: 0; border-bottom: 1px solid #eee; padding-bottom: 10px;">{self.title}</h2>
            {inner_content}
        </div>
        """
class Alert(Component):
    def __init__(self, message, type="success"):
        # types: success (green), error (red), info (blue)
        self.message = message
        self.colors = {"success": "#00ffcc", "error": "#ff4b4b", "info": "#00a8ff"}
        self.color = self.colors.get(type, "#00ffcc")

    def render(self):
        return f"""
        <div style="padding: 15px; background: rgba(0,0,0,0.3); border-left: 5px solid {self.color}; 
                    color: white; margin: 20px auto; max-width: 800px; font-family: sans-serif;">
            <strong style="color: {self.color}; text-transform: uppercase;">{self.message}</strong>
        </div>
        """    
class YouTubeVideo(Component):
    def __init__(self, url, title="Video"):
        self.url = url
        self.title = title

    def render(self):
        # Extract ID from a standard URL or a 'short' URL
        video_id = self.url.split("v=")[-1] if "v=" in self.url else self.url.split("/")[-1]
        
        return f"""
        <div style="background: #111; padding: 10px; border-radius: 12px; width: 320px; margin: 10px; border: 1px solid #333;">
            <iframe width="100%" height="180" 
                src="https://www.youtube.com/embed/{video_id}" 
                frameborder="0" allowfullscreen style="border-radius: 8px;">
            </iframe>
            <p style="color: white; font-family: sans-serif; font-size: 14px; margin-top: 10px;">{self.title}</p>
        </div>
        """    
class Container(Component):
    def __init__(self, items):
        self.items = items

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f"""
        <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px;">
            {content}
        </div>
        """    
class ProductCard(Component):
    def __init__(self, id, name, price, img_url):
        self.id = id
        self.name = name
        self.price = price
        self.img_url = img_url

    def render(self):
        return f"""
        <div style="background: white; color: #111; padding: 15px; border-radius: 8px; 
                    width: 220px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: left;">
            <img src="{self.img_url}" style="width: 100%; height: 180px; object-fit: contain;">
            <h3 style="font-size: 16px; margin: 10px 0;">{self.name}</h3>
            <div style="color: #B12704; font-size: 18px; font-weight: bold;">${self.price}</div>
            <a href="/add_to_cart?id={self.id}" style="display: block; background: #FFD814; 
               text-align: center; padding: 8px; border-radius: 20px; 
               text-decoration: none; color: black; margin-top: 10px; font-size: 13px;">
               Add to Cart
            </a>
        </div>
        """        

class Header(Component):
    def __init__(self, title="SYSTEM", links=None):
        self.title = title
        self.links = links if links else {"Home": "/", "Shop": "/", "Cart": "/cart"}

    def render(self):
        # Create navigation links
        nav_html = "".join([
            f'<a href="{url}" style="color: white; text-decoration: none; margin: 0 15px; font-size: 14px;">{name}</a>' 
            for name, url in self.links.items()
        ])
        
        return f"""
        <nav style="background: #131921; padding: 10px 50px; display: flex; 
                    align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 1000;">
            <div style="color: #FF9900; font-size: 24px; font-weight: bold; font-family: sans-serif;">
                {self.title}<span style="color: white;">.py</span>
            </div>
            <div style="flex-grow: 1; margin: 0 30px;">
                <input type="text" placeholder="Search products..." 
                       style="width: 100%; padding: 8px; border-radius: 4px; border: none; outline: none;">
            </div>
            <div>
                {nav_html}
            </div>
        </nav>
        """

class Footer(Component):
    def __init__(self, company="Amazon.py"):
        self.company = company

    def render(self):
        return f"""
        <footer style="background: #232f3e; 
                        color: #ddd; 
                        padding: 40px 0; 
                        text-align: center; 
                        font-family: sans-serif; 
                        width: 100%; 
                        margin-top: auto;"> <div style="display: flex; justify-content: center; gap: 50px; margin-bottom: 20px; flex-wrap: wrap;">
                <div>
                    <h4 style="color: white; margin-bottom: 10px;">Get to Know Us</h4>
                    <p style="font-size: 12px; margin: 5px 0;">Careers</p>
                    <p style="font-size: 12px; margin: 5px 0;">About System</p>
                </div>
                <div>
                    <h4 style="color: white; margin-bottom: 10px;">Hunter Support</h4>
                    <p style="font-size: 12px; margin: 5px 0;">Your Account</p>
                    <p style="font-size: 12px; margin: 5px 0;">Purchase History</p>
                </div>
            </div>
            <hr style="border: 0; border-top: 1px solid #444; width: 80%; margin: 20px auto;">
            <p style="font-size: 12px;">&copy; 2026 {self.company}. All Rights Reserved.</p>
        </footer>
        """

class FlexibleFooter(Component):
    def __init__(self, sections, company="ShadowTube.py"):
        self.sections = sections # Dictionary: {"Title": {"Link Text": "URL"}}
        self.company = company

    def render(self):
        sections_html = ""
        for title, links in self.sections.items():
            # Generate actual clickable anchor tags for each link
            links_html = "".join([
                f"""<a href="{url}" style="display: block; color: #888; text-decoration: none; 
                    font-size: 12px; margin: 8px 0; transition: 0.3s;" 
                    onmouseover="this.style.color='#00ffcc'" 
                    onmouseout="this.style.color='#888'">{label}</a>""" 
                for label, url in links.items()
            ])
            
            sections_html += f"""
                <div style="min-width: 160px; text-align: left;">
                    <h4 style="color: white; margin-bottom: 15px; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">{title}</h4>
                    {links_html}
                </div>
            """

        return f"""
        <footer style="background: #131921; color: #ddd; padding: 50px 0; margin-top: auto; width: 100%; border-top: 1px solid #333;">
            <div style="display: flex; justify-content: center; gap: 80px; flex-wrap: wrap; max-width: 1200px; margin: 0 auto; padding: 0 20px;">
                {sections_html}
            </div>
            <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #222;">
                <p style="font-size: 11px; color: #555;">&copy; 2026 {self.company} | Authorized by the System</p>
            </div>
        </footer>
        """