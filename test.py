import random
from Engine.core import *
app = WebApp("game_state.json")

# Initialize game state in the library's storage
if "pos" not in app.data:
    app.data = {"pos": 200, "vel": 0, "score": 0, "pipe_x": 400, "pipe_h": 150, "dead": False}
    app.app_logic.save(app.data)

def check_collision():
    d = app.data
    # Check if bird hits floor or ceiling
    if d["pos"] > 400 or d["pos"] < 0: return True
    # Check if bird is inside the pipe's X range
    if 50 < d["pipe_x"] < 100:
        # Check if bird is NOT in the gap
        if d["pos"] < d["pipe_h"] or d["pos"] > d["pipe_h"] + 100:
            return True
    return False

@app.page("/")
def game_view(params, is_post=False):
    d = app.data
    
    if d["dead"]:
        return app.build_page([
            Container([
                Text("GAME OVER", size="40px", bold=True, color="#ff4b4b", align="center"),
                Text(f"Final Score: {d['score']}", align="center"),
                Text('<a href="/reset" style="color:#00ffcc;">Try Again</a>', align="center")
            ])
        ])

    # Draw the "Graphics" using CSS and DIVs via your Text component
    # The bird is a gold square, pipes are green blocks
    game_world = f"""
    <div style="position:relative; width:400px; height:400px; background:#000; overflow:hidden; border:2px solid #333; margin:auto;">
        <div style="position:absolute; left:50px; top:{d['pos']}px; width:20px; height:20px; background:gold;"></div>
        <div style="position:absolute; left:{d['pipe_x']}px; top:0; width:40px; height:{d['pipe_h']}px; background:green;"></div>
        <div style="position:absolute; left:{d['pipe_x']}px; top:{d['pipe_h']+100}px; width:40px; height:400px; background:green;"></div>
    </div>
    """

    return app.build_page([
        Container([
            Text("Python-Powered Flap", size="30px", bold=True, align="center"),
            Text(game_world),
            Row([
                Text('<a href="/action?do=jump" style="padding:15px 30px; background:#fff; color:#000; text-decoration:none; border-radius:8px; font-weight:bold;">JUMP</a>'),
                Text('<a href="/action?do=wait" style="padding:15px 30px; background:#333; color:#fff; text-decoration:none; border-radius:8px; font-weight:bold;">WAIT</a>')
            ]),
            Text(f"Score: {d['score']}", align="center", size="20px")
        ])
    ])

@app.page("/action")
def handle_action(params, is_post=False):
    d = app.data
    if d["dead"]: return ""

    # 1. Physics: Gravity
    action = params.get("do")
    if action == "jump":
        d["vel"] = -40
    else:
        d["vel"] += 10 # Gravity pull
    
    d["pos"] += d["vel"]
    
    # 2. Move Pipes
    d["pipe_x"] -= 30
    if d["pipe_x"] < -40:
        d["pipe_x"] = 400
        import random
        d["pipe_h"] = random.randint(50, 250)
        d["score"] += 1

    # 3. Collision
    if check_collision():
        d["dead"] = True

    app.app_logic.save(d)
    # Redirect back to home to see updated state
    return "<html><script>window.location.href='/'</script></html>"

@app.page("/reset")
def reset(params, is_post=False):
    app.data = {"pos": 200, "vel": 0, "score": 0, "pipe_x": 400, "pipe_h": 150, "dead": False}
    app.app_logic.save(app.data)
    return "<html><script>window.location.href='/'</script></html>"

if __name__ == "__main__":
    app.start(port=8080)