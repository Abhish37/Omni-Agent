import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from typing import List, Dict

class AnomalyDetector:
    def __init__(self, contamination=0.01):
        """
        contamination: The proportion of outliers in the data set.
        """
        self.model = IsolationForest(
            n_estimators=100, 
            contamination=contamination,
            random_state=42
        )
        self.is_trained = False
        
    def _prepare_features(self, transactions: List[Dict]) -> pd.DataFrame:
        """
        Extract numeric features from raw extracted JSON.
        """
        df = pd.DataFrame(transactions)
        # In a real scenario, handle categorical encoding for 'vendor', 'currency', etc.
        # For basic numeric anomaly detection, we might just use 'amount'
        return df[['amount']].fillna(0)

    def train(self, historical_transactions: List[Dict]):
        X = self._prepare_features(historical_transactions)
        self.model.fit(X)
        self.is_trained = True

    def predict(self, transactions: List[Dict]) -> List[Dict]:
        """
        Returns list of transactions with anomaly predictions appended.
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before calling predict.")
            
        X = self._prepare_features(transactions)
        
        # Isolation forest returns -1 for outliers and 1 for inliers
        preds = self.model.predict(X)
        scores = self.model.decision_function(X)
        
        results = []
        for i, t in enumerate(transactions):
            result = t.copy()
            result['is_anomaly'] = bool(preds[i] == -1)
            result['anomaly_score'] = float(scores[i])
            results.append(result)
            
        return results

    def save(self, filepath: str):
        joblib.dump(self.model, filepath)

    def load(self, filepath: str):
        self.model = joblib.load(filepath)
        self.is_trained = True
