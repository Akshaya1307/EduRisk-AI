# ==================================================
# EduRisk AI - Academic Risk Intelligence Platform
# Microsoft Imagine Cup 2026
# UI-ENHANCED | LOGIC UNCHANGED
# ==================================================

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="EduRisk AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
body {
    background-color: #F9FAFB;
}
.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #0078D4, #00BCF2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    text-align: center;
    color: #6B7280;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}
.risk-high {
    background: linear-gradient(135deg, #FEE2E2, #FCA5A5);
    color: #7F1D1D;
}
.risk-medium {
    background: linear-gradient(135deg, #FEF3C7, #FDE68A);
    color: #92400E;
}
.risk-low {
    background: linear-gradient(135deg, #D1FAE5, #A7F3D0);
    color: #065F46;
}
.risk-banner {
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    font-size: 1.8rem;
    font-weight: 800;
}
.weak-card {
    background: #FFFBEB;
    border-left: 6px solid #F59E0B;
    padding: 14px;
    border-radius: 8px;
    margin-bottom: 10px;
}
.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 20px 0 10px;
}
</style>
""", unsafe_allow_html=True)

# ==================== SIMULATED AZURE ML ====================
class SimulatedAzureML:
    def predict(self, f):
        time.sleep(1.2)

        study_norm = min(f["study_hours_per_week"], 20) / 20 * 100
        gpa_norm = f["previous_gpa"] * 10

        score = (
            f["attendance_pct"] * 0.25 +
            f["assignment_score"] * 0.20 +
            f["quiz_score"] * 0.20 +
            f["midterm_score"] * 0.25 +
            study_norm * 0.05 +
            gpa_norm * 0.05
        )

        if (
            f["attendance_pct"] < 60 or
            f["assignment_score"] < 50 or
            f["quiz_score"] < 50 or
            f["midterm_score"] < 50 or
            f["study_hours_per_week"] < 5 or
            f["previous_gpa"] < 5.0
        ):
            return {"risk": "High", "confidence": 0.95, "score": score}

        if score < 55:
            return {"risk": "High", "confidence": 0.90, "score": score}
        elif score < 70:
            return {"risk": "Medium", "confidence": 0.85, "score": score}
        else:
            return {"risk": "Low", "confidence": 0.88, "score": score}

# ==================== SIMULATED OPENAI ====================
class SimulatedOpenAI:
    def guidance(self, risk, weak):
        time.sleep(1.3)
        weak_text = "\n".join([f"• {w}" for w in weak]) if weak else "• No major weak areas"

        plans = {
            "High": f"""
### 🔴 URGENT RECOVERY PLAN
{weak_text}

• Meet academic advisor immediately  
• 5–6 hours focused study daily  
• Mandatory tutoring  
• Strict attendance tracking  
""",
            "Medium": f"""
### 🟡 IMPROVEMENT PLAN
{weak_text}

• 3–4 hours structured study  
• Focus weakest subject daily  
• Weekly progress review  
""",
            "Low": """
### 🟢 EXCELLENCE PLAN

• Maintain consistency  
• Peer mentoring  
• Advanced learning projects  
"""
        }
        return plans[risk]

# ==================== VISUALS ====================
def gauge(val, title):
    color = "#10B981" if val >= 75 else "#F59E0B" if val >= 60 else "#EF4444"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        title={"text": title},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": color}}
    ))
    fig.update_layout(height=250)
    return fig

# ==================== MAIN ====================
def main():
    ml = SimulatedAzureML()
    ai = SimulatedOpenAI()

    st.markdown('<div class="main-title">🎓 EduRisk AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Academic Risk Intelligence Platform</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 👤 Student Profile")
        attendance = st.slider("Attendance (%)", 0, 100, 75)
        assignment = st.slider("Assignment Score", 0, 100, 65)
        quiz = st.slider("Quiz Score", 0, 100, 60)
        midterm = st.slider("Midterm Score", 0, 100, 62)
        study = st.slider("Study Hours / Week", 0, 40, 10)
        gpa = st.slider("Previous GPA (0–10)", 0.0, 10.0, 6.5)
        analyze = st.button("🔍 Analyze Risk", type="primary", use_container_width=True)

    if analyze:
        features = {
            "attendance_pct": attendance,
            "assignment_score": assignment,
            "quiz_score": quiz,
            "midterm_score": midterm,
            "study_hours_per_week": study,
            "previous_gpa": gpa
        }

        weak = []
        if attendance < 75: weak.append(f"Attendance ({attendance}%)")
        if assignment < 60: weak.append(f"Assignments ({assignment}%)")
        if quiz < 60: weak.append(f"Quizzes ({quiz}%)")
        if midterm < 60: weak.append(f"Midterm ({midterm}%)")
        if study < 10: weak.append(f"Study Hours ({study}/week)")
        if gpa < 6.0: weak.append(f"GPA ({gpa}/10)")

        with st.spinner("Analyzing academic risk..."):
            pred = ml.predict(features)

        st.markdown("---")
        st.markdown(
            f'<div class="risk-banner risk-{pred["risk"].lower()}">Risk Level: {pred["risk"]}</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.plotly_chart(gauge(attendance, "Attendance"), use_container_width=True)
        with col2:
            st.plotly_chart(gauge(np.mean([assignment, quiz, midterm]), "Academic Avg"), use_container_width=True)
        with col3:
            st.metric("Overall Score", f"{pred['score']:.1f}/100", f"{pred['confidence']*100:.0f}% confidence")

        if weak:
            st.markdown("### ⚠️ Weak Areas")
            for w in weak:
                st.markdown(f'<div class="weak-card">{w}</div>', unsafe_allow_html=True)

        st.markdown("### 🤖 Personalized Guidance")
        with st.spinner("Generating guidance..."):
            st.markdown(ai.guidance(pred["risk"], weak))

if __name__ == "__main__":
    main()
