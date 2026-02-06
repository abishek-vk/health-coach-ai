"""
main.py - Professional Streamlit Dashboard for Personal Health Coach AI
Interactive web interface with modern UI, charts, and data management
Theme-aware UI that automatically adapts to light/dark mode
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
# THEME MANAGEMENT SYSTEM
# ============================================================================
class ThemeManager:
    """Manages theme-aware colors and styling based on Streamlit's active theme"""
    
    def __init__(self):
        self.is_dark_mode = self._detect_theme()
        self.colors = self._get_color_palette()
    
    def _detect_theme(self):
        """Detect if dark mode is active in Streamlit"""
        try:
            return st.get_option("theme.base") == "dark"
        except:
            return False
    
    def _get_color_palette(self):
        """Return color palette based on current theme"""
        if self.is_dark_mode:
            return {
                "primary": "#4CAF50",
                "secondary": "#42A5F5",
                "accent": "#FF9800",
                "success": "#66BB6A",
                "warning": "#FDD835",
                "danger": "#EF5350",
                "bg_main": "#0E1117",
                "bg_secondary": "#262730",
                "bg_tertiary": "#3D3D4D",
                "text_primary": "#ECDDC8",
                "text_secondary": "#B0B0B0",
                "border": "#3D3D4D",
                "shadow": "rgba(0,0,0,0.5)",
                "chart_bg": "#1a1a2e",
                "card_hover": "#4a4a5e",
            }
        else:
            return {
                "primary": "#2E7D32",
                "secondary": "#1976D2",
                "accent": "#F57C00",
                "success": "#388E3C",
                "warning": "#FBC02D",
                "danger": "#D32F2F",
                "bg_main": "#F5F7FA",
                "bg_secondary": "#FFFFFF",
                "bg_tertiary": "#F5F5F5",
                "text_primary": "#212121",
                "text_secondary": "#757575",
                "border": "#E0E0E0",
                "shadow": "rgba(0,0,0,0.1)",
                "chart_bg": "#FFFFFF",
                "card_hover": "#F0F0F0",
            }
    
    def get_color(self, color_name):
        """Get a specific color from the palette"""
        return self.colors.get(color_name, "#000000")
    
    def get_plotly_template(self):
        """Get appropriate Plotly template based on theme"""
        return "plotly_dark" if self.is_dark_mode else "plotly"
    
    def apply_theme_to_plotly(self, fig):
        """Apply theme colors to Plotly figures"""
        fig.update_layout(
            template=self.get_plotly_template(),
            paper_bgcolor=self.get_color("bg_secondary"),
            plot_bgcolor=self.get_color("chart_bg"),
            font=dict(color=self.get_color("text_primary")),
            margin=dict(l=50, r=50, t=50, b=50),
        )
        return fig


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

# Initialize theme manager
theme = ThemeManager()

# ============================================================================
# DYNAMIC CSS STYLING - THEME AWARE
# ============================================================================
def generate_theme_css(theme):
    """Generate CSS dynamically based on current theme"""
    colors = theme.colors
    
    css = f"""
    <style>
    /* Root Colors - Dynamically set based on theme */
    :root {{
        --primary-color: {colors['primary']};
        --secondary-color: {colors['secondary']};
        --accent-color: {colors['accent']};
        --success-color: {colors['success']};
        --warning-color: {colors['warning']};
        --danger-color: {colors['danger']};
        --light-bg: {colors['bg_main']};
        --card-bg: {colors['bg_secondary']};
        --text-primary: {colors['text_primary']};
        --text-secondary: {colors['text_secondary']};
        --border-color: {colors['border']};
        --shadow-color: {colors['shadow']};
    }}
    
    /* Main Container */
    .main {{
        background-color: {colors['bg_main']};
        color: {colors['text_primary']};
    }}
    
    /* Professional Header */
    .header-container {{
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
        padding: 40px 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px {colors['shadow']};
        transition: all 0.3s ease;
    }}
    
    .header-title {{
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        color: white;
        text-shadow: 0 2px 4px {colors['shadow']};
    }}
    
    .header-subtitle {{
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: 10px;
        opacity: 0.95;
        color: white;
    }}
    
    /* Card Styling */
    .metric-card {{
        background: {colors['bg_secondary']};
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 5px solid {colors['primary']};
        box-shadow: 0 2px 8px {colors['shadow']};
        transition: all 0.3s ease;
        color: {colors['text_primary']};
    }}
    
    .metric-card:hover {{
        box-shadow: 0 6px 16px {colors['shadow']};
        transform: translateY(-2px);
        background-color: {colors['card_hover']};
    }}
    
    .metric-card-success {{
        border-left-color: {colors['success']};
    }}
    
    .metric-card-info {{
        border-left-color: {colors['secondary']};
    }}
    
    .metric-card-warning {{
        border-left-color: {colors['accent']};
    }}
    
    .metric-value {{
        font-size: 2.2rem;
        font-weight: 700;
        color: {colors['primary']};
        margin: 10px 0;
    }}
    
    .metric-label {{
        font-size: 0.95rem;
        color: {colors['text_secondary']};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .metric-unit {{
        font-size: 0.85rem;
        color: {colors['text_secondary']};
        margin-left: 5px;
        opacity: 0.7;
    }}
    
    /* Alert Boxes */
    .alert-box {{
        background-color: {colors['warning']};
        border-left: 5px solid {colors['accent']};
        padding: 18px;
        border-radius: 8px;
        margin: 15px 0;
        color: #333;
        font-size: 0.95rem;
        line-height: 1.6;
        transition: all 0.3s ease;
    }}
    
    .success-box {{
        background-color: {colors['success']};
        border-left: 5px solid {colors['success']};
        padding: 18px;
        border-radius: 8px;
        margin: 15px 0;
        color: white;
        font-size: 0.95rem;
        line-height: 1.6;
        transition: all 0.3s ease;
        opacity: 0.9;
    }}
    
    .danger-box {{
        background-color: {colors['danger']};
        border-left: 5px solid {colors['danger']};
        padding: 18px;
        border-radius: 8px;
        margin: 15px 0;
        color: white;
        font-size: 0.95rem;
        line-height: 1.6;
        transition: all 0.3s ease;
        opacity: 0.9;
    }}
    
    .info-box {{
        background-color: {colors['secondary']};
        border-left: 5px solid {colors['secondary']};
        padding: 18px;
        border-radius: 8px;
        margin: 15px 0;
        color: white;
        font-size: 0.95rem;
        line-height: 1.6;
        transition: all 0.3s ease;
        opacity: 0.9;
    }}
    
    /* Section Headers */
    .section-header {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {colors['primary']};
        margin: 30px 0 20px 0;
        padding-bottom: 15px;
        border-bottom: 3px solid {colors['primary']};
        transition: all 0.3s ease;
    }}
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {colors['bg_main']};
        border-radius: 8px;
        padding: 5px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: {colors['bg_secondary']};
        border-radius: 6px;
        margin: 5px;
        color: {colors['text_primary']};
        transition: all 0.3s ease;
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {colors['primary']} !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover {{
        background-color: {colors['secondary']} !important;
        box-shadow: 0 4px 12px {colors['shadow']} !important;
    }}
    
    /* Text Color Adjustments */
    p, span, label {{
        color: {colors['text_primary']};
        transition: color 0.3s ease;
    }}
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {{
        background-color: {colors['bg_secondary']} !important;
        color: {colors['text_primary']} !important;
        border-color: {colors['border']} !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {colors['primary']} !important;
        box-shadow: 0 0 0 3px {colors['primary']}44 !important;
    }}
    
    /* Divider */
    .divider {{
        margin: 30px 0;
        border-bottom: 2px solid {colors['border']};
    }}
    
    /* Progress Bar */
    .progress-container {{
        margin: 20px 0;
    }}
    
    .progress-bar {{
        background-color: {colors['bg_tertiary']};
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
    }}
    
    .progress-bar-fill {{
        background: linear-gradient(90deg, {colors['primary']}, {colors['success']});
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }}
    
    /* Sidebar */
    .sidebar-container {{
        background: linear-gradient(180deg, {colors['primary']} 0%, {colors['secondary']} 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }}
    
    .user-info {{
        background-color: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid {colors['warning']};
    }}
    
    /* Badge */
    .badge {{
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 5px 5px 0;
    }}
    
    .badge-success {{
        background-color: {colors['success']};
        color: white;
    }}
    
    .badge-warning {{
        background-color: {colors['warning']};
        color: #333;
    }}
    
    .badge-danger {{
        background-color: {colors['danger']};
        color: white;
    }}
    
    .badge-info {{
        background-color: {colors['secondary']};
        color: white;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        color: {colors['text_secondary']};
        font-size: 0.85rem;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid {colors['border']};
    }}
    
    /* Chart Container */
    .chart-container {{
        background-color: {colors['bg_secondary']};
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px {colors['shadow']};
        margin: 20px 0;
    }}
    
    /* Responsive adjustments */
    @media (max-width: 768px) {{
        .header-title {{
            font-size: 2rem;
        }}
        
        .metric-card {{
            margin: 10px 0;
        }}
    }}
    </style>
    """
    return css

# Apply dynamic theme CSS
st.markdown(generate_theme_css(theme), unsafe_allow_html=True)


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
    """Display professional gradient header - Theme aware"""
    primary = theme.get_color("primary")
    secondary = theme.get_color("secondary")
    text_color = "white"
    
    st.markdown(f"""
    <div class="header-container">
        <h1 class="header-title">🏥 Health Coach AI</h1>
        <p class="header-subtitle">Your Intelligent Personal Health & Wellness Companion</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar_styling():
    """Generate theme-aware sidebar styling HTML"""
    primary = theme.get_color("primary")
    secondary = theme.get_color("secondary")
    bg_secondary = theme.get_color("bg_secondary")
    text_primary = theme.get_color("text_primary")
    
    return f"""
    <style>
    .sidebar-container {{
        background: linear-gradient(180deg, {primary} 0%, {secondary} 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px {theme.get_color('shadow')};
    }}
    
    .sidebar-container h3 {{
        color: white;
        margin: 0;
    }}
    
    .user-info {{
        background-color: rgba(255,255,255,0.15);
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
        border-left: 4px solid {theme.get_color('warning')};
        color: white;
    }}
    
    .user-info strong {{
        color: white;
    }}
    
    .user-info code {{
        color: {theme.get_color('warning')};
        font-weight: bold;
    }}
    </style>
    """


def create_plotly_steps_chart(user_records):
    """Create interactive Plotly chart for daily steps - Theme aware"""
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
        line=dict(color=theme.get_color("primary"), width=3),
        marker=dict(size=8, color=theme.get_color("primary"), symbol="circle"),
        fill="tozeroy",
        fillcolor=theme.get_color("primary") + "1A"
    ))
    
    fig.add_hline(y=7000, line_dash="dash", line_color=theme.get_color("accent"), 
                  annotation_text="Daily Goal", annotation_position="right")
    
    fig.update_layout(
        title="Daily Steps Trend",
        xaxis_title="Date",
        yaxis_title="Steps",
        hovermode="x unified",
        height=400
    )
    
    # Apply theme to the figure
    theme.apply_theme_to_plotly(fig)
    
    return fig


def create_plotly_sleep_chart(user_records):
    """Create interactive Plotly chart for sleep hours - Theme aware"""
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
        line=dict(color=theme.get_color("secondary"), width=3),
        marker=dict(size=8, color=theme.get_color("secondary"), symbol="circle"),
        fill="tozeroy",
        fillcolor=theme.get_color("secondary") + "1A"
    ))
    
    fig.add_hline(y=8, line_dash="dash", line_color=theme.get_color("accent"),
                  annotation_text="Recommended", annotation_position="right")
    
    fig.update_layout(
        title="Sleep Hours Trend",
        xaxis_title="Date",
        yaxis_title="Hours",
        hovermode="x unified",
        height=400
    )
    
    # Apply theme to the figure
    theme.apply_theme_to_plotly(fig)
    
    return fig


def create_water_intake_chart(user_records):
    """Create interactive Plotly chart for water intake - Theme aware"""
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
            color=theme.get_color("success"),
            opacity=0.8
        )
    ))
    
    fig.add_hline(y=2, line_dash="dash", line_color=theme.get_color("accent"),
                  annotation_text="Daily Goal", annotation_position="right")
    
    fig.update_layout(
        title="Daily Water Intake",
        xaxis_title="Date",
        yaxis_title="Liters",
        height=400
    )
    
    # Apply theme to the figure
    theme.apply_theme_to_plotly(fig)
    
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
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: {theme.get_color('primary')}; margin-top: 0;">📋 How It Works</h3>
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
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: {theme.get_color('secondary')}; margin-top: 0;">✨ Key Features</h3>
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
    
    st.markdown(f"""
    <h3 style="color: {theme.get_color('primary')}; margin-bottom: 20px;">🚀 Get Started Today</h3>
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
        st.markdown(f"""
        <h3 style="color: {theme.get_color('secondary')}; margin-bottom: 20px;">📈 Track Your Daily Activity</h3>
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
    st.markdown(f"""
    <h3 style="color: {theme.get_color('primary')}; margin-bottom: 20px;">👤 Your Profile</h3>
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
    st.markdown(f"""
    <h3 style="color: {theme.get_color('primary')}; margin-bottom: 20px;">📈 Health Metrics</h3>
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
        st.markdown(f"""
        <h3 style="color: {theme.get_color('primary')}; margin-bottom: 20px;">🏃 Exercise & Activity Recommendations</h3>
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
        st.markdown(f"""
        <h3 style="color: {theme.get_color('primary')}; margin-bottom: 20px;">🥗 Diet & Nutrition Recommendations</h3>
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
        st.markdown(f"""
        <h3 style="color: {theme.get_color('primary')}; margin-bottom: 20px;">😴 Sleep Recommendations</h3>
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
        st.markdown(f"""
        <h3 style="color: {theme.get_color('primary')}; margin-bottom: 20px;">💧 Hydration Recommendations</h3>
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
        st.markdown(f"""
        <h3 style="color: {theme.get_color('primary')}; margin-bottom: 20px;">⚠️ Health Alerts & Risk Indicators</h3>
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
    
    st.markdown(f"""
    <h3 style="color: {theme.get_color('primary')}; margin-bottom: 20px;">User Data Management</h3>
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
    """Main application flow with professional UI - Theme aware"""
    initialize_session_state()
    
    # Display professional header
    display_professional_header()
    
    # Apply sidebar styling
    st.markdown(render_sidebar_styling(), unsafe_allow_html=True)
    
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
        
        st.markdown(f"""<div style="margin: 30px 0; border-bottom: 2px solid {theme.get_color('border')};"></div>""", unsafe_allow_html=True)
        
        # User session info
        if st.session_state.user_id:
            st.markdown(f"""
            <div class="user-info">
                <strong>👤 Current User</strong><br/>
                <code style="color: {theme.get_color('warning')}; font-weight: bold;">{st.session_state.user_id}</code>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user_id = None
                st.session_state.current_page = "Home"
                st.rerun()
        else:
            st.markdown(f"""
            <div class="user-info">
                <em>👤 Not logged in</em>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""<div style="margin: 30px 0;"></div>""", unsafe_allow_html=True)
        
        # App info
        st.markdown(f"""
        <div style="text-align: center; color: {theme.get_color('text_secondary')}; font-size: 0.85rem;">
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
    st.markdown(f"""
    <div class="footer">
        <p>© 2026 Personal Health Coach AI | Built with Streamlit, Pandas, Plotly & NumPy</p>
        <p style="font-size: 0.75rem;">Privacy-focused | Local storage | No cloud data</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
