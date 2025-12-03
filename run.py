import uvicorn
import os

if __name__ == "__main__":
    # Check if running in development or production
    is_dev = os.getenv("APP_ENV", "development") == "development"
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  
        port=int(os.getenv("PORT", 8000)),
        reload=is_dev,  # Only reload in development
        workers=1 if is_dev else int(os.getenv("UVICORN_WORKERS", 4))
    )
