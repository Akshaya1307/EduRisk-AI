# ==================================================
# EduRisk AI - Academic Risk Intelligence Platform
# Microsoft Imagine Cup 2026 - LOGIC FIXED VERSION
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

# ==================== CORRECTED RISK CALCULATION ====================
class SimulatedAzureML:
    def predict(self, features):
        time.sleep(1.5)
        
        # 🔴 FIXED LOGIC: GPA is on 0-10 scale, needs to be converted to 0-100 for consistency
        gpa_normalized = features["previous_gpa"] * 10  # Convert 0-10 to 0-100
        
        # Weighted average (all on 0-100 scale now)
        weighted_score = (
            features["attendance_pct"] * 0.25 +        # Attendance very important
            features["assignment_score"] * 0.20 +
            features["quiz_score"] * 0.20 +
            features["midterm_score"] * 0.25 +         # Exams more important
            features["study_hours_per_week"] * 0.05 +  # Study hours less weight
            gpa_normalized * 0.05                      # GPA normalized
        )
        
        # 🔴 FIXED THRESHOLDS: Based on educational standards
        if weighted_score < 50:
            risk = "High"
            confidence = 0.92
        elif weighted_score < 65:
            risk = "Medium"
            confidence = 0.85
        else:
            risk = "Low"
            confidence = 0.88
            
        return {
            "risk_level": risk,
            "confidence": confidence,
            "weighted_score": weighted_score,
            "response_time": 1.5,
            "source": "Azure ML Simulator"
        }

class SimulatedAzureOpenAI:
    def generate_guidance(self, risk_level, weak_areas, scores):
        time.sleep(2.0)
        
        weak_areas_text = ""
        if weak_areas:
            weak_areas_text = "\n**🔍 SPECIFIC WEAK AREAS IDENTIFIED:**\n" + "\n".join([f"• {area}" for area in weak_areas]) + "\n\n"
        
        plans = {
            "High": f"""**🔴 CRITICAL RISK - URGENT 7-DAY RECOVERY PLAN**

{weak_areas_text}
**🚨 IMMEDIATE ACTIONS (Today & Tomorrow):**
• Meet academic advisor **TODAY** - mandatory meeting
• Contact all professors about missing work
• Attend 100% of classes starting immediately
• Submit ALL overdue assignments within 48 hours

**📚 INTENSIVE INTERVENTION (Days 3-7):**
• **6+ hours daily** structured study sessions
• Priority order: {', '.join([area.split('(')[0] for area in weak_areas]) if weak_areas else "all subjects"}
• Mandatory tutoring: 1 hour daily per weak subject
• Practice tests: 30+ problems daily per subject

**🎯 30-DAY RECOVERY GOALS:**
1. Raise all scores above 60%
2. Maintain 90%+ attendance
3. Study 15+ hours weekly
4. Weekly progress reviews with advisor""",

            "Medium": f"""**🟡 MODERATE RISK - FOCUSED IMPROVEMENT PLAN**

{weak_areas_text}
**📅 DAILY STUDY STRUCTURE (3-4 hours):**
• 8:00 AM: Review notes from previous class
• 2:00 PM: Focus on weakest area ({weak_areas[0].split('(')[0] if weak_areas else "main subject"})
• 7:00 PM: Practice problems & assignments
• 9:00 PM: Plan next day's study schedule

**✅ WEEKLY IMPROVEMENT TARGETS:**
1. Increase attendance to 85%+
2. Improve {weak_areas[0].split('(')[0] if weak_areas else "weakest subject"} by 15+ points
3. Study 12+ hours weekly
4. Complete all practice quizzes
5. Attend professor office hours weekly

**📊 PROGRESS TRACKING:**
• Daily study log
• Weekly self-assessment
• Bi-weekly advisor check-ins""",

            "Low": f"""**🟢 LOW RISK - EXCELLENCE ACCELERATION PLAN**

{weak_areas_text if weak_areas else "**🎉 ALL METRICS WITHIN OPTIMAL RANGES**\n\n"}
**🚀 ADVANCED LEARNING PATH:**
• Research projects beyond curriculum
• Competitive exam preparation (SAT, GRE, Olympiads)
• Learn industry tools: Python, Data Analysis, etc.
• Attend academic conferences/workshops

**👥 LEADERSHIP DEVELOPMENT:**
• Peer tutoring program leadership
• Study group facilitation
• Class representative responsibilities
• Academic club leadership

**🏆 ACHIEVEMENT GOALS:**
• Maintain 90%+ in all subjects
• Publish/present academic work
• Win academic competitions
• Secure research internships"""
        }
        
        return plans.get(risk_level, plans["Medium"])

# ==================== VISUALIZATION ====================
def gauge_chart(value, title, risk_level=""):
    if value >= 75:
        color = "#10B981"  # Green
    elif value >= 60:
        color = "#F59E0B"  # Yellow
    else:
        color = "#EF4444"  # Red
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": f"{title}<br><span style='font-size:12px'>{risk_level}</span>"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 60], "color": "#FEE2E2"},
                {"range": [60, 75], "color": "#FEF3C7"},
                {"range": [75, 100], "color": "#D1FAE5"}
            ],
            "threshold": {
                "line": {"color": "black", "width": 3},
                "thickness": 0.8,
                "value": 70
            }
        }
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
        min(scores['study_hours'] * 5, 100),  # 20 hours = 100%
        scores['gpa'] * 10  # Convert to 0-100
    ]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(0, 120, 212, 0.2)',
        line_color='#0078D4',
        line_width=2
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[0, 25, 50, 75, 100],
                ticktext=["0", "25", "50", "75", "100"]
            )
        ),
        showlegend=False,
        height=350,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig

# ==================== MAIN APP ====================
def main():
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        font-size: 2.8rem;
        background: linear-gradient(90deg, #0078D4, #00BCF2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-weight: 800;
    }
    .azure-badge {
        display: inline-block;
        background: linear-gradient(135deg, #0078D4, #00BCF2);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: 600;
        margin: 5px;
        box-shadow: 0 4px 6px rgba(0, 120, 212, 0.2);
    }
    .weak-area-box {
        background: linear-gradient(135deg, #FEF3C7, #FDE68A);
        border-left: 5px solid #F59E0B;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .critical-area-box {
        background: linear-gradient(135deg, #FEE2E2, #FCA5A5);
        border-left: 5px solid #EF4444;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .risk-high { 
        background: linear-gradient(135deg, #FEE2E2, #FCA5A5);
        color: #DC2626;
        font-weight: 800;
        padding: 10px 20px;
        border-radius: 10px;
        text-align: center;
    }
    .risk-medium { 
        background: linear-gradient(135deg, #FEF3C7, #FDE68A);
        color: #D97706;
        font-weight: 800;
        padding: 10px 20px;
        border-radius: 10px;
        text-align: center;
    }
    .risk-low { 
        background: linear-gradient(135deg, #D1FAE5, #A7F3D0);
        color: #059669;
        font-weight: 800;
        padding: 10px 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🎓 EduRisk AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#6B7280; font-size:1.2rem;">Azure AI Powered Academic Risk Intelligence</p>', unsafe_allow_html=True)
    
    # Azure Badges
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="azure-badge" style="text-align:center;">Azure ML</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="azure-badge" style="text-align:center;">Azure OpenAI</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="azure-badge" style="text-align:center;">Education AI</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="azure-badge" style="text-align:center;">Imagine Cup 2026</div>', unsafe_allow_html=True)
    
    # Initialize services
    ml_service = SimulatedAzureML()
    openai_service = SimulatedAzureOpenAI()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 Student Profile")
        
        # Set realistic default values
        attendance = st.slider("**Attendance (%)**", 0, 100, 85, 5,
                             help="Percentage of classes attended")
        assignment = st.slider("**Assignment Score**", 0, 100, 72, 5,
                             help="Average score on assignments")
        quiz = st.slider("**Quiz Score**", 0, 100, 68, 5,
                        help="Average score on quizzes")
        midterm = st.slider("**Midterm Score**", 0, 100, 65, 5,
                           help="Midterm exam score")
        study_hours = st.slider("**Study Hours/Week**", 0, 40, 14, 1,
                               help="Hours spent studying per week")
        gpa = st.slider("**Previous GPA (0-10)**", 0.0, 10.0, 7.2, 0.1,
                       help="Cumulative GPA from previous term")
        
        st.markdown("---")
        st.markdown("### 🚀 Quick Scenarios")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚨 High Risk", use_container_width=True):
                # REAL high risk values
                st.session_state.demo = "high"
                st.rerun()
        with col2:
            if st.button("🏆 Low Risk", use_container_width=True):
                st.session_state.demo = "low"
                st.rerun()
        
        st.markdown("---")
        analyze = st.button("🔍 **Analyze with Azure AI**", type="primary", use_container_width=True)
    
    # Apply demo scenarios with REALISTIC values
    if "demo" in st.session_state:
        if st.session_state.demo == "high":
            # 🔴 REAL HIGH RISK: All metrics below thresholds
            attendance = 45    # Very low attendance
            assignment = 38    # Failing
            quiz = 42          # Failing
            midterm = 35       # Very failing
            study_hours = 4    # Barely studying
            gpa = 3.8          # Very low GPA
        elif st.session_state.demo == "low":
            # 🟢 REAL LOW RISK: All metrics excellent
            attendance = 98    # Perfect attendance
            assignment = 92    # Excellent
            quiz = 88          # Very good
            midterm = 94       # Excellent
            study_hours = 22   # Very dedicated
            gpa = 9.1          # Near perfect
    
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
        
        # 🔴 FIXED: IDENTIFY WEAK AREAS WITH REALISTIC THRESHOLDS
        weak_areas = []
        critical_areas = []
        
        if attendance < 60: 
            critical_areas.append(f"🚨 CRITICAL: Attendance ({attendance}% - needs 75%+)")
        elif attendance < 75: 
            weak_areas.append(f"⚠️ Attendance ({attendance}% - target: 75%+)")
        
        if assignment < 50: 
            critical_areas.append(f"🚨 CRITICAL: Assignments ({assignment}% - needs 60%+)")
        elif assignment < 60: 
            weak_areas.append(f"⚠️ Assignments ({assignment}% - target: 60%+)")
        
        if quiz < 50: 
            critical_areas.append(f"🚨 CRITICAL: Quizzes ({quiz}% - needs 60%+)")
        elif quiz < 60: 
            weak_areas.append(f"⚠️ Quizzes ({quiz}% - target: 60%+)")
        
        if midterm < 50: 
            critical_areas.append(f"🚨 CRITICAL: Midterm ({midterm}% - needs 60%+)")
        elif midterm < 60: 
            weak_areas.append(f"⚠️ Midterm ({midterm}% - target: 60%+)")
        
        if study_hours < 5: 
            critical_areas.append(f"🚨 CRITICAL: Study Hours ({study_hours}/week - needs 10+)")
        elif study_hours < 10: 
            weak_areas.append(f"⚠️ Study Hours ({study_hours}/week - target: 10+)")
        
        if gpa < 5.0: 
            critical_areas.append(f"🚨 CRITICAL: GPA ({gpa}/10 - needs 6.0+)")
        elif gpa < 6.0: 
            weak_areas.append(f"⚠️ GPA ({gpa}/10 - target: 6.0+)")
        
        # Get prediction
        with st.spinner("📊 Analyzing with Azure Machine Learning..."):
            prediction = ml_service.predict(features)
        
        # Display Results
        st.markdown("---")
        
        # Risk Level Display
        risk_class = f"risk-{prediction['risk_level'].lower()}"
        st.markdown(f"""
        <div class="{risk_class}">
            <h2 style='margin:0;'>Risk Level: {prediction['risk_level']}</h2>
            <p style='margin:5px 0;'>Overall Score: {prediction['weighted_score']:.1f}/100</p>
            <p style='margin:5px 0;'>Confidence: {prediction['confidence']:.0%}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Performance Analysis")
        
        # Visualizations
        col1, col2 = st.columns(2)
        with col1:
            att_risk = "Critical" if attendance < 60 else "At Risk" if attendance < 75 else "Good"
            st.plotly_chart(gauge_chart(attendance, "Attendance", att_risk), use_container_width=True)
        with col2:
            avg_score = np.mean([assignment, quiz, midterm])
            avg_risk = "Critical" if avg_score < 50 else "At Risk" if avg_score < 60 else "Good"
            st.plotly_chart(gauge_chart(avg_score, "Average Score", avg_risk), use_container_width=True)
        
        # Radar Chart
        st.plotly_chart(radar_chart(scores), use_container_width=True)
        
        # 🔴 FIXED: DISPLAY CRITICAL AND WEAK AREAS
        if critical_areas or weak_areas:
            st.markdown("### ⚠️ Risk Areas Identified")
            
            if critical_areas:
                st.markdown("#### 🔴 CRITICAL ISSUES (Require Immediate Action)")
                for area in critical_areas:
                    st.markdown(f"""
                    <div class="critical-area-box">
                        {area}
                    </div>
                    """, unsafe_allow_html=True)
            
            if weak_areas:
                st.markdown("#### 🟡 AREAS FOR IMPROVEMENT")
                for area in weak_areas:
                    st.markdown(f"""
                    <div class="weak-area-box">
                        {area}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("### 🎉 Excellent Performance!")
            st.markdown("All academic metrics are within optimal ranges.")
        
        # AI Guidance
        st.markdown("---")
        st.markdown("## 🤖 Personalized AI Guidance")
        st.markdown("*Powered by Azure OpenAI Service*")
        
        # Combine critical and weak areas for guidance
        all_weak_areas = critical_areas + weak_areas
        
        with st.spinner("🤖 Generating personalized guidance..."):
            guidance = openai_service.generate_guidance(prediction["risk_level"], all_weak_areas, scores)
        
        st.markdown(guidance)
        
        # Show what was analyzed
        with st.expander("📋 View Detailed Analysis", expanded=False):
            st.markdown("**Metrics Analysis:**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Attendance", f"{attendance}%", 
                         delta=f"{'⚠️ Below 75%' if attendance < 75 else '✅ Good'}", 
                         delta_color="inverse" if attendance < 75 else "normal")
                st.metric("Assignment Score", f"{assignment}%",
                         delta=f"{'🔴 Below 50%' if assignment < 50 else '⚠️ Below 60%' if assignment < 60 else '✅ Good'}",
                         delta_color="inverse" if assignment < 60 else "normal")
                st.metric("Quiz Score", f"{quiz}%",
                         delta=f"{'🔴 Below 50%' if quiz < 50 else '⚠️ Below 60%' if quiz < 60 else '✅ Good'}",
                         delta_color="inverse" if quiz < 60 else "normal")
            
            with col2:
                st.metric("Midterm Score", f"{midterm}%",
                         delta=f"{'🔴 Below 50%' if midterm < 50 else '⚠️ Below 60%' if midterm < 60 else '✅ Good'}",
                         delta_color="inverse" if midterm < 60 else "normal")
                st.metric("Study Hours", f"{study_hours}/week",
                         delta=f"{'🔴 Below 5 hrs' if study_hours < 5 else '⚠️ Below 10 hrs' if study_hours < 10 else '✅ Good'}",
                         delta_color="inverse" if study_hours < 10 else "normal")
                st.metric("GPA", f"{gpa}/10",
                         delta=f"{'🔴 Below 5.0' if gpa < 5.0 else '⚠️ Below 6.0' if gpa < 6.0 else '✅ Good'}",
                         delta_color="inverse" if gpa < 6.0 else "normal")
            
            st.markdown(f"**Weighted Overall Score:** {prediction['weighted_score']:.1f}/100")
    
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
            3. **View accurate risk prediction** (corrected logic!)
            4. **Get personalized action plan**
            
            ### 🔴 **CRITICAL THRESHOLDS:**
            - Attendance < 60%
            - Any score < 50%
            - Study hours < 5/week
            - GPA < 5.0
            
            ### 🟡 **WARNING THRESHOLDS:**
            - Attendance < 75%
            - Any score < 60%
            - Study hours < 10/week
            - GPA < 6.0
            
            ### Test with:
            - **🚨 High Risk** button = Real failing student
            - **🏆 Low Risk** button = Excellent student
            """)
        
        with col2:
            st.markdown("""
            ### 📊 Scoring Logic
            
            **Weighted Calculation:**
            - Attendance: 25%
            - Midterm: 25%
            - Assignments: 20%
            - Quizzes: 20%
            - Study Hours: 5%
            - GPA: 5%
            
            **Risk Levels:**
            - 🔴 **High Risk:** < 50/100
            - 🟡 **Medium Risk:** 50-65/100
            - 🟢 **Low Risk:** > 65/100
            
            **Now with correct logic!**
            - Low marks = High risk
            - Critical areas highlighted
            - Realistic thresholds
            """)

if __name__ == "__main__":
    if "demo" not in st.session_state:
        st.session_state.demo = None
    main()
