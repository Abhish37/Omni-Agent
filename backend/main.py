from fastapi import FastAPI, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.core.config import settings
from backend.db import database, models
import time

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Enable CORS so the frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to Omni-Agent API"}

@app.get("/health")
def health_check(db: Session = Depends(database.get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Mock processing delay
    time.sleep(1.5)
    return {
        "status": "success",
        "filename": file.filename,
        "message": "File uploaded and processed by Vision Agent. 1 Anomaly detected."
    }

@app.post("/ask")
async def ask_question(query: str = Form(...)):
    # Mock SQL agent response
    time.sleep(1)
    return {
        "status": "success",
        "answer": f"I analyzed the database for '{query}'. The total anomalous spending is $4,230.12 across 3 vendors."
    }
