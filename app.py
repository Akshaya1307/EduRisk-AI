# ==================================================
# EduRisk AI - Academic Risk Intelligence Platform
# Microsoft Imagine Cup 2026 - READY TO TEST
# Simulated Azure AI (Works Instantly)
# ==================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="EduRisk AI | Azure AI Demo",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SIMULATED AZURE SERVICES ====================
class SimulatedAzureML:
    def predict(self, features):
        time.sleep(1.5)  # Simulate API call
        
        # Calculate risk score
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
            confidence = 0.89
        elif score < 75:
            risk = "Medium"
            confidence = 0.82
        else:
            risk = "Low"
            confidence = 0.91
            
        return {
            "risk_level": risk,
            "confidence": confidence,
            "response_time": 1.5,
            "source": "Azure ML Simulator"
        }

class SimulatedAzureOpenAI:
    def generate_guidance(self, risk_level, weak_areas, scores):
        time.sleep(2.0)  # Simulate API call
        
        plans = {
            "High": """**🔴 URGENT 7-DAY ACADEMIC RECOVERY PLAN**

**Days 1-2: IMMEDIATE ACTION REQUIRED**
• Meet with academic advisor TODAY to create recovery plan
• Attend 100% of classes starting immediately
• Submit all missing assignments within 48 hours
• Identify top 3 priority subjects needing attention

**Days 3-5: INTENSIVE STUDY SESSIONS**
• Study 4+ hours daily in focused, distraction-free environment
• Target weakest subjects first (2 hours per weak subject daily)
• Work with tutor or study group for difficult concepts
• Complete 20+ practice problems per subject

**Days 6-7: MOMENTUM BUILDING**
• Take full practice exam under timed conditions
• Create detailed 30-day study schedule
• Review progress with mentor
• Set up weekly accountability check-ins""",

            "Medium": """**🟡 FOCUSED IMPROVEMENT PLAN**

**DAILY ROUTINE (2-3 hours structured study):**
• Morning: Review previous day's material (30 mins)
• Afternoon: Focus on one weak area (90 mins)
• Evening: Practice and application (60 mins)

**WEEKLY GOALS:**
1. Improve attendance to 90%+ consistently
2. Raise assignment scores by 10+ points
3. Master 5 key concepts in weakest subject
4. Complete all practice quizzes
5. Track progress with weekly self-assessment""",

            "Low": """**🟢 EXCELLENCE ACCELERATION PLAN**

**ADVANCED LEARNING:**
• Study topics beyond current curriculum
• Start independent academic project
• Prepare for academic competitions
• Learn advanced tools in your field

**LEADERSHIP DEVELOPMENT:**
• Mentor struggling classmates
• Lead study group sessions
• Present topics to your class
• Build academic portfolio"""
        }
        
        return plans.get(risk_level, plans["Medium"])

# ==================== VISUALIZATION ====================
def gauge_chart(value, title):
    color = "#10B981" if value >= 75 else "#F59E0B" if value >= 60 else "#EF4444"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": color}}
    ))
    fig.update_layout(height=250)
    return fig

def radar_chart(scores):
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
        height=350
    )
    return fig

# ==================== MAIN APP ====================
def main():
    # Header
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        font-size: 2.5rem;
        color: #0078D4;
        margin-bottom: 0.5rem;
    }
    .azure-badge {
        display: inline-block;
        background: #0078D4;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 5px;
    }
    </style>
    
    <h1 class="main-header">🎓 EduRisk AI</h1>
    <p style='text-align:center; color:#6B7280;'>Azure AI Powered Academic Risk Intelligence</p>
    
    <div style='text-align:center; margin:20px 0;'>
        <span class="azure-badge">Azure Machine Learning</span>
        <span class="azure-badge">Azure OpenAI</span>
        <span class="azure-badge">Demo Mode</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize simulated services
    ml_service = SimulatedAzureML()
    openai_service = SimulatedAzureOpenAI()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 Student Profile")
        
        attendance = st.slider("Attendance (%)", 40, 100, 75)
        assignment = st.slider("Assignment Score", 0, 100, 70)
        quiz = st.slider("Quiz Score", 0, 100, 65)
        midterm = st.slider("Midterm Score", 0, 100, 60)
        study_hours = st.slider("Study Hours/Week", 0, 40, 12)
        gpa = st.slider("Previous GPA (0-10)", 0.0, 10.0, 6.5)
        
        st.markdown("---")
        st.markdown("### 🚀 Quick Scenarios")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("High Risk", use_container_width=True):
                st.session_state.demo = "high"
                st.rerun()
        with col2:
            if st.button("Low Risk", use_container_width=True):
                st.session_state.demo = "low"
                st.rerun()
        
        st.markdown("---")
        analyze = st.button("🔍 **Analyze with Azure AI**", type="primary", use_container_width=True)
    
    # Apply demo scenarios
    if "demo" in st.session_state:
        if st.session_state.demo == "high":
            attendance = 55
            assignment = 50
            quiz = 45
            midterm = 40
            study_hours = 5
            gpa = 4.5
        elif st.session_state.demo == "low":
            attendance = 95
            assignment = 90
            quiz = 88
            midterm = 92
            study_hours = 25
            gpa = 9.2
    
    # Process analysis
    if analyze:
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
        
        # Identify weak areas
        weak_areas = []
        if attendance < 75: weak_areas.append(f"Attendance ({attendance}%)")
        if assignment < 60: weak_areas.append(f"Assignments ({assignment}%)")
        if quiz < 60: weak_areas.append(f"Quizzes ({quiz}%)")
        if midterm < 60: weak_areas.append(f"Midterm ({midterm}%)")
        if study_hours < 10: weak_areas.append(f"Study Hours ({study_hours}/week)")
        if gpa < 6.0: weak_areas.append(f"GPA ({gpa}/10)")
        
        # Get prediction
        with st.spinner("📊 Calling Azure Machine Learning..."):
            prediction = ml_service.predict(features)
        
        st.success(f"🎯 **Risk Level: {prediction['risk_level']}** (Confidence: {prediction['confidence']:.0%})")
        
        # Visualizations
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(gauge_chart(attendance, "Attendance Rate"), use_container_width=True)
        with col2:
            avg_score = np.mean([assignment, quiz, midterm])
            st.plotly_chart(gauge_chart(avg_score, "Average Score"), use_container_width=True)
        
        st.plotly_chart(radar_chart(scores), use_container_width=True)
        
        # Weak areas
        if weak_areas:
            with st.expander("⚠️ Areas Needing Improvement", expanded=True):
                for area in weak_areas:
                    st.markdown(f"• {area}")
        
        # AI Guidance
        st.markdown("---")
        st.markdown("## 🤖 Personalized AI Guidance")
        
        with st.spinner("🤖 Generating guidance with Azure OpenAI..."):
            guidance = openai_service.generate_guidance(prediction["risk_level"], weak_areas, scores)
        
        st.markdown(guidance)
        
        # Demo note
        st.info("""
        **🎯 Imagine Cup Demo Mode** - In production:
        - ✅ **Real Azure Machine Learning** endpoint
        - ✅ **Real Azure OpenAI Service** 
        - ✅ **Azure Key Vault** for security
        - ✅ **Azure App Service** hosting
        """)
    
    else:
        # Welcome screen
        st.markdown("""
        ## Welcome to EduRisk AI Demo
        
        ### To test:
        1. Adjust sliders in sidebar
        2. Click **"Analyze with Azure AI"**
        3. Or use **Quick Scenarios** for instant demos
        
        ### What you'll see:
        - 📊 Academic risk prediction
        - 📈 Interactive visualizations
        - 🤖 AI-generated guidance
        - 🎯 Personalized action plans
        
        *Note: This demo uses simulated Azure AI services. The production version connects to actual Azure ML and OpenAI.*
        """)

if __name__ == "__main__":
    main()
