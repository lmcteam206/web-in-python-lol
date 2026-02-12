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
            comp.Text("TOTAL MEMBERS", size="11px", color="#888", bold=True),
            comp.Text(str(total_count), size="36px", bold=True, color="#00ffcc")
        ]),
        comp.Card([
            comp.Text("LATEST ADDITION", size="11px", color="#888", bold=True),
            comp.Text(last_member, size="24px", bold=True, color="#fff")
        ]),
        comp.Card([
            comp.Text("SYSTEM STATUS", size="11px", color="#888", bold=True),
            comp.Text("● ONLINE", size="24px", bold=True, color="#4bb543")
        ])
    ], justify="center", gap="30px")

    # --- 2. MEMBER GRID ---
    member_cards = []
    for m in members:
        img_src = m.get("img", "https://via.placeholder.com/150")
        member_cards.append(
            comp.Card([
                comp.Image(url=img_src, size="120px", circular=True, border=True),
                comp.Text(m["name"], size="18px", bold=True, align="center"),
                comp.Row([
                    comp.Text(f'<a href="/member/{m["name"]}" style="color:#00ffcc; font-size:11px; font-weight:bold; text-decoration:none; letter-spacing:1px;">PROFILE</a>', align="center"),
                    comp.Text(f'<a href="/?delete={m["name"]}" style="color:#ff4b4b; font-size:11px; font-weight:bold; text-decoration:none; letter-spacing:1px;">REMOVE</a>', align="center")
                ], gap="15px", justify="center")
            ])
        )

    return web.build_page([
        comp.Navbar(brand="FAMILY_OS", links={"DASHBOARD": "/", "ADD MEMBER": "/add"}),
        comp.Container([
            comp.Text("Control Center", size="32px", bold=True, color="#fff"),
            comp.Text("Manage and monitor all authorized family profiles.", size="14px", color="#666"),
            
            # Adding a spacer margin through a blank text element or CSS
            comp.Text("", size="20px"), 
            
            stats_row,
            
            comp.Text("Active Directory", size="22px", bold=True, color="#fff"),
            comp.Row(items=member_cards, gap="25px", justify="flex-start")
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
                    comp.Image(url=member_data.get("img", "https://via.placeholder.com/150"), size="220px", border=True),
                    comp.Container([
                        comp.Text("AUTHORIZED PROFILE", size="12px", color="#00ffcc", bold=True),
                        comp.Text(name, size="48px", bold=True, color="#fff"),
                        comp.Text("Role: Family Member", size="16px", color="#888"),
                        comp.Text("Status: Active Access Card", size="16px", color="#4bb543"),
                        comp.Text("Last Login: Just now", size="14px", color="#555")
                    ])
                ], justify="flex-start", gap="40px")
            ])
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
                comp.Text("Access Provisioning", size="24px", bold=True, color="#fff"),
                comp.Text("Initialize new member identity and biometric data.", size="14px", color="#888"),
                comp.Form(action_url="/add", submit_text="INITIALIZE ACCESS", has_files=True, items=[
                    comp.TextInput(label="IDENTIFIER (NAME)", name="name", placeholder="Ex: John Doe"),
                    comp.FileUpload(label="PROFILE IMAGE SOURCE", name="img")
                ])
            ])
        ])
    ])

if __name__ == "__main__":
    web.start()