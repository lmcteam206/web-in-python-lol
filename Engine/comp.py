class Component:
    """Base class for all UI elements in the framework. 
    All specialized components must inherit from this class.
    """
    def render(self):
        """Generates the HTML string representation of the component."""
        return ""
    
class Text(Component):
    """
    Renders a simple paragraph of text with customizable typography.
    
    Args:
        content (str): The text message to display.
        size (str): CSS font size (e.g., '18px').
        color (str): CSS color value (e.g., '#ffffff').
        bold (bool): If True, renders the text with bold weight.
    """
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
    """
    Renders a stylized, dark-themed text input field with a glowing accent.
    
    Args:
        label (str): The descriptive text shown above the input.
        name (str): The key used when submitting form data.
        placeholder (str): The hint text shown inside the empty field.
    """
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
    """
    A container that wraps input components and submits their values to a URL.
    
    Args:
        action_url (str): The endpoint to which the form data is sent.
        items (list[Component]): A list of input-based components to render inside.
    """
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
    """
    Displays a numerical value with an icon inside a stylized card.
    
    Args:
        label (str): The name of the statistic (e.g., 'STRENGTH').
        value (str/int): The numerical or text value to highlight.
        icon_name (str): FontAwesome class name (e.g., 'fa-bolt').
    """
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
    """
    A large, bordered navigation button with hover-ready styling.
    
    Args:
        text (str): The button label.
        url (str): The destination path or link.
    """
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
    """
    A horizontal layout container that wraps items and centers them.
    
    Args:
        items (list[Component]): Components to be displayed side-by-side.
    """
    def __init__(self, items):
        self.items = items

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f"""
        <div style="display: flex; flex-wrap: wrap; justify-content: center; 
                    gap: 15px; padding: 20px; width: 100%; max-width: 1000px; margin: 0 auto;">
            {content}
        </div>
        """

class Row_full(Component):
    """
    A wide-format grid layout that starts items from the left. 
    Optimized for media galleries.
    
    Args:
        items (list[Component]): Components to be displayed in the grid.
    """
    def __init__(self, items):
        self.items = items

    def render(self):
        content = "".join([i.render() for i in self.items])
        return f"""
        <div style="display: flex; flex-wrap: wrap; justify-content: flex-start; 
                    gap: 20px; padding: 20px; width: 95%; max-width: 1400px; margin: 0 auto;">
            {content}
        </div>
        """    

class HunterImage(Component):
    """
    Displays a circular profile image with a glowing border.
    
    Args:
        url (str): The source path or URL of the image.
        size (str): Diameter of the circular image (e.g., '150px').
    """
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
    """
    Renders data in a structured, dark-themed grid table.
    
    Args:
        headers (list[str]): List of column names.
        rows (list[list[str]]): List of row data, where each row is a list of strings.
    """
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
    """
    Renders a stylized dropdown selection menu.
    
    Args:
        label (str): The label text above the dropdown.
        name (str): The key used for form submission.
        options (list[str]): The list of selectable values.
    """
    def __init__(self, label, name, options):
        self.label = label
        self.name = name
        self.options = options

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
    """
    Renders a visual progress bar with XP-style labels.
    
    Args:
        label (str): Name of the progress track.
        current (int): Current numerical progress.
        total (int): Maximum possible value.
        color (str): CSS color of the filling bar.
    """
    def __init__(self, label, current, total, color="#00ffcc"):
        self.label = label
        self.current = current
        self.total = total
        self.color = color

    def render(self):
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
    """
    Renders a scrollable console-style log for displaying system messages.
    
    Args:
        messages (list[str]): List of strings to display as log entries.
    """
    def __init__(self, messages):
        self.messages = messages

    def render(self):
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
    """
    A light-themed content container with a soft shadow and internal padding.
    
    Args:
        title (str): Header text for the card.
        content_items (list[Component]): Components to render inside the card body.
    """
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
    """
    Displays a prominent notification banner with a color-coded status.
    
    Args:
        message (str): The alert text.
        type (str): The status type ('success', 'error', or 'info').
    """
    def __init__(self, message, type="success"):
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
    """
    Embeds a YouTube video using an iframe. Automatically extracts ID from URL.
    
    Args:
        url (str): The full YouTube URL or short link.
        title (str): Title text shown below the video thumbnail.
    """
    def __init__(self, url, title="Video"):
        self.url = url
        self.title = title

    def render(self):
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
    """
    A generic layout wrapper that constrains content to a max-width and centers it.
    
    Args:
        items (list[Component]): Components to be centered on the page.
    """
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
    """
    A retail-style card for displaying store items with an 'Add to Cart' action.
    
    Args:
        id (str/int): Unique identifier for the product.
        name (str): The product name.
        price (float): Price value.
        img_url (str): Path to the product image.
    """
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
    """
    Renders a sticky navigation bar with a search bar and menu links.
    
    Args:
        title (str): The primary brand title.
        links (dict): Dictionary of {'Link Name': '/url'} for the menu.
    """
    def __init__(self, title="SYSTEM", links=None):
        self.title = title
        self.links = links if links else {"Home": "/", "Shop": "/", "Cart": "/cart"}

    def render(self):
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
            <div>{nav_html}</div>
        </nav>
        """

class Footer(Component):
    """
    Renders a multi-column static footer for large-scale applications.
    
    Args:
        company (str): Brand name for the copyright notice.
    """
    def __init__(self, company="Amazon.py"):
        self.company = company

    def render(self):
        return f"""
        <footer style="background: #232f3e; color: #ddd; padding: 40px 0; text-align: center; 
                        font-family: sans-serif; width: 100%; margin-top: auto;"> 
            <div style="display: flex; justify-content: center; gap: 50px; margin-bottom: 20px; flex-wrap: wrap;">
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
    """
    A highly customizable sticky footer that accepts nested link dictionaries.
    
    Args:
        sections (dict): Dict where keys are column titles and values are dicts of {'Label': 'URL'}.
        company (str): Copyright brand name.
    """
    def __init__(self, sections, company="ShadowTube.py"):
        self.sections = sections
        self.company = company

    def render(self):
        sections_html = ""
        for title, links in self.sections.items():
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