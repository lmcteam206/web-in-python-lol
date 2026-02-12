from Engine import core, comp
import os

web = core.WebApp()

# Ensure base data keys exist
if "members" not in web.data:
    web.data["members"] = []
    web.app_logic.save(web.data)

@web.page("/")
def dashboard(params):
    # --- LOGIC: DELETE ---
    if "delete" in params:
        target = params["delete"]
        web.data["members"] = [m for m in web.data["members"] if m['name'] != target]
        web.app_logic.save(web.data)

    members = web.data.get("members", [])
    
    # --- 1. STATS SECTION ---
    # Calculating metrics for the dashboard header
    total_count = len(members)
    last_member = members[-1]["name"] if members else "None"
    
    stats_row = comp.Row(items=[
        comp.Card([
            comp.Text("Total Members", size="12px", color="#888"),
            comp.Text(str(total_count), size="32px", bold=True, color="#00ffcc")
        ]),
        comp.Card([
            comp.Text("Latest Addition", size="12px", color="#888"),
            comp.Text(last_member, size="24px", bold=True)
        ]),
        comp.Card([
            comp.Text("System Status", size="12px", color="#888"),
            comp.Text("ONLINE", size="24px", bold=True, color="#4bb543")
        ])
    ], justify="space-evenly")

    # --- 2. MEMBER GRID ---
    member_cards = []
    for m in members:
        member_cards.append(
            comp.Card([
                comp.Image(url=m["img"], size="100px", circular=True),
                comp.Text(m["name"], bold=True, align="center"),
                comp.Text(f'<a href="/?delete={m["name"]}" style="color:#ff4b4b; font-size:11px; text-decoration:none;">REMOVE</a>', align="center")
            ])
        )

    # --- 3. FINAL PAGE ASSEMBLY ---
    return web.build_page([
        comp.Navbar(brand="FAMILY_OS", links={"Dashboard": "/", "Add New": "/add"}),
        comp.Container([
            comp.Text("System Dashboard", size="28px", bold=True),
            stats_row,  # The high-level overview
            
            comp.Text("Family Directory", size="20px", bold=True),
            comp.Row(items=member_cards, gap="20px", justify="flex-start")
        ])
    ])
 
@web.page("/add")
def add_page(params, is_post=False):
    if is_post:
        web.data["members"].append(params)
        web.app_logic.save(web.data)

    return web.build_page([
        comp.Navbar(brand="FAMILY_OS", links={"Dashboard": "/", "Add New": "/add"}),
        comp.Container([
            comp.Card([
                comp.Text("Register New Member", size="22px", bold=True),
                comp.Form(action_url="/add", submit_text="Authorize Member", items=[
                    comp.TextInput(label="Full Name", name="name", placeholder="Enter name..."),
                    comp.TextInput(label="Image Path", name="img", placeholder="e.g. dad.jpg")
                ])
            ])
        ])
    ])

if __name__ == "__main__":
    web.start()