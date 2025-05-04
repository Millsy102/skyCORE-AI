# 📦 Module imports
from fastapi import FastAPI, Request
import uvicorn
from src.logger import log
from src.router import router

app = FastAPI()

@app.post("/xexute")
async def xexute(request: Request):
    payload = await request.json()
    route = payload.get("route", "agent")
    log(f"[WebServer] Received xexution request for route: {route}")
    # 🏁 Returning result
    return {"result": router.dispatch(route, payload)}

# Function: run_server — handles a core step in this module
def run_server():
    log("[WebServer] Starting FastAPI server on port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

# 🚀 Main entry point for script
if __name__ == "__main__":
    run_server()