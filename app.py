from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json, base64, os, logging, secrets
from typing import Optional

app = FastAPI(title="Secure App", version="1.0.0")

# Configure logging securely
logging.basicConfig(
    level=logging.INFO,  # Changed from DEBUG to INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security: Use environment variables instead of hardcoded secrets
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
API_KEY = os.getenv("API_KEY", secrets.token_urlsafe(32))

# Security: HTTP Bearer token authentication
security = HTTPBearer()

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API key for admin endpoints"""
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return credentials.credentials

def load_config():
    """Load configuration safely without exposing secrets"""
    safe_config = {
        "database": {
            "host": os.getenv("DATABASE_HOST", "localhost"),
            "port": int(os.getenv("DATABASE_PORT", "5432")),
            "database_name": os.getenv("DATABASE_NAME", "myapp")
        },
        "app": {
            "name": "secure_app",
            "version": "1.0.0"
        }
    }
    return safe_config

@app.get("/")
async def index():
    return PlainTextResponse("OK - secure app")

@app.get("/health")
async def health_check():
    """Health check endpoint without sensitive information"""
    return JSONResponse({
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    })

@app.get("/safe-config")
async def show_safe_config():
    """Show only non-sensitive configuration"""
    safe_config = load_config()
    return JSONResponse(safe_config)

@app.get("/admin/config", dependencies=[Depends(verify_api_key)])
async def show_admin_config():
    """Admin-only endpoint for sensitive configuration"""
    admin_config = load_config()
    return JSONResponse(admin_config)

@app.get("/admin/users", dependencies=[Depends(verify_api_key)])
async def admin_users():
    """Admin endpoint with proper authentication"""
    users = ["admin", "user1", "user2"]
    return JSONResponse({"users": users})

@app.get("/error-handler")
async def error_handler():
    """Demonstrate proper error handling without information leakage"""
    try:
        result = 1 / 0
        return JSONResponse({"result": result})
    except ZeroDivisionError:
        # Security: Don't expose stack trace or internal details
        logger.error("Division by zero error occurred")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid operation"
        )
    except Exception as e:
        # Security: Generic error message
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred"
        )

@app.post("/safe-accept")
async def safe_accept(user_data: dict):
    """Safely accept and validate user input"""
    try:
        # Security: Validate input
        if "name" not in user_data or "amount" not in user_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields"
            )
        
        name = user_data["name"]
        amount = user_data["amount"]
        
        # Security: Sanitize and validate data
        if len(name) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Name too long"
            )
        
        if not isinstance(amount, (int, float)) or amount < 0 or amount > 10000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid amount"
            )
        
        # Security: Log without sensitive data
        logger.info(f"Processing request for user: {name}")
        
        return JSONResponse({
            "status": "success",
            "message": "Data accepted safely",
            "processed": True
        })
        
    except Exception as e:
        # Security: Don't expose internal error details
        logger.error(f"Internal error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8085)
