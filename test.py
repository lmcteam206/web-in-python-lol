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
        # Check if img exists, else use a placeholder
        img_src = m.get("img", "placeholder.png")
        member_cards.append(
            comp.Card([
                comp.Image(url=img_src, size="100px", circular=True),
                comp.Text(m["name"], bold=True, align="center"),
                comp.Text(f'<a href="/member/{m["name"]}" style="color:#00ffcc; font-size:12px; text-decoration:none;">VIEW PROFILE</a>', align="center"),
                comp.Text(f'<a href="/?delete={m["name"]}" style="color:#ff4b4b; font-size:11px; text-decoration:none;">REMOVE</a>', align="center")
            ])
        )

    return web.build_page([
        comp.Navbar(brand="FAMILY_OS", links={"Dashboard": "/", "Add New": "/add"}),
        comp.Container([
            comp.Text("System Dashboard", size="28px", bold=True),
            stats_row,
            comp.Text("Family Directory", size="20px", bold=True),
            comp.Row(items=member_cards, gap="20px", justify="flex-start")
        ])
    ])

@web.page("/member/(.+)")
def member_profile(params, name, is_post=False):
    member_data = next((m for m in web.data["members"] if m["name"] == name), None)
    
    if not member_data:
        return web.build_page([comp.Text("Member Not Found", size="40px", color="red")])

    return web.build_page([
        comp.Navbar(brand="FAMILY_OS", links={"Dashboard": "/", "Back": "/"}),
        comp.Container([
            comp.Card([
                comp.Row([
                    comp.Image(url=member_data.get("img", "placeholder.png"), size="200px", border=True),
                    comp.Container([
                        comp.Text(f"Profile: {name}", size="32px", bold=True, color="#00ffcc"),
                        comp.Text("Role: Family Member", color="#888"),
                        comp.Text("Status: Active", color="#4bb543")
                    ])
                ])
            ])
        ])
    ])

@web.page("/add")
def add_page(params, is_post=False):
    if is_post:
        # 'params' now includes the filename from the upload
        web.data["members"].append(params)
        web.app_logic.save(web.data)

    return web.build_page([
        comp.Navbar(brand="FAMILY_OS", links={"Dashboard": "/", "Add New": "/add"}),
        comp.Container([
            comp.Card([
                comp.Text("Register New Member", size="22px", bold=True),
                # Note the has_files=True here!
                comp.Form(action_url="/add", submit_text="Authorize Member", has_files=True, items=[
                    comp.TextInput(label="Full Name", name="name", placeholder="Enter name..."),
                    # New FileUpload Component replacing TextInput
                    comp.FileUpload(label="Profile Picture", name="img")
                ])
            ])
        ])
    ])
@web.page("/bug")
def bug_page(params):
    return 10 / 0  # This will trigger the Error Boundary!
if __name__ == "__main__":
    web.start()