# ==================================================
# EduRisk AI - Academic Risk Intelligence Platform
# Microsoft Imagine Cup 2026 - FINAL LOGIC-CORRECT VERSION
# Local Simulation (No Azure Dependency)
# ==================================================

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="EduRisk AI | Academic Risk Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SIMULATED AZURE ML ====================
class SimulatedAzureML:
    def predict(self, features):
        time.sleep(1.2)

        # Normalize inputs
        attendance = features["attendance_pct"]
        assignment = features["assignment_score"]
        quiz = features["quiz_score"]
        midterm = features["midterm_score"]

        study_hours_norm = min(features["study_hours_per_week"], 20) / 20 * 100
        gpa_norm = features["previous_gpa"] * 10

        weighted_score = (
            attendance * 0.25 +
            assignment * 0.20 +
            quiz * 0.20 +
            midterm * 0.25 +
            study_hours_norm * 0.05 +
            gpa_norm * 0.05
        )

        # 🚨 HARD OVERRIDE — CRITICAL FAILURES
        if (
            attendance < 60 or
            assignment < 50 or
            quiz < 50 or
            midterm < 50 or
            features["study_hours_per_week"] < 5 or
            features["previous_gpa"] < 5.0
        ):
            return {
                "risk_level": "High",
                "confidence": 0.95,
                "weighted_score": weighted_score
            }

        # Normal thresholds
        if weighted_score < 55:
            risk = "High"
            confidence = 0.90
        elif weighted_score < 70:
            risk = "Medium"
            confidence = 0.85
        else:
            risk = "Low"
            confidence = 0.88

        return {
            "risk_level": risk,
            "confidence": confidence,
            "weighted_score": weighted_score
        }

# ==================== SIMULATED AZURE OPENAI ====================
class SimulatedAzureOpenAI:
    def generate_guidance(self, risk_level, weak_areas):
        time.sleep(1.5)

        weak_text = "\n".join([f"• {w}" for w in weak_areas]) if weak_areas else "• No weak areas detected"

        plans = {
            "High": f"""
### 🔴 URGENT 7-DAY RECOVERY PLAN

**Identified Problems**
{weak_text}

**Immediate (Days 1–2)**
• Mandatory advisor meeting  
• Contact professors  
• 100% attendance  
• Submit pending work  

**Days 3–7**
• 5–6 hrs/day focused study  
• Daily tutoring for weak subjects  
• Practice tests + revision  

**Goal:** Move all metrics above minimum academic thresholds
""",

            "Medium": f"""
### 🟡 FOCUSED IMPROVEMENT PLAN

**Areas to Improve**
{weak_text}

**Daily Routine**
• 3–4 hrs study  
• Focus on weakest subject  
• Weekly office hours  

**Goal:** Push performance into safe academic zone
""",

            "Low": """
### 🟢 EXCELLENCE & GROWTH PLAN

• Maintain strong habits  
• Peer mentoring  
• Advanced learning projects  
• Internship / competition preparation  

**Goal:** Academic excellence & leadership
"""
        }

        return plans[risk_level]

# ==================== VISUALS ====================
def gauge(value, title):
    color = "#10B981" if value >= 75 else "#F59E0B" if value >= 60 else "#EF4444"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 60], "color": "#FEE2E2"},
                {"range": [60, 75], "color": "#FEF3C7"},
                {"range": [75, 100], "color": "#D1FAE5"},
            ]
        }
    ))
    fig.update_layout(height=250)
    return fig

def radar(scores):
    categories = ["Attendance", "Assignments", "Quizzes", "Midterm", "Study Hours", "GPA"]
    values = [
        scores["attendance"],
        scores["assignment"],
        scores["quiz"],
        scores["midterm"],
        min(scores["study_hours"] * 5, 100),
        scores["gpa"] * 10
    ]

    fig = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself"
    ))
    fig.update_layout(polar=dict(radialaxis=dict(range=[0, 100])), showlegend=False)
    return fig

# ==================== MAIN APP ====================
def main():
    ml = SimulatedAzureML()
    ai = SimulatedAzureOpenAI()

    st.markdown("<h1 style='text-align:center;'>🎓 EduRisk AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Academic Risk Intelligence (Local Demo)</p>", unsafe_allow_html=True)

    with st.sidebar:
        st.header("Student Metrics")

        attendance = st.slider("Attendance (%)", 0, 100, 75)
        assignment = st.slider("Assignment Score", 0, 100, 65)
        quiz = st.slider("Quiz Score", 0, 100, 60)
        midterm = st.slider("Midterm Score", 0, 100, 62)
        study_hours = st.slider("Study Hours / Week", 0, 40, 10)
        gpa = st.slider("Previous GPA (0–10)", 0.0, 10.0, 6.5)

        analyze = st.button("Analyze Risk")

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

        weak_areas = []
        if attendance < 75: weak_areas.append(f"Attendance ({attendance}%)")
        if assignment < 60: weak_areas.append(f"Assignments ({assignment}%)")
        if quiz < 60: weak_areas.append(f"Quizzes ({quiz}%)")
        if midterm < 60: weak_areas.append(f"Midterm ({midterm}%)")
        if study_hours < 10: weak_areas.append(f"Study Hours ({study_hours}/week)")
        if gpa < 6.0: weak_areas.append(f"GPA ({gpa}/10)")

        with st.spinner("Analyzing academic risk..."):
            prediction = ml.predict(features)

        st.markdown("---")
        st.subheader(f"Risk Level: {prediction['risk_level']}")
        st.write(f"Confidence: {prediction['confidence']*100:.0f}%")
        st.write(f"Overall Score: {prediction['weighted_score']:.1f}/100")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(gauge(attendance, "Attendance"), use_container_width=True)
        with col2:
            st.plotly_chart(gauge(np.mean([assignment, quiz, midterm]), "Academic Average"), use_container_width=True)

        st.plotly_chart(radar(scores), use_container_width=True)

        if weak_areas:
            st.markdown("### ⚠️ Weak Areas")
            for w in weak_areas:
                st.markdown(f"- **{w}**")

        st.markdown("---")
        st.subheader("🤖 Personalized Guidance")

        with st.spinner("Generating guidance..."):
            guidance = ai.generate_guidance(prediction["risk_level"], weak_areas)

        st.markdown(guidance)

if __name__ == "__main__":
    main()
