from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, JSONResponse
import pickle, base64, yaml, os, logging

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)

# Hardcoded secret - SECURITY ISSUE
HARD_CODED_SECRET = "sk_live_SUPERSECRET_123"

# Load config without error handling - SECURITY ISSUE
DB_CONF = yaml.safe_load(open("config.yml"))

@app.get("/")
async def index():
    return PlainTextResponse("OK - vulnerable app")

@app.get("/crash")
async def crash():
    """Endpoint that crashes to demonstrate information leakage"""
    1 / 0  # This will cause ZeroDivisionError
    return PlainTextResponse("never")

@app.get("/deserialize")
async def deserialize(data: str = ""):
    """
    Dangerous endpoint that deserializes user input using pickle.
    This can lead to Remote Code Execution (RCE).
    """
    if not data:
        return JSONResponse({"error": "no data"}, status_code=400)
    try:
        raw = base64.b64decode(data)
        obj = pickle.loads(raw)  # DANGEROUS: Can execute arbitrary code
        return JSONResponse({"result": str(obj)})
    except Exception as e:
        # SECURITY ISSUE: Exposing detailed error messages
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/show-config")
async def show_config():
    """Endpoint that exposes configuration with secrets"""
    return JSONResponse(DB_CONF)

@app.get("/admin/users")
async def admin_users():
    """Admin endpoint without authentication"""
    return JSONResponse({"users": ["admin", "user1", "user2"]})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
