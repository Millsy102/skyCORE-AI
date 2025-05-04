# 📦 Module imports
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import json

app = FastAPI(title="SkyCORE AI OS", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UI_PATH = os.path.join(os.path.dirname(__file__), "..", "ui", "tauri-dist")
if os.path.isdir(UI_PATH):
    app.mount("/", StaticFiles(directory=UI_PATH, html=True), name="static")

# Backend logic routes
@app.get("/api/plugins")
# Function: get_plugins — handles a core step in this module
def get_plugins():
    # 🏁 Returning result
    return {"plugins": ["SkyGen", "AutoML", "MemoryStream", "SignalTap"]}

@app.get("/api/analytics")
# Function: get_analytics — handles a core step in this module
def get_analytics():
    # 🏁 Returning result
    return {
        "tokens_used": 43157,
        "memory_allocated": "142 MB",
        "active_sessions": 3
    }

@app.get("/api/settings")
# Function: get_settings — handles a core step in this module
def get_settings():
    # 🏁 Returning result
    return {
        "mode": "autonomous",
        "theme": "dark",
        "model": "gpt-4",
        "plugins_enabled": True
    }

@app.post("/api/settings")
async def update_settings(request: Request):
    data = await request.json()
    # 🏁 Returning result
    return {"status": "updated", "new": data}

@app.get("/api/logs")
# Function: stream_logs — handles a core step in this module
def stream_logs():
    # 🏁 Returning result
    return {"logs": ["[INFO] SkyCORE initialized", "[INFO] Plugin SkyGen loaded", "[WARN] Memory high"]}