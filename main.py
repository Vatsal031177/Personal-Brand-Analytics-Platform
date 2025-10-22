from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from datetime import datetime
import numpy as np
from transformers import pipeline
import tweepy
import linkedin_api
import pandas as pd

app = FastAPI(title="Personal Brand Analytics")

class SocialProfile(BaseModel):
    platform: str
    username: str
    content_type: str

class AnalyticsResult(BaseModel):
    sentiment_score: float
    engagement_rate: float
    reach: int
    growth_prediction: float

class BrandAnalyzer:
    def __init__(self):
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        
    def analyze_content(self, text):
        result = self.sentiment_analyzer(text)[0]
        return {
            'sentiment': result['label'],
            'score': result['score']
        }
    
    def calculate_engagement(self, likes, comments, followers):
        return (likes + comments * 2) / followers * 100
    
    def predict_growth(self, historical_data):
        # Simple linear regression for growth prediction
        x = np.array(range(len(historical_data)))
        y = np.array(historical_data)
        z = np.polyfit(x, y, 1)
        return float(z[0] * (len(historical_data) + 30))  # 30-day prediction

@app.post("/analyze/{platform}")
async def analyze_profile(platform: str, profile: SocialProfile):
    analyzer = BrandAnalyzer()
    
    try:
        if platform == "twitter":
            data = fetch_twitter_data(profile.username)
        elif platform == "linkedin":
            data = fetch_linkedin_data(profile.username)
        else:
            raise HTTPException(status_code=400, detail="Unsupported platform")
        
        analysis = analyzer.analyze_content(data['recent_posts'])
        engagement = analyzer.calculate_engagement(
            data['likes'],
            data['comments'],
            data['followers']
        )
        
        growth = analyzer.predict_growth(data['historical_engagement'])
        
        return AnalyticsResult(
            sentiment_score=analysis['score'],
            engagement_rate=engagement,
            reach=data['reach'],
            growth_prediction=growth
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
