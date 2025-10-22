from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class BrandPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
        self.scaler = StandardScaler()
        
    def prepare_features(self, data):
        features = pd.DataFrame({
            'day_of_week': data['timestamp'].dt.dayofweek,
            'hour': data['timestamp'].dt.hour,
            'engagement_rate': data['engagement_rate'],
            'sentiment_score': data['sentiment_score'],
            'post_length': data['content'].str.len(),
            'has_media': data['has_media'].astype(int)
        })
        
        return self.scaler.fit_transform(features)
    
    def train(self, historical_data):
        X = self.prepare_features(historical_data)
        y = historical_data['reach']
        
        self.model.fit(X, y)
    
    def predict_optimal_time(self, user_data):
        next_week = pd.date_range(
            start=datetime.now(),
            periods=7*24,
            freq='H'
        )
        
        test_data = pd.DataFrame({
            'timestamp': next_week,
            'engagement_rate': [user_data['avg_engagement']] * len(next_week),
            'sentiment_score': [user_data['avg_sentiment']] * len(next_week),
            'content': [''] * len(next_week),
            'has_media': [True] * len(next_week)
        })
        
        X_pred = self.prepare_features(test_data)
        predictions = self.model.predict(X_pred)
        
        best_time_idx = np.argmax(predictions)
        return next_week[best_time_idx]
