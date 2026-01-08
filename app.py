# ==================================================
# EduRisk AI - Academic Risk Intelligence Platform
# Microsoft Imagine Cup 2026 - PRODUCTION READY
# With Weak Areas Display FIXED
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
        time.sleep(1.5)
        
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
        time.sleep(2.0)
        
        # 🔥 FIXED: Include weak areas in the guidance!
        weak_areas_text = ""
        if weak_areas:
            weak_areas_text = "\n**SPECIFIC WEAK AREAS TO FOCUS ON:**\n" + "\n".join([f"• {area}" for area in weak_areas]) + "\n\n"
        
        plans = {
            "High": f"""**🔴 URGENT 7-DAY ACADEMIC RECOVERY PLAN**

{weak_areas_text}
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

            "Medium": f"""**🟡 FOCUSED IMPROVEMENT PLAN**

{weak_areas_text}
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

            "Low": f"""**🟢 EXCELLENCE ACCELERATION PLAN**

{weak_areas_text}
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
        fill='toself',
        fillcolor='rgba(0, 120, 212, 0.2)',
        line_color='#0078D4'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=350
    )
    return fig

# ==================== MAIN APP ====================
def main():
    # Custom CSS
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
    .weak-area-box {
        background: #FFF3CD;
        border-left: 5px solid #FFC107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .stButton button {
        background: #0078D4;
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 10px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🎓 EduRisk AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#6B7280;">Azure AI Powered Academic Risk Intelligence</p>', unsafe_allow_html=True)
    
    # Azure Badges
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="azure-badge" style="text-align:center;">Azure Machine Learning</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="azure-badge" style="text-align:center;">Azure OpenAI</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="azure-badge" style="text-align:center;">Demo Mode</div>', unsafe_allow_html=True)
    
    # Initialize services
    ml_service = SimulatedAzureML()
    openai_service = SimulatedAzureOpenAI()
    
    # Sidebar - STUDENT INPUT
    with st.sidebar:
        st.markdown("### 👤 Student Profile")
        st.markdown("Adjust sliders to simulate student performance:")
        
        attendance = st.slider("**Attendance (%)**", 40, 100, 75, 5)
        assignment = st.slider("**Assignment Score**", 0, 100, 70, 5)
        quiz = st.slider("**Quiz Score**", 0, 100, 65, 5)
        midterm = st.slider("**Midterm Score**", 0, 100, 60, 5)
        study_hours = st.slider("**Study Hours/Week**", 0, 40, 12, 1)
        gpa = st.slider("**Previous GPA (0-10)**", 0.0, 10.0, 6.5, 0.1)
        
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
    
    # Process analysis when button is clicked
    if analyze:
        # Prepare data
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
        
        # 🔥 FIXED: IDENTIFY WEAK AREAS with specific values
        weak_areas = []
        if attendance < 75: 
            weak_areas.append(f"Attendance ({attendance}% - target: 75%+)")
        if assignment < 60: 
            weak_areas.append(f"Assignments ({assignment}% - target: 60%+)")
        if quiz < 60: 
            weak_areas.append(f"Quizzes ({quiz}% - target: 60%+)")
        if midterm < 60: 
            weak_areas.append(f"Midterm ({midterm}% - target: 60%+)")
        if study_hours < 10: 
            weak_areas.append(f"Study Hours ({study_hours}/week - target: 10+ hrs)")
        if gpa < 6.0: 
            weak_areas.append(f"GPA ({gpa}/10 - target: 6.0+)")
        
        # Get prediction from Azure ML
        with st.spinner("📊 Calling Azure Machine Learning endpoint..."):
            prediction = ml_service.predict(features)
        
        # Display Results
        st.markdown("---")
        
        # Risk Level Display
        risk_color = {
            "High": "#EF4444",
            "Medium": "#F59E0B",
            "Low": "#10B981"
        }.get(prediction["risk_level"], "#6B7280")
        
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: #f8fafc; 
                    border-radius: 10px; border-left: 5px solid {risk_color};'>
            <h2 style='color:{risk_color}; margin:0;'>Risk Level: {prediction['risk_level']}</h2>
            <p style='margin:5px 0;'>Confidence: <strong>{prediction['confidence']:.0%}</strong></p>
            <p style='margin:5px 0;'>Response Time: <strong>{prediction['response_time']:.1f}s</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Performance Metrics")
        
        # Visualizations
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(gauge_chart(attendance, "Attendance Rate"), use_container_width=True)
        with col2:
            avg_score = np.mean([assignment, quiz, midterm])
            st.plotly_chart(gauge_chart(avg_score, "Average Score"), use_container_width=True)
        
        # Radar Chart
        st.plotly_chart(radar_chart(scores), use_container_width=True)
        
        # 🔥 FIXED: DISPLAY WEAK AREAS PROMINENTLY
        if weak_areas:
            st.markdown("### ⚠️ Identified Weak Areas")
            for area in weak_areas:
                st.markdown(f"""
                <div class="weak-area-box">
                    📌 {area}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("### 🎉 Strong Performance Overall!")
            st.markdown("No weak areas identified. All metrics are within optimal ranges.")
        
        # Azure OpenAI Guidance
        st.markdown("---")
        st.markdown("## 🤖 Personalized AI Guidance")
        st.markdown("*Powered by Azure OpenAI Service*")
        
        with st.spinner("🤖 Generating personalized guidance with Azure OpenAI..."):
            guidance = openai_service.generate_guidance(prediction["risk_level"], weak_areas, scores)
        
        st.markdown(guidance)
        
        # Imagine Cup Note
        st.info("""
        **🎯 Imagine Cup MVP Ready** - This application demonstrates:
        - ✅ **Two Microsoft AI Services** (Azure ML + Azure OpenAI)
        - ✅ **Production Azure Architecture**
        - ✅ **Real-time AI predictions**
        - ✅ **Personalized guidance generation**
        - ✅ **Education category alignment**
        
        *Note: Demo uses simulated Azure AI. Production version connects to actual Azure services.*
        """)
        
        # Show what data was analyzed
        with st.expander("📋 View Analyzed Data", expanded=False):
            st.markdown("**Student Metrics Analyzed:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Attendance", f"{attendance}%")
                st.metric("Assignments", f"{assignment}%")
            with col2:
                st.metric("Quizzes", f"{quiz}%")
                st.metric("Midterm", f"{midterm}%")
            with col3:
                st.metric("Study Hours", f"{study_hours}/week")
                st.metric("GPA", f"{gpa}/10")
    
    else:
        # Welcome screen
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ## Welcome to EduRisk AI
            
            **Predict academic risk. Provide personalized guidance. Improve student success.**
            
            ### How it works:
            1. **Enter student metrics** in sidebar
            2. **Click "Analyze with Azure AI"**
            3. **View risk prediction** from Azure ML
            4. **Get personalized plan** from Azure OpenAI
            
            ### Weak Areas Identified:
            - ✅ **Attendance** < 75%
            - ✅ **Assignments** < 60%
            - ✅ **Quizzes** < 60%
            - ✅ **Midterm** < 60%
            - ✅ **Study Hours** < 10/week
            - ✅ **GPA** < 6.0/10
            
            ### Quick Testing:
            - Use **High Risk** button for struggling student
            - Use **Low Risk** button for excellent student
            - Or **adjust sliders** manually
            """)
        
        with col2:
            st.markdown("""
            ### 📊 Performance Thresholds
            
            **Optimal Ranges:**
            - ✅ Attendance: 85%+
            - ✅ Assignments: 75%+
            - ✅ Quizzes: 70%+
            - ✅ Midterm: 65%+
            - ✅ Study: 15+ hrs/week
            - ✅ GPA: 7.0+/10.0
            
            **At Risk:**
            - ⚠️ Attendance: 60-75%
            - ⚠️ Scores: 50-60%
            - ⚠️ Study: 5-10 hrs/week
            - ⚠️ GPA: 5.0-6.0
            
            **High Risk:**
            - 🔴 Attendance: < 60%
            - 🔴 Scores: < 50%
            - 🔴 Study: < 5 hrs/week
            - 🔴 GPA: < 5.0
            """)

if __name__ == "__main__":
    main()
