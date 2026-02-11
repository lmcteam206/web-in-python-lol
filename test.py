from youtubesearchpython import VideosSearch
from Engine import core, comp
import os

# --- APP SETUP ---
web = core.WebApp()

# Ensure the data structure is solid on startup
if "videos" not in web.data:
    web.data["videos"] = []

@web.page("/")
def video_home():
    # Defensive check for the 'videos' key
    video_list = web.data.get("videos", [])
    video_cards = [comp.YouTubeVideo(v['url'], v['title']) for v in video_list]

    return web.build_page([
        comp.Header(title="SHADOWTUBE", links={"Home": "/", "Sync System": "/scrape"}),
        
        comp.Container([
            comp.Row([
                comp.Text("Monarch's Live Feed", size="32px", bold=True, color="#00ffcc"),
                comp.ActionButton("SCRY 10 VIDEOS", "/scrape")
            ]),
            # Display videos or a 'System Empty' message
            comp.Row_full(video_cards) if video_cards else comp.Text("Archive Empty. Initiate Sync.", color="gray")
        ]),
        
        comp.FlexibleFooter(
            sections={
                "System": {"Wiki": "/wiki", "Maps": "/maps", "Rankings": "/leaderboard"},
                "Support": {"Manual": "/docs", "Help": "/support"}
            },
            company="ShadowTube.py"
        )
    ])

@web.page("/scrape")
def scrape_action():
    try:
        # SCRAPER LOGIC: Search for real content
        search = VideosSearch('Solo Leveling Official', limit=10)
        results = search.result()['result']
        
        new_batch = [{"title": r['title'], "url": r['link']} for r in results]
        
        # Update and save
        web.data["videos"].extend(new_batch)
        web.app_logic.save(web.data)
        
        status_msg = f"Successfully synchronized {len(new_batch)} videos."
    except Exception as e:
        status_msg = f"Sync Failed: {str(e)}"

    return web.build_page([
        comp.Header(title="SHADOWTUBE"),
        comp.Container([
            comp.Alert(status_msg, type="success" if "Successfully" in status_msg else "error"),
            comp.ActionButton("Back to Feed", "/")
        ]),
        comp.Footer()
    ])

if __name__ == "__main__":
    # For local testing. Change to host="0.0.0.0" for cloud deployment.
    web.start()