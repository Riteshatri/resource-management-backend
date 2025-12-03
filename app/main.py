from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, users, theme, resources, admin
from app.db.database import Base, engine, init_db

app = FastAPI(
    title="Resource Management API",
    description="Python FastAPI backend with Azure SQL Database",
    version="1.0.0"
)

# CORS Configuration - Use settings for consistent configuration management
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(theme.router, prefix="/api/theme", tags=["Theme"])
app.include_router(resources.router, prefix="/api/resources", tags=["Resources"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.on_event("startup")
def startup_event():
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        init_db()  # Initialize/fix Azure SQL schema
        
        # Create super user
        from app.db.database import SessionLocal
        from app.db.super_user_seed import create_super_user
        db = SessionLocal()
        try:
            create_super_user(db)
        finally:
            db.close()
    except Exception as e:
        print(f"⚠️ Database initialization warning: {str(e)[:100]}")
        print("ℹ️ API will still start but database operations may fail")


@app.get("/")
def root():
    return {"message": "Resource Management API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
