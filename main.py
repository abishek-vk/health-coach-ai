"""
main.py - Professional Streamlit Dashboard for Personal Health Coach AI
Interactive web interface with modern UI, charts, and data management
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
from pathlib import Path

# Import custom modules
from modules.data_input import HealthDataCollector
from modules.file_storage import JSONHealthStorage
from modules.profile_summarizer import HealthProfileSummarizer
from modules.recommendation_engine import RecommendationEngine


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Health Coach AI | Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Personal Health Coach AI v2.0 - Professional Edition"
    }
)

# ============================================================================
# PROFESSIONAL CSS STYLING
# ============================================================================
st.markdown("""
    <style>
    /* Root Colors */
    :root {
        --primary-color: #2E7D32;
        --secondary-color: #1976D2;
        --accent-color: #F57C00;
        --success-color: #388E3C;
        --warning-color: #FBC02D;
        --danger-color: #D32F2F;
        --light-bg: #F5F7FA;
        --card-bg: #FFFFFF;
        --text-primary: #212121;
        --text-secondary: #757575;
        --border-color: #E0E0E0;
    }
    
    /* Main Container */
    .main {
        background-color: #F5F7FA;
    }
    
    /* Professional Header */
    .header-container {
        background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%);
        padding: 40px 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(90deg, #FFFFFF, #E8F5E9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: 10px;
        opacity: 0.95;
    }
    
    /* Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F5F5F5 100%);
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 5px solid #2E7D32;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .metric-card-success {
        border-left-color: #388E3C;
    }
    
    .metric-card-info {
        border-left-color: #1976D2;
    }
    
    .metric-card-warning {
        border-left-color: #F57C00;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2E7D32;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: #757575;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-unit {
        font-size: 0.85rem;
        color: #999;
        margin-left: 5px;
    }
    
    /* Alert Boxes */
    .alert-box {
        background-color: #FFF8E1;
        border-left: 5px solid #FBC02D;
        padding: 18px;
        border-radius: 8px;
        margin: 15px 0;
        color: #856404;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .success-box {
        background-color: #E8F5E9;
        border-left: 5px solid #388E3C;
        padding: 18px;
        border-radius: 8px;
        margin: 15px 0;
        color: #2E5233;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .danger-box {
        background-color: #FFEBEE;
        border-left: 5px solid #D32F2F;
        padding: 18px;
        border-radius: 8px;
        margin: 15px 0;
        color: #6F1210;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .info-box {
        background-color: #E3F2FD;
        border-left: 5px solid #1976D2;
        padding: 18px;
        border-radius: 8px;
        margin: 15px 0;
        color: #0C3B66;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2E7D32;
        margin: 30px 0 20px 0;
        padding-bottom: 15px;
        border-bottom: 3px solid #2E7D32;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F5F7FA;
        border-radius: 8px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border-radius: 6px;
        margin: 5px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.4);
        transform: translateY(-2px);
    }
    
    /* Input Fields */
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div [data-baseweb="select"] {
        border-radius: 6px;
        border: 2px solid #E0E0E0;
    }
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #2E7D32;
        box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1);
    }
    
    /* Divider */
    .divider {
        margin: 30px 0;
        border-bottom: 2px solid #E0E0E0;
    }
    
    /* Progress Bar */
    .progress-container {
        margin: 20px 0;
    }
    
    .progress-bar {
        background-color: #E0E0E0;
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        background: linear-gradient(90deg, #2E7D32, #388E3C);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Sidebar */
    .sidebar-container {
        background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .user-info {
        background-color: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #FBC02D;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 5px 5px 0;
    }
    
    .badge-success {
        background-color: #C8E6C9;
        color: #1B5E20;
    }
    
    .badge-warning {
        background-color: #FFE0B2;
        color: #E65100;
    }
    
    .badge-danger {
        background-color: #FFCDD2;
        color: #B71C1C;
    }
    
    .badge-info {
        background-color: #BBDEFB;
        color: #0D47A1;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #757575;
        font-size: 0.85rem;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #E0E0E0;
    }
    
    /* Chart Container */
    .chart-container {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "collector" not in st.session_state:
        st.session_state.collector = HealthDataCollector()
    if "storage" not in st.session_state:
        st.session_state.storage = JSONHealthStorage(data_dir="data")
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def create_metric_card(label, value, unit="", category="", emoji="📊"):
    """Create a styled metric card"""
    card_html = f"""
    <div class="metric-card">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <div class="metric-label">{emoji} {label}</div>
                <div class="metric-value">{value}<span class="metric-unit">{unit}</span></div>
                {f'<span class="badge badge-{get_badge_type(category)}">{category}</span>' if category else ''}
            </div>
        </div>
    </div>
    """
    return card_html


def get_badge_type(category):
    """Get badge type based on category"""
    if category:
        category_lower = category.lower()
        if "good" in category_lower or "excellent" in category_lower or "optimal" in category_lower:
            return "success"
        elif "warning" in category_lower or "caution" in category_lower:
            return "warning"
        elif "danger" in category_lower or "risk" in category_lower or "poor" in category_lower:
            return "danger"
        else:
            return "info"
    return "info"


def display_professional_header():
    """Display professional gradient header"""
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🏥 Health Coach AI</h1>
        <p class="header-subtitle">Your Intelligent Personal Health & Wellness Companion</p>
    </div>
    """, unsafe_allow_html=True)


def create_plotly_steps_chart(user_records):
    """Create interactive Plotly chart for daily steps"""
    steps_data = []
    for record in user_records:
        data = record.get("data", record)
        steps_data.append({
            "Date": record.get("timestamp", "")[:10],
            "Steps": data.get("daily_steps", 0)
        })
    
    if not steps_data:
        return None
    
    df_steps = pd.DataFrame(steps_data)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_steps["Date"],
        y=df_steps["Steps"],
        mode="lines+markers",
        name="Daily Steps",
        line=dict(color="#2E7D32", width=3),
        marker=dict(size=8, color="#2E7D32", symbol="circle"),
        fill="tozeroy",
        fillcolor="rgba(46, 125, 50, 0.1)"
    ))
    
    fig.add_hline(y=7000, line_dash="dash", line_color="#F57C00", 
                  annotation_text="Daily Goal", annotation_position="right")
    
    fig.update_layout(
        title="Daily Steps Trend",
        xaxis_title="Date",
        yaxis_title="Steps",
        hovermode="x unified",
        template="plotly_white",
        plot_bgcolor="rgba(245,247,250,0.5)",
        paper_bgcolor="white",
        height=400
    )
    
    return fig


def create_plotly_sleep_chart(user_records):
    """Create interactive Plotly chart for sleep hours"""
    sleep_data = []
    for record in user_records:
        data = record.get("data", record)
        sleep_data.append({
            "Date": record.get("timestamp", "")[:10],
            "Sleep": data.get("sleep_hours", 0)
        })
    
    if not sleep_data:
        return None
    
    df_sleep = pd.DataFrame(sleep_data)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_sleep["Date"],
        y=df_sleep["Sleep"],
        mode="lines+markers",
        name="Sleep Hours",
        line=dict(color="#1976D2", width=3),
        marker=dict(size=8, color="#1976D2", symbol="circle"),
        fill="tozeroy",
        fillcolor="rgba(25, 118, 210, 0.1)"
    ))
    
    fig.add_hline(y=8, line_dash="dash", line_color="#F57C00",
                  annotation_text="Recommended", annotation_position="right")
    
    fig.update_layout(
        title="Sleep Hours Trend",
        xaxis_title="Date",
        yaxis_title="Hours",
        hovermode="x unified",
        template="plotly_white",
        plot_bgcolor="rgba(245,247,250,0.5)",
        paper_bgcolor="white",
        height=400
    )
    
    return fig


def create_water_intake_chart(user_records):
    """Create interactive Plotly chart for water intake"""
    water_data = []
    for record in user_records:
        data = record.get("data", record)
        water_data.append({
            "Date": record.get("timestamp", "")[:10],
            "Water": data.get("water_intake_liters", 0)
        })
    
    if not water_data:
        return None
    
    df_water = pd.DataFrame(water_data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_water["Date"],
        y=df_water["Water"],
        name="Water Intake",
        marker=dict(
            color=df_water["Water"],
            colorscale="Greens",
            showscale=True,
            colorbar=dict(title="Liters")
        )
    ))
    
    fig.add_hline(y=2, line_dash="dash", line_color="#F57C00",
                  annotation_text="Daily Goal", annotation_position="right")
    
    fig.update_layout(
        title="Daily Water Intake",
        xaxis_title="Date",
        yaxis_title="Liters",
        template="plotly_white",
        plot_bgcolor="rgba(245,247,250,0.5)",
        paper_bgcolor="white",
        height=400
    )
    
    return fig




# ============================================================================
# PAGE FUNCTIONS
# ============================================================================
def page_home():
    """Home page with introduction and user setup"""
    st.markdown("""
    <h2 class="section-header">👋 Welcome to Your Health Journey</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2E7D32; margin-top: 0;">📋 How It Works</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        1. **Create Your Profile** - Enter your basic health information
        2. **Daily Tracking** - Log your daily metrics (steps, sleep, water)
        3. **Smart Analysis** - Get intelligent insights about your health
        4. **Personalized Tips** - Receive customized recommendations
        5. **Track Progress** - Monitor your improvements over time
        """)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1976D2; margin-top: 0;">✨ Key Features</h3>
        </div>
        """, unsafe_allow_html=True)
        
        features = [
            ("📊", "Real-time Health Monitoring"),
            ("📈", "Progress Tracking & Analytics"),
            ("🤖", "AI-Powered Personalization"),
            ("⚡", "Instant Health Insights"),
            ("🏆", "Achievement & Goal Tracking"),
        ]
        
        for icon, feature in features:
            st.write(f"{icon} **{feature}**")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <h3 style="color: #2E7D32; margin-bottom: 20px;">🚀 Get Started Today</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1], gap="medium")
    
    with col1:
        user_id = st.text_input(
            "👤 Create Your User ID",
            placeholder="e.g., john_doe, user_001",
            label_visibility="collapsed"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("Start Tracking", use_container_width=True, type="primary"):
            if user_id.strip():
                st.session_state.user_id = user_id.strip()
                st.session_state.current_page = "Input Health Data"
                st.rerun()
            else:
                st.error("Please enter a valid User ID")
    
    with col3:
        if st.session_state.user_id:
            st.write("")
            st.write("")
            if st.button("Continue", use_container_width=True):
                st.rerun()
    
    if st.session_state.user_id:
        st.markdown(f"""
        <div class="info-box">
            ✅ <strong>You're logged in as:</strong> <code>{st.session_state.user_id}</code>
        </div>
        """, unsafe_allow_html=True)




def page_input_health_data():
    """Page for inputting health data with enhanced UI"""
    st.markdown("""
    <h2 class="section-header">📥 Update Your Health Data</h2>
    """, unsafe_allow_html=True)
    
    if not st.session_state.user_id:
        st.error("Please enter a User ID on the Home page first")
        return
    
    st.markdown(f"""
    <div class="info-box">
        👤 <strong>User ID:</strong> <code>{st.session_state.user_id}</code>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different data input sections
    tab1, tab2 = st.tabs(["👤 Basic Information", "📊 Daily Metrics"])
    
    with tab1:
        st.markdown("""
        <h3 style="color: #2E7D32; margin-bottom: 20px;">📋 Your Basic Health Profile</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            age = st.number_input(
                "📅 Age (years)",
                min_value=1,
                max_value=150,
                value=30,
                step=1
            )
            height = st.number_input(
                "📏 Height (cm)",
                min_value=30,
                max_value=300,
                value=175,
                step=1
            )
            
        with col2:
            gender = st.selectbox(
                "👥 Gender",
                ["Male", "Female", "Other", "Prefer not to say"]
            )
            weight = st.number_input(
                "⚖️ Weight (kg)",
                min_value=1,
                max_value=300,
                value=75,
                step=0.5
            )
        
        medical_conditions = st.text_area(
            "🏥 Medical Conditions (if any)",
            placeholder="Enter any chronic conditions, allergies, or health concerns...",
            height=100
        )
        
        user_info = {
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "medical_conditions": medical_conditions
        }
    
    with tab2:
        st.markdown("""
        <h3 style="color: #1976D2; margin-bottom: 20px;">📈 Track Your Daily Activity</h3>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            daily_steps = st.number_input(
                "👟 Daily Steps",
                min_value=0,
                max_value=100000,
                value=5000,
                step=100
            )
        
        with col2:
            sleep_hours = st.number_input(
                "😴 Sleep Hours",
                min_value=0.0,
                max_value=24.0,
                value=7.0,
                step=0.5
            )
        
        with col3:
            water_intake = st.number_input(
                "💧 Water Intake (liters)",
                min_value=0.0,
                max_value=20.0,
                value=2.0,
                step=0.1
            )
        
        # Progress indicators
        st.markdown("""<div class="divider"></div>""", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            steps_percent = min(100, (daily_steps / 7000) * 100)
            st.metric("Steps Goal Progress", f"{steps_percent:.0f}%")
        with col2:
            sleep_percent = min(100, (sleep_hours / 8) * 100)
            st.metric("Sleep Goal Progress", f"{sleep_percent:.0f}%")
        with col3:
            water_percent = min(100, (water_intake / 2.5) * 100)
            st.metric("Water Goal Progress", f"{water_percent:.0f}%")
        
        daily_metrics = {
            "daily_steps": daily_steps,
            "sleep_hours": sleep_hours,
            "water_intake": water_intake
        }
    
    # Submit button
    st.markdown("""<div class="divider"></div>""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        if st.button("💾 Save Health Data", use_container_width=True, type="primary"):
            # Validate data
            is_valid, error, _ = st.session_state.collector.collect_userinfo(
                user_info["age"],
                user_info["gender"],
                user_info["height"],
                user_info["weight"],
                user_info["medical_conditions"]
            )
            
            if is_valid:
                is_valid, error, _ = st.session_state.collector.collect_daily_metrics(
                    daily_metrics["daily_steps"],
                    daily_metrics["sleep_hours"],
                    daily_metrics["water_intake"]
                )
            
            if is_valid:
                # Create complete record
                health_record = st.session_state.collector.create_health_record(
                    {
                        "age": user_info["age"],
                        "gender": user_info["gender"],
                        "height_cm": user_info["height"],
                        "weight_kg": user_info["weight"],
                        "medical_conditions": user_info["medical_conditions"] or "None"
                    },
                    {
                        "daily_steps": daily_metrics["daily_steps"],
                        "sleep_hours": daily_metrics["sleep_hours"],
                        "water_intake_liters": daily_metrics["water_intake"]
                    }
                )
                
                # Save to storage
                if st.session_state.storage.add_health_record(st.session_state.user_id, health_record):
                    st.success("✅ Health data saved successfully!", icon="✅")
                    st.balloons()
                else:
                    st.error("❌ Error saving health data", icon="❌")
            else:
                st.error(f"❌ Validation Error: {error}", icon="❌")
    
    with col2:
        if st.button("📊 View Summary", use_container_width=True):
            st.session_state.current_page = "Health Summary"
            st.rerun()
    
    with col3:
        if st.button("💡 Get Recommendations", use_container_width=True):
            st.session_state.current_page = "Recommendations"
            st.rerun()




def page_health_summary():
    """Page displaying comprehensive health summary with visualizations"""
    st.markdown("""
    <h2 class="section-header">📊 Your Health Dashboard</h2>
    """, unsafe_allow_html=True)
    
    if not st.session_state.user_id:
        st.error("Please enter a User ID on the Home page first")
        return
    
    st.markdown(f"""
    <div class="info-box">
        👤 <strong>User ID:</strong> <code>{st.session_state.user_id}</code>
    </div>
    """, unsafe_allow_html=True)
    
    # Get user records
    user_records = st.session_state.storage.get_user_records(st.session_state.user_id)
    
    if not user_records:
        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>No health data found.</strong> Please enter your health data first.
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Input Health Data"):
            st.session_state.current_page = "Input Health Data"
            st.rerun()
        return
    
    # Summarize records
    profile = HealthProfileSummarizer.summarize_from_records(user_records)
    
    if profile is None:
        st.error("Error summarizing health data")
        return
    
    # Save profile for future use
    st.session_state.storage.save_user_profile(st.session_state.user_id, profile)
    
    # ========== BASIC INFORMATION ==========
    st.markdown("""
    <h3 style="color: #2E7D32; margin-bottom: 20px;">👤 Your Profile</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.metric("👤 Age", f"{profile['age']} years", delta=None)
    with col2:
        st.metric("⚖️ Weight", f"{profile['weight_kg']} kg", delta=None)
    with col3:
        st.metric("📏 Height", f"{profile['height_cm']} cm", delta=None)
    with col4:
        st.metric("👥 Gender", profile['gender'], delta=None)
    
    if profile.get("medical_conditions", "None") != "None":
        st.markdown(f"""
        <div class="warning-box">
            🏥 <strong>Medical Conditions:</strong> {profile['medical_conditions']}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ========== HEALTH METRICS ==========
    st.markdown("""
    <h3 style="color: #2E7D32; margin-bottom: 20px;">📈 Health Metrics</h3>
    """, unsafe_allow_html=True)
    
    metric_col1, metric_col2, metric_col3 = st.columns(3, gap="large")
    
    with metric_col1:
        st.markdown(create_metric_card(
            "BMI",
            f"{profile['bmi']}",
            "",
            profile['bmi_category'],
            "⚖️"
        ), unsafe_allow_html=True)
        
        st.markdown(create_metric_card(
            "Avg Daily Steps",
            f"{int(profile['average_steps']):,}",
            "steps",
            "Good" if profile['activity_level'] in ["Good", "Excellent"] else "Needs Work",
            "👟"
        ), unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown(create_metric_card(
            "Sleep Average",
            f"{profile['average_sleep_hours']}",
            "hours",
            profile['sleep_category'],
            "😴"
        ), unsafe_allow_html=True)
        
        st.markdown(create_metric_card(
            "Days Tracked",
            f"{profile['days_tracked']}",
            "days",
            "Excellent",
            "📅"
        ), unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown(create_metric_card(
            "Water Intake",
            f"{profile['average_water_intake']}",
            "liters",
            profile['hydration_level'],
            "💧"
        ), unsafe_allow_html=True)
        
        st.markdown(create_metric_card(
            "Activity Level",
            profile['activity_level'],
            "",
            "Good",
            "🏃"
        ), unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ========== CHARTS & VISUALIZATIONS ==========
    st.markdown("""
    <h3 style="color: #2E7D32; margin-bottom: 20px;">📊 Trends & Analysis</h3>
    """, unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2, gap="medium")
    
    with chart_col1:
        steps_fig = create_plotly_steps_chart(user_records)
        if steps_fig:
            st.plotly_chart(steps_fig, use_container_width=True)
        else:
            st.info("No steps data available")
    
    with chart_col2:
        sleep_fig = create_plotly_sleep_chart(user_records)
        if sleep_fig:
            st.plotly_chart(sleep_fig, use_container_width=True)
        else:
            st.info("No sleep data available")
    
    water_fig = create_water_intake_chart(user_records)
    if water_fig:
        st.plotly_chart(water_fig, use_container_width=True)
    else:
        st.info("No water intake data available")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ========== HEALTH RISKS ==========
    st.markdown("""
    <h3 style="color: #2E7D32; margin-bottom: 20px;">⚠️ Health Indicators</h3>
    """, unsafe_allow_html=True)
    
    if profile.get("health_risks"):
        for risk in profile["health_risks"]:
            st.markdown(f"""
            <div class="danger-box">
                ⚠️ {risk}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
            ✅ <strong>No major health risks identified!</strong> Keep up the good work!
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ========== NAVIGATION ==========
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        if st.button("📥 Add New Data", use_container_width=True):
            st.session_state.current_page = "Input Health Data"
            st.rerun()
    with col2:
        if st.button("💡 Get Recommendations", use_container_width=True):
            st.session_state.current_page = "Recommendations"
            st.rerun()
    with col3:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()




def page_recommendations():
    """Page displaying personalized recommendations with enhanced UI"""
    st.markdown("""
    <h2 class="section-header">💡 Personalized Health Recommendations</h2>
    """, unsafe_allow_html=True)
    
    if not st.session_state.user_id:
        st.error("Please enter a User ID on the Home page first")
        return
    
    st.markdown(f"""
    <div class="info-box">
        👤 <strong>User ID:</strong> <code>{st.session_state.user_id}</code>
    </div>
    """, unsafe_allow_html=True)
    
    # Get or generate profile
    user_records = st.session_state.storage.get_user_records(st.session_state.user_id)
    
    if not user_records:
        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>No health data found.</strong> Please enter your health data first.
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Input Health Data"):
            st.session_state.current_page = "Input Health Data"
            st.rerun()
        return
    
    # Summarize records
    profile = HealthProfileSummarizer.summarize_from_records(user_records)
    
    if profile is None:
        st.error("Error generating recommendations")
        return
    
    # Generate recommendations
    recommendations = RecommendationEngine.generate_comprehensive_recommendations(profile)
    
    # Display recommendations in tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏃 Exercise",
        "🥗 Diet",
        "😴 Sleep",
        "💧 Hydration",
        "⚠️ Health Alerts"
    ])
    
    with tab1:
        st.markdown("""
        <h3 style="color: #2E7D32; margin-bottom: 20px;">🏃 Exercise & Activity Recommendations</h3>
        """, unsafe_allow_html=True)
        st.markdown(f"**Your Activity Level:** `{profile['activity_level']}`", unsafe_allow_html=True)
        st.markdown(f"**Average Daily Steps:** `{int(profile['average_steps']):,} steps`", unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        for i, recommendation in enumerate(recommendations["exercise"], 1):
            st.markdown(f"""
            <div class="metric-card">
                <strong>{i}. {recommendation}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <h3 style="color: #2E7D32; margin-bottom: 20px;">🥗 Diet & Nutrition Recommendations</h3>
        """, unsafe_allow_html=True)
        st.markdown(f"**BMI Category:** `{profile['bmi_category']}`", unsafe_allow_html=True)
        st.markdown(f"**Your BMI:** `{profile['bmi']}`", unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        for i, recommendation in enumerate(recommendations["diet"], 1):
            st.markdown(f"""
            <div class="metric-card">
                <strong>{i}. {recommendation}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <h3 style="color: #2E7D32; margin-bottom: 20px;">😴 Sleep Recommendations</h3>
        """, unsafe_allow_html=True)
        st.markdown(f"**Sleep Category:** `{profile['sleep_category']}`", unsafe_allow_html=True)
        st.markdown(f"**Average Sleep:** `{profile['average_sleep_hours']} hours`", unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        for i, recommendation in enumerate(recommendations["sleep"], 1):
            st.markdown(f"""
            <div class="metric-card">
                <strong>{i}. {recommendation}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("""
        <h3 style="color: #2E7D32; margin-bottom: 20px;">💧 Hydration Recommendations</h3>
        """, unsafe_allow_html=True)
        st.markdown(f"**Hydration Level:** `{profile['hydration_level']}`", unsafe_allow_html=True)
        st.markdown(f"**Average Water Intake:** `{profile['average_water_intake']} liters`", unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        for i, recommendation in enumerate(recommendations["hydration"], 1):
            st.markdown(f"""
            <div class="metric-card">
                <strong>{i}. {recommendation}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("""
        <h3 style="color: #2E7D32; margin-bottom: 20px;">⚠️ Health Alerts & Risk Indicators</h3>
        """, unsafe_allow_html=True)
        for alert in recommendations["health_alerts"]:
            if "✅" in alert:
                st.markdown(f"""
                <div class="success-box">
                    {alert}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="warning-box">
                    {alert}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        if st.button("📥 Add New Data", use_container_width=True):
            st.session_state.current_page = "Input Health Data"
            st.rerun()
    with col2:
        if st.button("📊 View Summary", use_container_width=True):
            st.session_state.current_page = "Health Summary"
            st.rerun()
    with col3:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()




def page_data_management():
    """Page for managing user data with enhanced UI"""
    st.markdown("""
    <h2 class="section-header">⚙️ Data Management</h2>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <h3 style="color: #2E7D32; margin-bottom: 20px;">User Data Management</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        user_id_to_manage = st.text_input("👤 Enter User ID to manage", placeholder="e.g., john_doe")
    
    with col2:
        action = st.selectbox("📋 Action", ["View Records", "Delete Data"])
    
    if st.button("Execute", type="primary", use_container_width=False):
        if not user_id_to_manage.strip():
            st.error("Please enter a User ID")
        elif action == "View Records":
            records = st.session_state.storage.get_user_records(user_id_to_manage)
            if records:
                st.success(f"✅ Found {len(records)} records for {user_id_to_manage}")
                for i, record in enumerate(records, 1):
                    with st.expander(f"Record {i} - {record.get('timestamp', 'N/A')[:10]}"):
                        st.json(record.get("data", record))
            else:
                st.info(f"ℹ️ No records found for {user_id_to_manage}")
        
        elif action == "Delete Data":
            st.warning(f"⚠️ You are about to delete all data for {user_id_to_manage}")
            col_delete, col_cancel = st.columns(2)
            with col_delete:
                if st.button("🗑️ Confirm Delete (This cannot be undone)", type="secondary"):
                    if st.session_state.storage.delete_user_data(user_id_to_manage):
                        st.success(f"✅ All data for {user_id_to_manage} has been deleted")
                    else:
                        st.error("❌ Error deleting data")




def main():
    """Main application flow with professional UI"""
    initialize_session_state()
    
    # Display professional header
    display_professional_header()
    
    # Sidebar navigation with professional styling
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-container">
            <h3 style="margin-top: 0;">🧭 Navigation</h3>
        </div>
        """, unsafe_allow_html=True)
        
        pages = {
            "🏠 Home": "Home",
            "📥 Input Health Data": "Input Health Data",
            "📊 Health Summary": "Health Summary",
            "💡 Recommendations": "Recommendations",
            "⚙️ Data Management": "Data Management"
        }
        
        for page_name, page_key in pages.items():
            if st.button(page_name, use_container_width=True, key=f"nav_{page_key}"):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("""<div style="margin: 30px 0; border-bottom: 2px solid rgba(255,255,255,0.2);"></div>""", unsafe_allow_html=True)
        
        # User session info
        if st.session_state.user_id:
            st.markdown(f"""
            <div class="user-info">
                <strong>👤 Current User</strong><br/>
                <code style="color: #FBC02D; font-weight: bold;">{st.session_state.user_id}</code>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user_id = None
                st.session_state.current_page = "Home"
                st.rerun()
        else:
            st.markdown("""
            <div class="user-info">
                <em>👤 Not logged in</em>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""<div style="margin: 30px 0;"></div>""", unsafe_allow_html=True)
        
        # App info
        st.markdown("""
        <div style="text-align: center; color: rgba(255,255,255,0.7); font-size: 0.85rem;">
            <p><strong>Health Coach AI</strong><br/>v2.0 - Professional Edition</p>
            <p>Built with ❤️ using Streamlit<br/>& AI Technology</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    if st.session_state.current_page == "Home":
        page_home()
    elif st.session_state.current_page == "Input Health Data":
        page_input_health_data()
    elif st.session_state.current_page == "Health Summary":
        page_health_summary()
    elif st.session_state.current_page == "Recommendations":
        page_recommendations()
    elif st.session_state.current_page == "Data Management":
        page_data_management()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2026 Personal Health Coach AI | Built with Streamlit, Pandas, Plotly & NumPy</p>
        <p style="font-size: 0.75rem;">Privacy-focused | Local storage | No cloud data</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
