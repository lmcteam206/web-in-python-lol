from Engine import core, comp
import os

# --- SAAS CONFIG ---
MY_LICENSE_KEY = "DEV-123" # This must match what's on your Tablet

web = core.WebApp()

@web.page("/")
def dashboard(params):
    # logic omitted for brevity...
    members = web.data.get("members", [])
    
    # --- PRO STATS SECTION (Fetched from Tablet) ---
    stats_row = comp.Row(items=[
        # Using your new Remote Component
        comp.ProAnalytics(MY_LICENSE_KEY, value=str(len(members))),
        comp.Card([
            comp.Text("SYSTEM STATUS", size="11px", color="#888", bold=True),
            comp.Text("● ONLINE", size="24px", bold=True, color="#4bb543")
        ])
    ], justify="center", gap="30px")

    # --- MEMBER GRID ---
    member_cards = [
        comp.Card([
            comp.Image(url=m.get("img", ""), size="120px", circular=True),
            comp.Text(m["name"], size="18px", bold=True, align="center"),
            # Pro Card version for the profile link
            comp.ProCard(MY_LICENSE_KEY, title="View Access Logs")
        ]) for m in members
    ]

    return web.build_page([
        # Pro Navbar from your tablet!
        comp.ProNav(MY_LICENSE_KEY, brand="FAMILY_OS"), 
        comp.Container([
            comp.Text("Control Center", size="32px", bold=True, color="#fff"),
            stats_row,
            comp.Row(items=member_cards, gap="25px", justify="flex-start")
        ])
    ])

# ... rest of your pages ...

if __name__ == "__main__":
    web.start()