# ==================================================
# EduRisk AI - Academic Risk Intelligence Platform
# Microsoft Imagine Cup 2026 - PRODUCTION READY
# Azure Machine Learning + Azure OpenAI Integration
# ==================================================

import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import os
import plotly.graph_objects as go
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta
import uuid

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="EduRisk AI | Azure AI Powered",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SESSION STATE INIT (ADDED) ====================
# 🔧 FIX 3: Session State Management
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

# ==================== AZURE KEY VAULT FOR SECRETS ====================
def get_azure_secrets():
    """Fetch secrets from Azure Key Vault or environment variables"""
    try:
        # 🔧 FIX 1: Secure Key Vault URL via env variable
        key_vault_url = os.getenv(
            "AZURE_KEY_VAULT_URL",
            "https://edurisk-kv.vault.azure.net/"
        )

        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_url, credential=credential)

        return {
            "openai_endpoint": client.get_secret("openai-endpoint").value,
            "openai_key": client.get_secret("openai-key").value,
            "openai_deployment": client.get_secret("openai-deployment").value,
            "ml_endpoint": client.get_secret("ml-endpoint").value,
            "ml_key": client.get_secret("ml-key").value
        }

    except Exception:
        st.warning("Azure Key Vault not configured. Using environment variables.")
        return {
            "openai_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "openai_key": os.getenv("AZURE_OPENAI_KEY"),
            "openai_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            "ml_endpoint": os.getenv("AZURE_ML_ENDPOINT"),
            "ml_key": os.getenv("AZURE_ML_KEY")
        }

# ==================== AZURE MACHINE LEARNING ENDPOINT ====================
class AzureMLPredictor:
    def __init__(self, endpoint_url, api_key):
        self.endpoint_url = endpoint_url
        self.api_key = api_key

    def predict(self, features):

        # 🔧 SAFETY GUARD (existing fix)
        if not self.endpoint_url or not self.api_key:
            return self._fallback_prediction(features)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "input_data": {
                "columns": list(features.keys()),
                "index": [0],
                "data": [list(features.values())]
            }
        }

        try:
            response = requests.post(
                self.endpoint_url,
                headers=headers,
                json=data,
                timeout=10
            )

            if response.status_code == 200:
                return self._parse_response(response.json())
            else:
                return self._fallback_prediction(features)

        except Exception:
            return self._fallback_prediction(features)

    def _parse_response(self, result):
        if "output" in result:
            pred = result["output"][0]
            risk_map = {0: "High", 1: "Medium", 2: "Low"}
            return {
                "risk_level": risk_map.get(pred[0], "Medium"),
                "confidence": float(pred[1]),
                "probabilities": {
                    "High": float(pred[2]),
                    "Medium": float(pred[3]),
                    "Low": float(pred[4])
                }
            }
        return self._fallback_prediction()

    def _fallback_prediction(self, features=None):
        if features:
            score = (
                features["attendance_pct"] * 0.15 +
                features["assignment_score"] * 0.20 +
                features["quiz_score"] * 0.20 +
                features["midterm_score"] * 0.20 +
                features["study_hours_per_week"] * 0.15 +
                features["previous_gpa"] * 1.0
            )
            if score < 60:
                risk = "High"
            elif score < 75:
                risk = "Medium"
            else:
                risk = "Low"
        else:
            risk = "Medium"

        return {
            "risk_level": risk,
            "confidence": 0.85,
            "probabilities": {"High": 0.3, "Medium": 0.4, "Low": 0.3}
        }

# ==================== AZURE OPENAI SERVICE ====================
class AzureOpenAIGuide:
    def __init__(self, endpoint, api_key, deployment):
        self.endpoint = endpoint
        self.api_key = api_key
        self.deployment = deployment

    def generate_guidance(self, risk_level, weak_areas, scores):

        # 🔧 SAFETY GUARD (existing fix)
        if not self.endpoint or not self.api_key or not self.deployment:
            return self._fallback_guidance(risk_level)

        prompt = f"""As an academic advisor AI, create a personalized 7-day action plan.

RISK LEVEL: {risk_level}
WEAK AREAS: {', '.join(weak_areas) if weak_areas else 'None'}
Attendance: {scores['attendance']}%
Assignments: {scores['assignment']}%
Quizzes: {scores['quiz']}%
Midterm: {scores['midterm']}%
Study Hours: {scores['study_hours']}/week
GPA: {scores['gpa']}/10
"""

        payload = {
            "messages": [
                {"role": "system", "content": "You are an experienced academic advisor."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 800,
            "temperature": 0.7
        }

        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        try:
            response = requests.post(
                f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version=2023-12-01-preview",
                headers=headers,
                json=payload,
                timeout=15
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return self._fallback_guidance(risk_level)

        except Exception:
            return self._fallback_guidance(risk_level)

    def _fallback_guidance(self, risk_level):
        plans = {
            "High": "**🔴 URGENT 7-DAY RECOVERY PLAN**\n• Advisor meeting\n• Full attendance\n• 4+ hrs study\n• Tutoring",
            "Medium": "**🟡 IMPROVEMENT PLAN**\n• 2–3 hrs/day\n• Focus weak areas",
            "Low": "**🟢 EXCELLENCE PLAN**\n• Advanced learning\n• Projects"
        }
        return plans.get(risk_level, plans["Medium"])

# ==================== VISUALIZATION TOOLS ====================
def create_radar_chart(scores):
    categories = ['Attendance', 'Assignments', 'Quizzes', 'Midterm', 'Study Hours', 'GPA']
    values = [
        scores['attendance'],
        scores['assignment'],
        scores['quiz'],
        scores['midterm'],
        min(scores['study_hours'] * 2.5, 100),
        scores['gpa'] * 10
    ]

    fig = go.Figure(data=go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=400
    )
    return fig

def gauge_chart(value, title):
    color = "#10B981" if value >= 75 else "#F59E0B" if value >= 60 else "#EF4444"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": color}}
    ))
    fig.update_layout(height=300)
    return fig

# ==================== MAIN APPLICATION ====================
def main():

    st.markdown("<h1 style='text-align:center;'>🎓 EduRisk AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Azure AI Powered Academic Risk Intelligence</p>", unsafe_allow_html=True)

    secrets = get_azure_secrets()
    ml_predictor = AzureMLPredictor(secrets["ml_endpoint"], secrets["ml_key"])
    openai_guide = AzureOpenAIGuide(
        secrets["openai_endpoint"],
        secrets["openai_key"],
        secrets["openai_deployment"]
    )

    with st.sidebar:
        attendance = st.slider("Attendance (%)", 40, 100, 75)
        assignment = st.slider("Assignment Score", 0, 100, 70)
        quiz = st.slider("Quiz Score", 0, 100, 65)
        midterm = st.slider("Midterm Score", 0, 100, 60)
        study_hours = st.slider("Study Hours/Week", 0, 40, 12)
        gpa = st.slider("Previous GPA (0–10)", 0.0, 10.0, 6.5)

        analyze = st.button("🔍 Analyze with Azure AI")

    if analyze:
        st.session_state.analyzed = True

    if st.session_state.analyzed:

        features = {
            "attendance_pct": attendance,
            "assignment_score": assignment,
            "quiz_score": quiz,
            "midterm_score": midterm,
            "study_hours_per_week": study_hours,
            "previous_gpa": gpa
        }

        scores = {
            "attendance": attendance,
            "assignment": assignment,
            "quiz": quiz,
            "midterm": midterm,
            "study_hours": study_hours,
            "gpa": gpa
        }

        weak_areas = []
        if attendance < 75: weak_areas.append("Attendance")
        if assignment < 60: weak_areas.append("Assignments")
        if quiz < 60: weak_areas.append("Quizzes")
        if midterm < 60: weak_areas.append("Midterm")
        if study_hours < 10: weak_areas.append("Study Hours")
        if gpa < 6.0: weak_areas.append("GPA")

        # 🔧 FIX 2: Loading state for ML
        with st.spinner("📊 Analyzing with Azure Machine Learning..."):
            prediction = ml_predictor.predict(features)

        st.success(f"🎯 Risk Level: **{prediction['risk_level']}**")
        st.plotly_chart(gauge_chart(attendance, "Attendance"), use_container_width=True)
        st.plotly_chart(gauge_chart((assignment+quiz+midterm)/3, "Average Score"), use_container_width=True)
        st.plotly_chart(create_radar_chart(scores), use_container_width=True)

        # 🔧 FIX 2: Loading state for OpenAI
        with st.spinner("🤖 Generating personalized guidance..."):
            guidance = openai_guide.generate_guidance(
                prediction["risk_level"],
                weak_areas,
                scores
            )

        st.markdown("## 🤖 Personalized AI Guidance")
        st.markdown(guidance)

if __name__ == "__main__":
    main()
