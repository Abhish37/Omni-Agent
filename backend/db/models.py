from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from backend.db.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String, unique=True, index=True)
    document_type = Column(String, index=True)  # invoice, receipt, etc.
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    vendor = Column(String, index=True)
    date = Column(DateTime, default=func.now())
    
    # Anomaly detection results
    is_anomaly = Column(Boolean, default=False)
    anomaly_score = Column(Float, nullable=True)
    
    # Raw extracted JSON from Vision Agent
    extracted_data = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
