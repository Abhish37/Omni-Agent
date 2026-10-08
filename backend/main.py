from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend.core.config import settings
from backend.db import database, models

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.get("/")
def root():
    return {"message": "Welcome to Omni-Agent API"}

@app.get("/health")
def health_check(db: Session = Depends(database.get_db)):
    # Basic health check to ensure DB is connected
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
