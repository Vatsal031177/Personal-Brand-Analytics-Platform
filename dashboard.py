import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class BrandDashboard:
    def __init__(self):
        st.set_page_config(layout="wide")
        st.title("Personal Brand Analytics Dashboard")
        
    def render_metrics(self, data):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Brand Sentiment", f"{data['sentiment_score']:.2f}")
        with col2:
            st.metric("Engagement Rate", f"{data['engagement_rate']:.2f}%")
        with col3:
            st.metric("Total Reach", f"{data['reach']:,}")
        with col4:
            st.metric("Growth Trend", f"{data['growth_prediction']:+.1f}%")
    
    def render_trends(self, historical_data):
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=historical_data['dates'],
            y=historical_data['engagement'],
            name="Engagement",
            line=dict(color="#2E86C1")
        ))
        
        fig.update_layout(
            title="Engagement Trends",
            xaxis_title="Date",
            yaxis_title="Engagement Rate (%)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_content_analysis(self, content_data):
        fig = px.treemap(
            content_data,
            path=['type', 'category'],
            values='engagement',
            color='sentiment',
            color_continuous_scale='RdYlBu'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_competitor_analysis(self, competitor_data):
        fig = px.scatter(
            competitor_data,
            x='followers',
            y='engagement_rate',
            size='posts',
            color='platform',
            hover_name='username',
            log_x=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
