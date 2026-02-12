# Termux: pkg install python && pip install fastapi uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI(title="ShadowEngine Pro Core")

# --- DATA MODELS ---
class RenderRequest(BaseModel):
    license_key: str
    comp_type: str
    props: Optional[dict] = {}

# --- YOUR CUSTOMER DATABASE ---
# In a real app, you'd load this from a 'keys.json' file
VALID_KEYS = {
    "DEV-123": {"owner": "User", "status": "active"},
    "GOLD-777": {"owner": "Pro Client", "status": "active"}
}

# --- THE RENDER ENGINE ---
@app.post("/request_pro_render")
async def serve_pro(request: RenderRequest):
    # 1. Validate License
    user = VALID_KEYS.get(request.license_key)
    if not user or user["status"] != "active":
        raise HTTPException(status_code=403, detail="Invalid License Key")

    # 2. Pro Component Logic (Hidden from GitHub)
    if request.comp_type == "ProNav":
        brand = request.props.get("brand", "OS")
        # Return high-end HTML with CSS animations
        html = f"""
        <nav style="display: flex; justify-content: space-between; padding: 20px 50px; 
                    background: rgba(0,0,0,0.8); backdrop-filter: blur(10px); 
                    border-bottom: 2px solid #00ffcc; box-shadow: 0 0 20px #00ffcc44;">
            <div style="font-weight: 900; color: #00ffcc; letter-spacing: 2px;">{brand.upper()} PRO</div>
            <div style="color: white; font-size: 12px;">LICENSE VERIFIED: {request.license_key}</div>
        </nav>
        """
        return {"html": html}

    if request.comp_type == "GlassCard":
        title = request.props.get("title", "Metric")
        html = f"""
        <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); 
                    padding: 30px; border-radius: 20px; backdrop-filter: blur(15px);">
            <h3 style="color: #888; margin: 0;">{title}</h3>
            <div style="font-size: 40px; color: #fff;">Premium Content</div>
        </div>
        """
        return {"html": html}

    raise HTTPException(status_code=404, detail="Component not found")

if __name__ == "__main__":
    import uvicorn
    # Start the server on port 5000
    uvicorn.run(app, host="0.0.0.0", port=5000)