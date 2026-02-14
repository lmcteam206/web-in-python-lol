import random
from Engine.core import *
# Initialize the WebApp
app = WebApp("player_status.json")

# --- System Logic Helpers ---

def get_player_data():
    default = {
        "name": "Sung Jin-Woo",
        "level": 1,
        "exp": 0,
        "exp_to_next": 100,
        "job": "None",
        "rank": "E-Rank",
        "stats": {"STR": 10, "AGI": 10, "VIT": 10, "INT": 10, "SEN": 10},
        "points": 0,
        "daily_quest": {"pushups": 0, "situps": 0, "running": 0, "completed": False}
    }
    if not app.data:
        app.data = default
        app.app_logic.save(app.data)
    return app.data

# --- Routes ---

@app.page("/")
def dashboard(params, is_post=False):
    player = get_player_data()
    
    # Progress Bar Calculation
    progress = (player['exp'] / player['exp_to_next']) * 100

    return app.build_page([
        Container([
            Row([
                # Left Column: Profile Card
                Card([
                    Image("https://i.imgur.com/your_avatar_here.png", size="150px", circular=True),
                    Text(f"{player['name']}", size="28px", bold=True, align="center", color="#00ffcc"),
                    Text(f"Rank: {player['rank']} | Job: {player['job']}", align="center", color="#888"),
                    Text(f"Level: {player['level']}", size="20px", bold=True, align="center"),
                    # EXP Bar
                    Text(f"EXP: {player['exp']} / {player['exp_to_next']}", size="12px", color="#aaa"),
                    Text(f'<div style="width:100%; background:#333; height:8px; border-radius:4px;">'
                         f'<div style="width:{progress}%; background:#00ffcc; height:100%; border-radius:4px; box-shadow: 0 0 10px #00ffcc;"></div>'
                         f'</div>'),
                ]),
                
                # Right Column: Stats & Allocation
                Card([
                    Text("Ability Stats", size="22px", bold=True, color="#00ffcc"),
                    Text(f"Available Points: {player['points']}", color="#ff4b4b", bold=True),
                    Row([
                        Text(f"STR: {player['stats']['STR']}"),
                        Text(f"AGI: {player['stats']['AGI']}"),
                        Text(f"VIT: {player['stats']['VIT']}"),
                    ], justify="space-between"),
                    Row([
                        Text(f"INT: {player['stats']['INT']}"),
                        Text(f"SEN: {player['stats']['SEN']}"),
                        Text("") # Spacer
                    ], justify="space-between"),
                    
                    Text("<hr style='border: 1px solid #2a2a2a; margin: 20px 0;'>"),
                    
                    Form("/add_stat", [
                        TextInput("Stat Name (STR, AGI, etc.)", "stat", "e.g., STR"),
                    ], submit_text="Allocate 1 Point")
                ])
            ]),
            
            # Daily Quest Section
            Card([
                Text("Daily Quest: Preparation to Become Strong", size="22px", bold=True, color="#ffcc00"),
                Text("Status: " + ("COMPLETED" if player['daily_quest']['completed'] else "INCOMPLETE"), 
                     color=("#00ffcc" if player['daily_quest']['completed'] else "#ff4b4b")),
                
                Row([
                    Text(f"Pushups: {player['daily_quest']['pushups']}/100"),
                    Text(f"Situps: {player['daily_quest']['situps']}/100"),
                    Text(f"Running: {player['daily_quest']['running']}/10km"),
                ], justify="space-around"),
                
                Form("/train", [
                    TextInput("Exercise (pushups/situps/running)", "type"),
                    TextInput("Amount", "amount", type="number")
                ], submit_text="Register Training")
            ], bg="#1a1a2e")
        ])
    ])

@app.page("/add_stat")
def add_stat(params, is_post=False):
    if is_post:
        player = get_player_data()
        stat = params.get("stat", "").upper()
        if player['points'] > 0 and stat in player['stats']:
            player['stats'][stat] += 1
            player['points'] -= 1
            app.app_logic.save(player)
    return ""

@app.page("/train")
def train(params, is_post=False):
    if is_post:
        player = get_player_data()
        ex_type = params.get("type", "").lower()
        amount = int(params.get("amount", 0))
        
        if ex_type in player['daily_quest']:
            player['daily_quest'][ex_type] += amount
            
            # Check for completion
            dq = player['daily_quest']
            if dq['pushups'] >= 100 and dq['situps'] >= 100 and dq['running'] >= 10 and not dq['completed']:
                dq['completed'] = True
                # Reward: Level up + Points
                player['exp'] += 50
                player['points'] += 3
                
                # Level up logic
                if player['exp'] >= player['exp_to_next']:
                    player['level'] += 1
                    player['exp'] = 0
                    player['exp_to_next'] = int(player['exp_to_next'] * 1.5)
            
            app.app_logic.save(player)
    return ""

if __name__ == "__main__":
    app.start(port=8080)