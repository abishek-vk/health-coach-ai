"""
theme_manager.py - Advanced Theme Management System with Persistence
Handles light/dark theme switching, persistence, and modular color schemes
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, Literal


class ThemeManager:
    """Advanced theme manager with local persistence and dynamic switching"""
    
    # Theme Color Palettes - Professional Edition
    LIGHT_THEME = {
        "name": "Light",
        "primary": "#1B7426",
        "secondary": "#0D47A1",
        "accent": "#E67E22",
        "success": "#27AE60",
        "warning": "#F39C12",
        "danger": "#E74C3C",
        "info": "#3498DB",
        "bg_main": "#F8FAFC",
        "bg_secondary": "#FFFFFF",
        "bg_tertiary": "#F1F5F9",
        "text_primary": "#1A202C",
        "text_secondary": "#718096",
        "text_muted": "#A0AEC0",
        "border": "#E2E8F0",
        "shadow": "rgba(0,0,0,0.08)",
        "chart_bg": "#FFFFFF",
        "card_hover": "#F7FAFC",
        "header_gradient_start": "#1B7426",
        "header_gradient_end": "#0D47A1",
        "input_focus_shadow": "rgba(27, 116, 38, 0.1)",
        "button_hover": "rgba(0,0,0,0.05)",
    }
    
    DARK_THEME = {
        "name": "Dark",
        "primary": "#52C77E",
        "secondary": "#64B5F6",
        "accent": "#FFB74D",
        "success": "#66BB6A",
        "warning": "#FDD835",
        "danger": "#EF5350",
        "info": "#42A5F5",
        "bg_main": "#0F1419",
        "bg_secondary": "#1E1E2E",
        "bg_tertiary": "#2A2A3E",
        "text_primary": "#E8EAED",
        "text_secondary": "#B0B0B0",
        "text_muted": "#808080",
        "border": "#404050",
        "shadow": "rgba(0,0,0,0.3)",
        "chart_bg": "#161B22",
        "card_hover": "#2C2C3C",
        "header_gradient_start": "#0D5F2F",
        "header_gradient_end": "#003DA5",
        "input_focus_shadow": "rgba(82, 199, 126, 0.15)",
        "button_hover": "rgba(255,255,255,0.1)",
    }

    # Modern Professional Theme
    MODERN_THEME = {
        "name": "Modern",
        "primary": "#6366F1",
        "secondary": "#EC4899",
        "accent": "#F59E0B",
        "success": "#10B981",
        "warning": "#FBBF24",
        "danger": "#F87171",
        "info": "#06B6D4",
        "bg_main": "#F9FAFB",
        "bg_secondary": "#FFFFFF",
        "bg_tertiary": "#F3F4F6",
        "text_primary": "#111827",
        "text_secondary": "#6B7280",
        "text_muted": "#9CA3AF",
        "border": "#E5E7EB",
        "shadow": "rgba(0,0,0,0.06)",
        "chart_bg": "#FFFFFF",
        "card_hover": "#F9FAFB",
        "header_gradient_start": "#6366F1",
        "header_gradient_end": "#EC4899",
        "input_focus_shadow": "rgba(99, 102, 241, 0.1)",
        "button_hover": "rgba(0,0,0,0.04)",
    }

    # Nature-inspired Theme
    NATURE_THEME = {
        "name": "Nature",
        "primary": "#059669",
        "secondary": "#0891B2",
        "accent": "#D97706",
        "success": "#16A34A",
        "warning": "#CA8A04",
        "danger": "#DC2626",
        "info": "#0284C7",
        "bg_main": "#F8FAFC",
        "bg_secondary": "#FFFFFF",
        "bg_tertiary": "#F0FDF4",
        "text_primary": "#1B4332",
        "text_secondary": "#52796F",
        "text_muted": "#95B8B1",
        "border": "#D1FAE5",
        "shadow": "rgba(5, 150, 105, 0.08)",
        "chart_bg": "#F0FDF4",
        "card_hover": "#F0FDF4",
        "header_gradient_start": "#065F46",
        "header_gradient_end": "#164E63",
        "input_focus_shadow": "rgba(5, 150, 105, 0.15)",
        "button_hover": "rgba(5, 150, 105, 0.05)",
    }
    
    # Themes dictionary
    THEMES = {
        "light": LIGHT_THEME,
        "dark": DARK_THEME,
        "modern": MODERN_THEME,
        "nature": NATURE_THEME,
    }
    
    def __init__(self, theme_file: str = "data/theme_preference.json"):
        """
        Initialize theme manager
        
        Args:
            theme_file: Path to store theme preference
        """
        self.theme_file = theme_file
        self.current_theme_name = self._load_theme_preference()
        self.colors = self.THEMES[self.current_theme_name].copy()
    
    def _load_theme_preference(self) -> str:
        """Load user's theme preference from file, default to light"""
        try:
            if os.path.exists(self.theme_file):
                with open(self.theme_file, 'r') as f:
                    data = json.load(f)
                    theme_name = data.get("theme", "light")
                    if theme_name in self.THEMES:
                        return theme_name
        except Exception as e:
            print(f"⚠️ Error loading theme preference: {e}")
        return "light"
    
    def save_theme_preference(self, theme_name: str) -> bool:
        """
        Save user's theme preference to file
        
        Args:
            theme_name: Theme name to save ("light" or "dark")
            
        Returns:
            True if save successful, False otherwise
        """
        if theme_name not in self.THEMES:
            return False
        
        try:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(self.theme_file) or ".", exist_ok=True)
            
            with open(self.theme_file, 'w') as f:
                json.dump({"theme": theme_name}, f, indent=2)
            return True
        except Exception as e:
            print(f"⚠️ Error saving theme preference: {e}")
            return False
    
    def set_theme(self, theme_name: str) -> bool:
        """
        Set active theme and persist preference
        
        Args:
            theme_name: Theme name to set
            
        Returns:
            True if successful
        """
        if theme_name not in self.THEMES:
            return False
        
        self.current_theme_name = theme_name
        self.colors = self.THEMES[theme_name].copy()
        return self.save_theme_preference(theme_name)
    
    def get_theme_name(self) -> str:
        """Get current theme name"""
        return self.current_theme_name
    
    def is_dark_mode(self) -> bool:
        """Check if dark mode is active"""
        return self.current_theme_name == "dark"
    
    def get_color(self, color_name: str) -> str:
        """
        Get a specific color from current theme
        
        Args:
            color_name: Name of the color
            
        Returns:
            Hex color code
        """
        return self.colors.get(color_name, "#000000")
    
    def get_colors(self) -> Dict[str, str]:
        """Get all colors from current theme"""
        return self.colors.copy()
    
    def get_plotly_template(self) -> str:
        """Get appropriate Plotly template based on current theme"""
        return "plotly_dark" if self.is_dark_mode() else "plotly"
    
    def get_available_themes(self) -> list:
        """Get list of available theme names"""
        return list(self.THEMES.keys())
    
    def apply_theme_to_plotly(self, fig):
        """
        Apply theme colors to Plotly figures
        
        Args:
            fig: Plotly figure object
            
        Returns:
            Updated figure with theme applied
        """
        fig.update_layout(
            template=self.get_plotly_template(),
            paper_bgcolor=self.get_color("bg_secondary"),
            plot_bgcolor=self.get_color("chart_bg"),
            font=dict(color=self.get_color("text_primary")),
            margin=dict(l=50, r=50, t=50, b=50),
        )
        return fig
    
    def get_theme_css(self) -> str:
        """
        Generate complete theme-aware CSS dynamically with professional styling
        
        Returns:
            CSS string with all theme variables and styles
        """
        colors = self.colors
        
        css = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
        
        * {{
            transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        }}
        
        html, body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: {colors['bg_main']};
            color: {colors['text_primary']};
        }}
        
        /* Root Colors - Dynamically set based on theme */
        :root {{
            --primary-color: {colors['primary']};
            --secondary-color: {colors['secondary']};
            --accent-color: {colors['accent']};
            --success-color: {colors['success']};
            --warning-color: {colors['warning']};
            --danger-color: {colors['danger']};
            --info-color: {colors['info']};
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
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}

        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] .main,
        [data-testid="stAppViewBlockContainer"] {{
            background-color: {colors['bg_main']} !important;
            color: {colors['text_primary']} !important;
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}
        
        /* Professional Header with Enhanced Design */
        .header-container {{
            background: linear-gradient(135deg, {colors['header_gradient_start']} 0%, {colors['header_gradient_end']} 100%);
            padding: 60px 50px;
            border-radius: 20px;
            color: white;
            margin-bottom: 50px;
            box-shadow: 0 15px 35px {colors['shadow']};
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            overflow: hidden;
        }}
        
        .header-container::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.05); opacity: 0.8; }}
        }}
        
        .header-title {{
            font-size: 3.2rem;
            font-weight: 800;
            margin: 0;
            color: white;
            letter-spacing: -0.8px;
            position: relative;
            z-index: 1;
        }}
        
        .header-subtitle {{
            font-size: 1.1rem;
            font-weight: 400;
            margin-top: 16px;
            opacity: 0.95;
            color: white;
            line-height: 1.7;
            position: relative;
            z-index: 1;
        }}
        
        /* Enhanced Card Styling */
        .metric-card {{
            background: {colors['bg_secondary']};
            padding: 32px;
            border-radius: 16px;
            margin: 16px 0;
            border-left: 5px solid {colors['primary']};
            box-shadow: 0 2px 8px {colors['shadow']};
            border: 1px solid {colors['border']};
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            color: {colors['text_primary']};
        }}
        
        .metric-card:hover {{
            box-shadow: 0 12px 32px {colors['shadow']};
            transform: translateY(-4px);
            background-color: {colors['card_hover']};
            border-color: {colors['primary']};
        }}
        
        .metric-card-success {{
            border-left-color: {colors['success']};
        }}
        
        .metric-card-success:hover {{
            box-shadow: 0 12px 32px {self.hex_to_rgba(colors['success'], 0.2)};
        }}
        
        .metric-card-info {{
            border-left-color: {colors['secondary']};
        }}
        
        .metric-card-info:hover {{
            box-shadow: 0 12px 32px {self.hex_to_rgba(colors['secondary'], 0.2)};
        }}
        
        .metric-card-warning {{
            border-left-color: {colors['accent']};
        }}
        
        .metric-card-warning:hover {{
            box-shadow: 0 12px 32px {self.hex_to_rgba(colors['accent'], 0.2)};
        }}
        
        .metric-value {{
            font-size: 2.5rem;
            font-weight: 800;
            color: {colors['primary']};
            margin: 14px 0 10px 0;
            letter-spacing: -1.2px;
            line-height: 1.1;
        }}
        
        .metric-label {{
            font-size: 0.85rem;
            color: {colors['text_secondary']};
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin: 0;
        }}
        
        .metric-unit {{
            font-size: 0.82rem;
            color: {colors['text_secondary']};
            margin-left: 6px;
            opacity: 0.75;
            font-weight: 500;
        }}
        
        /* Enhanced Alert Boxes with improved styling */
        .info-box {{
            background: linear-gradient(135deg, {self.hex_to_rgba(colors['info'], 0.08)} 0%, {self.hex_to_rgba(colors['secondary'], 0.04)} 100%);
            border-left: 4px solid {colors['info']};
            border-radius: 12px;
            padding: 20px 24px;
            margin: 18px 0;
            color: {colors['text_primary']};
            font-size: 0.95rem;
            line-height: 1.7;
            transition: all 0.3s ease;
            border: 1px solid {self.hex_to_rgba(colors['info'], 0.2)};
        }}
        
        .info-box:hover {{
            box-shadow: 0 4px 16px {self.hex_to_rgba(colors['info'], 0.15)};
            border-left-width: 5px;
        }}
        
        .warning-box {{
            background: linear-gradient(135deg, {self.hex_to_rgba(colors['warning'], 0.1)} 0%, {self.hex_to_rgba(colors['accent'], 0.04)} 100%);
            border-left: 4px solid {colors['warning']};
            border-radius: 12px;
            padding: 20px 24px;
            margin: 18px 0;
            color: {colors['text_primary']};
            font-size: 0.95rem;
            line-height: 1.7;
            transition: all 0.3s ease;
            border: 1px solid {self.hex_to_rgba(colors['warning'], 0.2)};
        }}
        
        .warning-box:hover {{
            box-shadow: 0 4px 16px {self.hex_to_rgba(colors['warning'], 0.15)};
            border-left-width: 5px;
        }}
        
        .success-box {{
            background: linear-gradient(135deg, {self.hex_to_rgba(colors['success'], 0.1)} 0%, {self.hex_to_rgba(colors['info'], 0.04)} 100%);
            border-left: 4px solid {colors['success']};
            border-radius: 12px;
            padding: 20px 24px;
            margin: 18px 0;
            color: {colors['text_primary']};
            font-size: 0.95rem;
            line-height: 1.7;
            transition: all 0.3s ease;
            border: 1px solid {self.hex_to_rgba(colors['success'], 0.2)};
        }}
        
        .success-box:hover {{
            box-shadow: 0 4px 16px {self.hex_to_rgba(colors['success'], 0.15)};
            border-left-width: 5px;
        }}
        
        .danger-box {{
            background: linear-gradient(135deg, {self.hex_to_rgba(colors['danger'], 0.1)} 0%, {self.hex_to_rgba(colors['warning'], 0.04)} 100%);
            border-left: 4px solid {colors['danger']};
            border-radius: 12px;
            padding: 20px 24px;
            margin: 18px 0;
            color: {colors['text_primary']};
            font-size: 0.95rem;
            line-height: 1.7;
            transition: all 0.3s ease;
            border: 1px solid {self.hex_to_rgba(colors['danger'], 0.2)};
        }}
        
        .danger-box:hover {{
            box-shadow: 0 4px 16px {self.hex_to_rgba(colors['danger'], 0.15)};
            border-left-width: 5px;
        }}
        
        /* Section Headers with enhanced styling */
        .section-header {{
            font-size: 2.2rem;
            font-weight: 800;
            color: {colors['primary']};
            margin: 48px 0 28px 0;
            padding-bottom: 20px;
            border-bottom: 3px solid {colors['primary']};
            letter-spacing: -0.5px;
        }}
        
        .subsection-header {{
            font-size: 1.35rem;
            font-weight: 700;
            color: {colors['primary']};
            margin: 28px 0 18px 0;
            letter-spacing: -0.3px;
        }}
        
        /* Professional Tab Styling */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: transparent;
            border-radius: 0;
            padding: 0;
            border-bottom: 2px solid {colors['border']};
            gap: 0;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: transparent;
            border-radius: 8px 8px 0 0;
            color: {colors['text_secondary']};
            border-bottom: 3px solid transparent;
            border: 1px solid transparent;
            padding: 14px 28px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            color: {colors['primary']};
            background-color: {colors['button_hover']};
        }}
        
        .stTabs [aria-selected="true"] {{
            border-bottom-color: {colors['primary']} !important;
            color: {colors['primary']} !important;
            border-bottom: 3px solid {colors['primary']};
            font-weight: 700;
        }}
        
        /* Professional Buttons */
        .stButton > button {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            padding: 12px 28px !important;
            font-size: 0.95rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px {self.hex_to_rgba(colors['primary'], 0.3)} !important;
            letter-spacing: 0.3px !important;
        }}
        
        .stButton > button:hover {{
            box-shadow: 0 8px 25px {self.hex_to_rgba(colors['primary'], 0.4)} !important;
            transform: translateY(-2px) !important;
        }}
        
        .stButton > button:active {{
            transform: translateY(0) !important;
        }}
        
        /* Enhanced Input Fields */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input,
        .stTextArea > div > div > textarea {{
            background-color: {colors['bg_secondary']} !important;
            color: {colors['text_primary']} !important;
            border: 1.5px solid {colors['border']} !important;
            border-radius: 10px !important;
            padding: 14px 16px !important;
            font-size: 0.95rem !important;
            transition: all 0.2s ease !important;
            font-family: 'Inter', sans-serif !important;
        }}

        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stNumberInput"] input,
        [data-baseweb="select"] > div,
        [data-baseweb="select"] input,
        [data-baseweb="select"] span,
        [data-baseweb="base-input"] > div,
        [data-baseweb="input"] > div {{
            background-color: {colors['bg_secondary']} !important;
            color: {colors['text_primary']} !important;
            border-color: {colors['border']} !important;
        }}

        [data-testid="stNumberInput"] button,
        [data-baseweb="select"] svg {{
            color: {colors['text_secondary']} !important;
            fill: {colors['text_secondary']} !important;
        }}
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stNumberInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: {colors['primary']} !important;
            box-shadow: 0 0 0 3px {colors['input_focus_shadow']} !important;
            background-color: {colors['card_hover']} !important;
        }}

        [data-baseweb="select"] > div:focus-within,
        [data-baseweb="base-input"] > div:focus-within,
        [data-baseweb="input"] > div:focus-within {{
            border-color: {colors['primary']} !important;
            box-shadow: 0 0 0 3px {colors['input_focus_shadow']} !important;
        }}
        
        /* Professional Labels */
        .stLabel > label {{
            font-weight: 600 !important;
            color: {colors['text_primary']} !important;
            font-size: 0.9rem !important;
            margin-bottom: 10px !important;
            letter-spacing: 0.2px !important;
        }}

        [data-testid="stWidgetLabel"] p,
        [data-testid="stMetricLabel"] p {{
            color: {colors['text_secondary']} !important;
            font-weight: 600 !important;
        }}

        [data-testid="stMetric"] {{
            background-color: {colors['bg_secondary']} !important;
            border: 1px solid {colors['border']} !important;
            border-radius: 12px !important;
            padding: 12px 14px !important;
        }}

        [data-testid="stMetricValue"] {{
            color: {colors['text_primary']} !important;
        }}

        .stAlert {{
            background-color: {colors['bg_secondary']} !important;
            border-color: {colors['border']} !important;
            color: {colors['text_primary']} !important;
        }}
        
        /* Divider */
        .divider {{
            margin: 36px 0;
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, {colors['border']} 10%, {colors['border']} 90%, transparent);
        }}
        
        /* Theme Toggle Button */
        .theme-toggle {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px {self.hex_to_rgba(colors['primary'], 0.3)};
            margin: 10px 0;
            width: 100%;
            font-size: 0.95rem;
        }}
        
        .theme-toggle:hover {{
            box-shadow: 0 6px 25px {self.hex_to_rgba(colors['primary'], 0.4)};
            transform: translateY(-2px);
        }}
        
        .theme-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: {colors['primary']};
            margin-right: 8px;
            vertical-align: middle;
            animation: fadeInOut 2s ease-in-out infinite;
        }}
        
        @keyframes fadeInOut {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}
        
        /* Professional Sidebar */
        [data-testid="stSidebar"] {{
            background: {colors['bg_secondary']};
            border-right: 1px solid {colors['border']};
        }}
        
        .sidebar-container {{
            background: linear-gradient(180deg, {colors['header_gradient_start']} 0%, {colors['header_gradient_end']} 100%);
            color: white;
            padding: 24px;
            border-radius: 14px;
            margin-bottom: 24px;
            box-shadow: 0 8px 24px {self.hex_to_rgba(colors['primary'], 0.25)};
        }}
        
        .sidebar-container h3 {{
            color: white;
            margin: 0 0 12px 0;
            font-weight: 700;
            font-size: 1.1rem;
            letter-spacing: -0.3px;
        }}
        
        .user-info {{
            background-color: rgba(255,255,255,0.15);
            padding: 16px;
            border-radius: 12px;
            margin: 20px 0;
            border-left: 4px solid {colors['accent']};
            border: 1px solid rgba(255,255,255,0.2);
            color: white;
            backdrop-filter: blur(10px);
        }}
        
        .user-info strong {{
            color: white;
            font-weight: 700;
        }}
        
        .user-info code {{
            color: {colors['accent']};
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
            background: rgba(255,255,255,0.1);
            padding: 2px 6px;
            border-radius: 4px;
        }}
        
        /* Chart Container */
        .chart-container {{
            background-color: {colors['bg_secondary']};
            padding: 28px;
            border-radius: 16px;
            box-shadow: 0 4px 16px {colors['shadow']};
            margin: 24px 0;
            border: 1px solid {colors['border']};
            transition: all 0.3s ease;
        }}
        
        .chart-container:hover {{
            box-shadow: 0 8px 32px {colors['shadow']};
            border-color: {colors['primary']};
        }}
        
        /* Professional Text Styling */
        h1, h2, h3, h4, h5, h6 {{
            color: {colors['primary']};
            font-weight: 800;
            letter-spacing: -0.5px;
            margin: 0;
        }}
        
        h1 {{ font-size: 2.5rem; }}
        h2 {{ font-size: 2rem; }}
        h3 {{ font-size: 1.5rem; }}
        h4 {{ font-size: 1.25rem; }}
        h5 {{ font-size: 1.1rem; }}
        h6 {{ font-size: 0.95rem; }}
        
        /* Code Styling */
        code {{
            background-color: {colors['bg_tertiary']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            padding: 3px 10px;
            color: {colors['text_primary']};
            font-family: 'JetBrains Mono', 'Monaco', monospace;
            font-size: 0.88rem;
            font-weight: 500;
        }}
        
        /* Streamlit Metric Box */
        .metric-box {{
            background-color: {colors['bg_secondary']};
            padding: 20px;
            border-radius: 12px;
            border: 1px solid {colors['border']};
            box-shadow: 0 2px 8px {colors['shadow']};
        }}
        
        /* Responsive adjustments */
        @media (max-width: 1024px) {{
            .header-container {{
                padding: 48px 40px;
            }}
            
            .header-title {{
                font-size: 2.8rem;
            }}
        }}
        
        @media (max-width: 768px) {{
            .header-title {{
                font-size: 2rem;
            }}
            
            .header-container {{
                padding: 40px 32px;
            }}
            
            .metric-card {{
                padding: 24px 28px;
            }}
            
            .metric-value {{
                font-size: 2rem;
            }}
            
            .metric-label {{
                font-size: 0.8rem;
            }}
            
            .section-header {{
                font-size: 1.8rem;
            }}
            
            .stButton > button {{
                padding: 10px 20px !important;
                font-size: 0.9rem !important;
            }}
        }}
        
        @media (max-width: 480px) {{
            .header-title {{
                font-size: 1.6rem;
            }}
            
            .header-container {{
                padding: 32px 24px;
            }}
            
            .section-header {{
                font-size: 1.5rem;
            }}
            
            .metric-card {{
                padding: 18px 20px;
            }}
            
            .metric-value {{
                font-size: 1.5rem;
            }}
        }}
        
        /* Smooth scrolling */
        html {{
            scroll-behavior: smooth;
        }}
        
        /* Selection styling */
        ::selection {{
            background-color: {self.hex_to_rgba(colors['primary'], 0.3)};
            color: {colors['text_primary']};
        }}
        </style>
        """
        return css
    @staticmethod
    def hex_to_rgba(hex_color: str, alpha: float = 0.15) -> str:
        """
        Convert hex color to rgba format
        
        Args:
            hex_color: Hex color code (e.g., '#FF0000')
            alpha: Alpha transparency (0-1)
            
        Returns:
            RGBA color string
        """
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgba({r}, {g}, {b}, {alpha})"
