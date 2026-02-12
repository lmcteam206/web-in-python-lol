# Termux Setup: 
# pkg update && pkg upgrade
# pkg install python
# pip install fastapi uvicorn

import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="ShadowEngine Pro Core")

# --- DATA MODELS ---
class RenderRequest(BaseModel):
    license_key: str
    comp_type: str
    props: Optional[dict] = {}

# --- DYNAMIC DATABASE HELPER ---
def load_valid_keys():
    """Loads keys from keys.json or creates a default if missing."""
    try:
        with open("keys.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Default keys if no file exists
        return {
            "DEV-123": {"owner": "User", "status": "active"},
            "GOLD-777": {"owner": "Pro Client", "status": "active"}
        }

# --- THE RENDER ENGINE ---
@app.post("/request_pro_render")
async def serve_pro(request: RenderRequest):
    # 1. Refresh & Validate License
    valid_keys = load_valid_keys()
    user = valid_keys.get(request.license_key)
    
    if not user or user["status"] != "active":
        raise HTTPException(status_code=403, detail="Invalid or Expired License Key")

    # 2. PRO NAVIGATION COMPONENT
    if request.comp_type == "ProNav":
        brand = request.props.get("brand", "SHADOW_OS")
        html = f"""
        <nav style="display: flex; justify-content: space-between; align-items: center; 
                    padding: 0 50px; height: 80px; background: rgba(10, 10, 10, 0.8); 
                    backdrop-filter: blur(15px); border-bottom: 2px solid #00ffcc;
                    box-shadow: 0 4px 20px rgba(0, 255, 204, 0.2); font-family: 'Segoe UI', sans-serif;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="width: 12px; height: 12px; background: #00ffcc; border-radius: 50%; box-shadow: 0 0 10px #00ffcc;"></div>
                <span style="font-size: 22px; font-weight: 900; color: #fff; letter-spacing: 3px;">{brand}</span>
            </div>
            <div style="display: flex; gap: 30px;">
                <span style="color: #00ffcc; font-size: 11px; font-weight: bold; border: 1px solid #00ffcc; padding: 5px 10px; border-radius: 4px;">
                    PRO_ACTIVE: {request.license_key[:7]}
                </span>
            </div>
        </nav>
        """
        return {"html": html}

    # 3. GLASS CARD COMPONENT
    if request.comp_type == "GlassCard":
        title = request.props.get("title", "Metric")
        html = f"""
        <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); 
                    padding: 30px; border-radius: 20px; backdrop-filter: blur(15px); font-family: sans-serif;">
            <h3 style="color: #888; margin: 0; font-size: 12px; text-transform: uppercase;">{title}</h3>
            <div style="font-size: 32px; color: #fff; font-weight: bold; margin-top: 10px;">Premium Content</div>
        </div>
        """
        return {"html": html}

    # 4. PREMIUM ANALYTICS COMPONENT
    if request.comp_type == "PremiumAnalytics":
        value = request.props.get("value", "0")
        html = f"""
        <div style="background: linear-gradient(135deg, #00ffcc 0%, #0088ff 100%); 
                    padding: 25px; border-radius: 15px; text-align: center; color: #000;
                    box-shadow: 0 10px 20px rgba(0,255,204,0.3); min-width: 150px; font-family: sans-serif;">
            <div style="font-size: 10px; font-weight: bold; text-transform: uppercase; opacity: 0.8;">Live Members</div>
            <div style="font-size: 42px; font-weight: 900;">{value}</div>
        </div>
        """
        return {"html": html}

    raise HTTPException(status_code=404, detail="Component logic not found on server")

if __name__ == "__main__":
    import uvicorn
    # host="0.0.0.0" allows other devices on your Wi-Fi to connect
    uvicorn.run(app, host="0.0.0.0", port=5000)