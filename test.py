from Engine.core import * # Ensure your engine code is in core.py

app = WebApp("shadow_os.json")

# --- INITIALIZE MULTI-FEATURE DATA ---
if "tasks" not in app.data:
    app.data = {
        "tasks": ["do homework",],
        "Schedule": {"school":"6am",},
        "logs": ["System Initialized..."],
        "user": {"name": "Commander", "level": 10}
    }
    app.app_logic.save(app.data)

# UI Constants
BLUE = "#00d1ff"
DARK = "#161616"

# --- HELPER: TAB NAVIGATION ---
def render_nav(active_tab):
    tabs = ["Dashboard", "Schedule", "tasks", "Settings"]
    nav_buttons = []
    for tab in tabs:
        is_active = tab.lower() == active_tab.lower()
        style = {"flex": "1", "padding": "10px", "text-align": "center", 
                 "border-bottom": f"3px solid {BLUE if is_active else 'transparent'}",
                 "cursor": "pointer", "color": "white" if is_active else "#666"}
        
        # We use a link for navigation
        nav_buttons.append(f'<a href="/?tab={tab.lower()}" style="text-decoration:none;{"; ".join([f"{k}:{v}" for k,v in style.items()])}">{tab}</a>')
    
    return f'<div style="display:flex; background:#000; margin-bottom:30px;">{"".join(nav_buttons)}</div>'

# --- MAIN CONTROLLER ---
@app.page("/")
def main_handler(params, is_post=True):
    current_tab = params.get("tab", "dashboard")
    content = [
        Text("",True)
    ]
    if current_tab == "Dashboard":
        content = [
            
        ]
    

    # Final Render
    return app.build_page([
        Container([
            Text("SHADOW OS v1.0", bold=True, style={"letter-spacing":"10px", "text-align":"center"}),
            Spacer("10px"),
            Text(render_nav(current_tab)), # Inject Nav
            *content
        ])
    ])

if __name__ == "__main__":
    app.start(port=8080)