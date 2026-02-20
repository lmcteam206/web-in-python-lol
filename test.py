from Engine.core import * # Assuming the code you provided is in Engine/core.py

app = WebApp(name="ShadowAnalytics")

@app.page("/")
def dashboard(instance, params):
    # 1. Sidebar Links & Mock Data
    nav_links = [("Overview", "/"), ("Analytics", "#"), ("Logs", "#"), ("Settings", "#")]
    
    # 2. Stats Header (Grid of Cards)
    stats = Grid([
        Card([
            Text("Total Users").color("#888").font_size("12px"),
            Text("12,482").font_size("28px").weight("bold").margin("5px 0"),
            Badge("↑ 12%", "#22c55e")
        ]),
        Card([
            Text("Active Sessions").color("#888").font_size("12px"),
            Text("1,043").font_size("28px").weight("bold").margin("5px 0"),
            Badge("Stable", "#6366f1")
        ]),
        Card([
            Text("Server Load").color("#888").font_size("12px"),
            Text("42%").font_size("28px").weight("bold").margin("5px 0"),
            Badge("Healthy", "#22c55e")
        ]),
        Card([
            Text("API Latency").color("#888").font_size("12px"),
            Text("84ms").font_size("28px").weight("bold").margin("5px 0"),
            Badge("Critical", "#ef4444")
        ])
    ], columns=4)

    # 3. Main Content Area (Split Grid)
    content = Grid([
        # Left Side: Project Management
        Column([
            Text("System Projects").font_size("20px").weight("bold").margin("0 0 10px 0"),
            Card([
                Row([
                    Column([
                        Text("Cloud Migration").weight("bold"),
                        Text("Infrastructure Team").color("#666").font_size("13px")
                    ]),
                    Badge("In Progress", "#f59e0b")
                ]).padding("10px 0").border_bottom("1px solid #333"),
                Row([
                    Column([
                        Text("Auth Service v2").weight("bold"),
                        Text("Security Team").color("#666").font_size("13px")
                    ]),
                    Badge("Completed", "#22c55e")
                ]).padding("10px 0")
            ])
        ]),
        
        # Right Side: Quick Actions Form
        Column([
            Text("Broadcast Message").font_size("20px").weight("bold").margin("0 0 10px 0"),
            Card([
                Form("/send-alert", [
                    TextInput("Announcement Title", "title", placeholder="System Maintenance..."),
                    TextInput("Message Body", "msg", placeholder="Describe the update..."),
                    Button("Dispatch to All Nodes").width("100%")
                ])
            ])
        ])
    ], columns=2)

    # 4. Final Layout Construction
    return Column([
        # Navbar is now at the root, so it takes 100% width
        Navbar("ShadowAnalytics", nav_links), 
        
        # Now we put the restricted-width content inside a Container
        Container([
            Spacer(h="20px"),
            Row([
                Column([
                    Text("Operational Dashboard").font_size("32px").weight("800"),
                    Text("Real-time monitoring and system dispatch center.").color("#888")
                ]),
                Button("Download PDF", primary=False).radius("20px").padding("8px 25px")
            ]).margin("0 0 30px 0").justify_content("space-between"),
            
            stats,
            Spacer(h="30px"),
            content
        ])
    ]).gap("0").render() # Set gap to 0 so Navbar touches the top

# --- BACKEND HANDLERS ---

@app.page("/send-alert")
def handle_alert(instance, params, is_post=False):
    if is_post:
        # Save alert to DB
        title = params.get("title", "No Title")
        instance.store("latest_alert", title)
        print(f"Broadcasting: {title}")
    return "Redirecting..."

if __name__ == "__main__":
    # Open browser automatically
    webbrowser.open("http://localhost:8080")
    app.start(port=8080)