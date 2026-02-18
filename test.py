from Engine.core import *

app = WebApp("landing_page.db")

# Simple Nav for a Landing Page
NAV_LINKS = [
    ("Docs", "#"), 
    ("Components", "#"), 
    ("GitHub", "https://github.com")
]

@app.page("/")
def landing_page(app, query, is_post=False):
    return app.build_page([
        Navbar("/", NAV_LINKS),
        
        # --- HERO SECTION ---
        Container([
            Spacer("60px"),
            Text("Build Web Apps in Pure Python.", size="48px", bold=True, style={"text-align": "center"}),
            Spacer("10px"),
            Text("The zero-dependency framework for hunters who hate HTML.", 
                 size="20px", color="#888", style={"text-align": "center"}),
            Spacer("40px"),
            Row([
                # Use spacer flex to center buttons
                Spacer("0px"), 
                Button("Get Started →", style={"padding": "15px 40px", "font-size": "18px"}),
                Button("View on GitHub", primary=False, style={"padding": "15px 40px", "font-size": "18px"}),
                Spacer("0px"),
            ], style={"justify-content": "center", "gap": "20px"}),
            Spacer("80px"),
        ]),

        # --- FEATURE GRID ---
        Container([
            Text("Engine Features", size="14px", bold=True, color="#6366f1", style={"text-align": "center"}),
            Spacer("10px"),
            Text("Everything you need, nothing you don't.", size="28px", bold=True, style={"text-align": "center"}),
            Spacer("40px"),
            Row([
                Card([
                    Text("⚡ Smart Persistence", bold=True),
                    Spacer("10px"),
                    Text("Automatic JSON-to-SQLite serialization. No more manual parsing.", color="#888", size="14px")
                ]),
                Card([
                    Text("🛡️ Error Boundaries", bold=True),
                    Spacer("10px"),
                    Text("Beautiful tracebacks rendered in-browser. Debug like a pro.", color="#888", size="14px")
                ]),
                Card([
                    Text("🌑 ShadowUI", bold=True),
                    Spacer("10px"),
                    Text("Pre-styled dark mode components ready for composition.", color="#888", size="14px")
                ])
            ]),
            Spacer("20px"),
            Row([
                Card([
                    Text("🔗 Regex Routing", bold=True),
                    Spacer("10px"),
                    Text("Dynamic URL slugs with zero configuration.", color="#888", size="14px")
                ]),
                Card([
                    Text("📦 Zero Deps", bold=True),
                    Spacer("10px"),
                    Text("Built 100% on the Python Standard Library. No bloat.", color="#888", size="14px")
                ]),
                Card([
                    # Feature placeholder
                    Text("🚀 Live Reload", bold=True),
                    Spacer("10px"),
                    Text("Automatic browser refresh when the database updates.", color="#888", size="14px")
                ])
            ])
        ]),

        # --- CODE PREVIEW SECTION ---
        Container([
            Spacer("80px"),
            Card([
                Row([
                    Text("app.py", color="#666", size="12px"),
                    Text("● ● ●", color="#444", size="12px")
                ], style={"justify-content": "space-between"}),
                Spacer("15px"),
                Text("from Engine.core import WebApp, Text", color="#4ade80"),
                Text("app = WebApp()", color="#fff"),
                Text("@app.page('/')", color="#facc15"),
                Text("def hello(app, params):", color="#fff"),
                Text("    return Text('Hello World')", color="#6366f1", style={"margin-left": "20px"}),
                Spacer("15px"),
                Text("app.start()", color="#fff"),
            ], style={"background": "#000", "font-family": "monospace", "border": "1px solid #333"}),
            Spacer("100px"),
            
            # --- FOOTER ---
            Row([
                Text("© 2024 web-in-python-lol", color="#444", size="12px"),
                Text("Built by Hunters", color="#444", size="12px")
            ], style={"justify-content": "space-between", "border-top": "1px solid #222", "padding-top": "20px"})
        ])
    ])

if __name__ == "__main__":
    app.start(port=8080)