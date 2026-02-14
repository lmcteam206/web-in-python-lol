from Engine import core, comp
import os

# --- CONFIG ---
# This links to your Tablet for the high-end UI styles
MY_LICENSE_KEY = "DEV-123" 

web = core.WebApp()

# Ensure we have a product database
if "products" not in web.data:
    web.data["products"] = [
        {"name": "Shadow Drone v2", "price": "$1,200", "stock": "14", "img": "https://images.unsplash.com/photo-1507582020474-9a35b7d455d9"},
        {"name": "Neural Link Pro", "price": "$2,500", "stock": "5", "img": "https://images.unsplash.com/photo-1593305841991-05c297ba4575"}
    ]
    web.app_logic.save(web.data)

@web.page("/")
def storefront(params):
    products = web.data.get("products", [])
    
    # 1. Header Section (ProNav)
    navbar = comp.ProNav(MY_LICENSE_KEY, brand="NEON_MARKET", links={
        "STOREFRONT": "/",
        "INVENTORY": "/admin",
        "SALES": "#"
    })

    # 2. Hero Section
    hero = comp.Container([
        comp.Text("Featured Technology", size="14px", color="#00ffcc", bold=True),
        comp.Text("The Future of Gear.", size="48px", bold=True),
    ])

    # 3. Product Grid
    items = []
    for p in products:
        items.append(
            comp.Card([
                comp.Image(url=p["img"], size="200px", border=False),
                comp.Text(p["name"], size="20px", bold=True),
                comp.Row([
                    comp.Text(p["price"], color="#00ffcc", bold=True),
                    comp.Text(f"QTY: {p['stock']}", color="#666", size="12px")
                ], justify="space-between"),
                # This fetches a premium "Buy" button/card style from your tablet
                comp.ProCard(MY_LICENSE_KEY, title="ADD TO CART")
            ])
        )

    return web.build_page([
        navbar,
        hero,
        comp.Container([
            comp.Row(items=items, gap="30px", justify="flex-start")
        ])
    ])

@web.page("/admin")
def admin_panel(params):
    # Handle Deletion
    if "delete" in params:
        web.data["products"] = [p for p in web.data["products"] if p['name'] != params["delete"]]
        web.app_logic.save(web.data)

    products = web.data.get("products", [])
    
    # Pro Analytics from Tablet (Showing total inventory value or count)
    stats = comp.Row([
        comp.ProAnalytics(MY_LICENSE_KEY, value=str(len(products))),
        comp.Card([
            comp.Text("REVENUE (24H)", size="11px", color="#888", bold=True),
            comp.Text("$14,200", size="24px", bold=True, color="#fff")
        ])
    ])

    admin_rows = [
        comp.Card([
            comp.Row([
                comp.Text(p["name"], bold=True),
                comp.Text(p["price"], color="#00ffcc"),
                comp.Text(f'<a href="/admin?delete={p["name"]}" style="color:red; text-decoration:none;">REMOVE</a>')
            ], justify="space-between")
        ]) for p in products
    ]

    return web.build_page([
        comp.ProNav(MY_LICENSE_KEY, brand="ADMIN_CORE"),
        comp.Container([
            comp.Text("Inventory Management", size="32px", bold=True),
            stats,
            comp.Text("Active Listings", size="18px", bold=True, color="#666"),
            comp.Container(admin_rows),
            comp.Text(f'<a href="/add_product" style="display:block; text-align:center; padding:15px; background:#fff; color:#000; border-radius:10px; font-weight:bold; text-decoration:none;">+ ADD NEW PRODUCT</a>')
        ])
    ])

@web.page("/add_product")
def add_product(params, is_post=False):
    if is_post:
        web.data["products"].append({
            "name": params.get("name", "New Item"),
            "price": f"${params.get('price', '0')}",
            "stock": params.get("stock", "0"),
            "img": params.get("img", "")
        })
        web.app_logic.save(web.data)

    return web.build_page([
        comp.ProNav(MY_LICENSE_KEY, brand="ADMIN_CORE"),
        comp.Container([
            comp.Card([
                comp.Text("List New Item", size="24px", bold=True),
                comp.Form(action_url="/add_product", has_files=True, items=[
                    comp.TextInput(label="Product Name", name="name"),
                    comp.TextInput(label="Price (Number Only)", name="price"),
                    comp.TextInput(label="Initial Stock", name="stock"),
                    comp.FileUpload(label="Product Image", name="img")
                ])
            ])
        ])
    ])

if __name__ == "__main__":
    web.start()