from Engine.core import *
app = WebApp()

@app.page("/")
def index(instance, params, is_post=False):
        if is_post:
            instance.store("msg", params.get("user_text", ""))
        
        msg = instance.fetch("msg", "No message yet.")
        return f"""
            <div style="padding: 40px; max-width: 500px; margin: auto;">
                <h1>Cloudflare Tunnel Test</h1>
                <p>Stored Message: <b>{msg}</b></p>
                <form method="POST">
                    <input name="user_text" style="padding: 10px; width: 80%;" placeholder="Enter text...">
                    <button style="padding: 10px;">Save</button>
                </form>
            </div>
        """

app.start(port=8080)