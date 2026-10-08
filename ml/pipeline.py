from typing import Dict, Any
from agents.vision_agent.agent import VisionAgent
from ml.anomaly_detector.model import AnomalyDetector
from backend.db.models import Transaction
from sqlalchemy.orm import Session

class IngestionPipeline:
    def __init__(self):
        self.vision_agent = VisionAgent()
        self.anomaly_detector = AnomalyDetector()
        
        # Load pre-trained models in a real scenario
        # self.anomaly_detector.load("path_to_model.pkl")
        
        # Dummy training for now to allow predictions
        self.anomaly_detector.train([
            {"amount": 50.0},
            {"amount": 100.0},
            {"amount": 75.0}
        ])

    def process_document(self, image_path: str, db: Session) -> Transaction:
        """
        Orchestrates the ingestion, extraction, anomaly detection, and DB insertion.
        """
        # 1. Vision Triage (Extraction)
        extracted_data = self.vision_agent.extract_from_image(image_path)
        data_dict = extracted_data.model_dump()
        
        # 2. Predictive Enrichment (Anomaly Detection)
        # We pass a list containing our single transaction to predict
        enriched_data_list = self.anomaly_detector.predict([data_dict])
        enriched_data = enriched_data_list[0]
        
        # 3. Database Insertion (Idempotent check could be added here based on document_id)
        existing_tx = db.query(Transaction).filter(Transaction.document_id == enriched_data["document_id"]).first()
        
        if existing_tx:
            # Update or return existing to maintain idempotency
            return existing_tx
            
        new_transaction = Transaction(
            document_id=enriched_data["document_id"],
            document_type=enriched_data["document_type"],
            amount=enriched_data["amount"],
            currency=enriched_data["currency"],
            vendor=enriched_data["vendor"],
            # date=enriched_data["date"], # Need to parse string to datetime properly
            is_anomaly=enriched_data["is_anomaly"],
            anomaly_score=enriched_data["anomaly_score"],
            extracted_data=data_dict
        )
        
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        
        return new_transaction
