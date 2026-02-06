# 🏥 Professional Health Coach AI - Quick Start Guide

## ✨ What's New in v2.0

Your Health Coach AI now features a **professional, modern interactive UI** with:

### 🎨 Design Enhancements
- **Gradient Header** - Beautiful gradient design with modern typography
- **Professional Color Scheme** - Green, blue, and orange theme for better visual hierarchy
- **Smooth Interactions** - Hover effects on cards and buttons
- **Responsive Layout** - Optimized for desktop and tablet viewing
- **Interactive Charts** - Plotly-powered visualizations with hover details

### 📊 New Features
- **Interactive Charts** - Line charts for steps & sleep, bar charts for water intake
- **Progress Indicators** - Visual progress bars showing goal completion
- **Metric Cards** - Beautiful cards with badges and status indicators
- **Enhanced Alerts** - Color-coded alerts (danger, warning, success, info)
- **Better Navigation** - Improved sidebar with user session info
- **Professional Typography** - Cleaner, more readable text hierarchy

### 🚀 Running the Application

#### Prerequisites
- Python 3.8 or higher
- All dependencies installed (pip install -r requirements.txt)

#### Start the Application

```bash
cd C:\Users\Abi Venkat\health-coach-ai
python -m streamlit run main.py
```

Or simply:
```bash
streamlit run main.py
```

The app will open automatically in your default browser at: `http://localhost:8501`

#### Browser Access
If it doesn't open automatically, visit: **http://localhost:8501**

### 📝 How to Use

1. **Home Page** - Create your user profile
   - Enter a User ID (e.g., `john_doe`, `user_001`)
   - Click "Start Tracking"

2. **Input Health Data** - Track your metrics
   - **Basic Info Tab** - Enter age, weight, height, gender, medical conditions
   - **Daily Metrics Tab** - Log steps, sleep hours, water intake
   - Click "Save Health Data"

3. **Health Summary** - View your analytics
   - See all your metrics in professional cards
   - Interactive charts showing trends over time
   - Health risk indicators

4. **Recommendations** - Get personalized advice
   - Exercise recommendations based on activity level
   - Diet recommendations based on BMI
   - Sleep optimization tips
   - Hydration guidance
   - Health alerts and risk indicators

5. **Data Management** - Manage your data
   - View all your historical records
   - Delete data if needed

### 🎯 Features by Page

#### Home Page
- Beautiful introduction with feature highlights
- Quick start section
- User login/session management

#### Input Health Data
- **Two-tab interface** for organized data entry
- Real-time progress indicators showing goal progress
- Visual feedback with progress bars
- Beautiful form inputs with better styling

#### Health Summary (Dashboard)
- Professional metric cards with color-coded badges
- **Interactive Plotly charts**:
  - Daily steps trend with goal line
  - Sleep hours trend with recommended line
  - Water intake bar chart with goal indicator
- Health risk indicators in color-coded boxes
- Compact profile information display

#### Recommendations
- **Five recommendation tabs**:
  - Exercise & Activity
  - Diet & Nutrition
  - Sleep Optimization
  - Hydration Guidance
  - Health Alerts
- Numbered recommendations in beautiful cards
- Color-coded alerts (green for good, orange for warning, red for risk)

#### Data Management
- View detailed health records
- Delete user data with confirmation
- Professional interface for data operations

### 🎨 UI Components

#### Colors
- **Primary Green** (#2E7D32) - Main actions and headers
- **Secondary Blue** (#1976D2) - Secondary actions
- **Accent Orange** (#F57C00) - Highlight and goals
- **Light Gray** (#F5F7FA) - Background
- **White** (#FFFFFF) - Cards and components

#### Boxes & Alerts
- ✅ **Success Box** - Green alert for positive information
- ⚠️ **Warning Box** - Yellow alert for caution items
- ❌ **Danger Box** - Red alert for risks
- ℹ️ **Info Box** - Blue alert for informational content

#### Badges
- Badge colors match alert types (success, warning, danger, info)
- Used to show categories and status

#### Charts
- Interactive Plotly charts with hover tooltips
- Goal lines shown with dashed orange lines
- Responsive sizing with light background

### 💡 Tips & Tricks

1. **Best Results** - Log data daily for accurate trends and insights
2. **Goals** - Default goals are:
   - Steps: 7,000 per day
   - Sleep: 8 hours per night
   - Water: 2.5 liters per day
3. **Mobile** - Works on tablets but optimized for desktop
4. **Data Privacy** - All data stored locally in JSON files
5. **Performance** - Charts load faster with more data points

### 🔧 Customization

To change default goals or styling, edit these in `main.py`:

```python
# Lines with goal values in chart creation functions
fig.add_hline(y=7000, ...)  # Daily steps goal
fig.add_hline(y=8, ...)      # Sleep goal
fig.add_hline(y=2, ...)      # Water intake goal
```

### 📦 Dependencies

- **streamlit** - Web framework
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **plotly** - Interactive charts
- **python-dotenv** - Environment variables
- **streamlit-option-menu** - Menu options (optional)
- **streamlit-lottie** - Animations (optional)

### 🚨 Troubleshooting

**App won't start**
```bash
pip install -r requirements.txt
python -m streamlit run main.py --logger.level=error
```

**Charts not showing**
- Ensure Plotly is installed: `pip install plotly`
- Check browser cache (Ctrl+F5 to refresh)

**Data not saving**
- Verify `data/` folder exists
- Check folder permissions
- Ensure JSON files aren't corrupted

**Slow performance**
- Clear browser cache
- Reduce number of historical records
- Restart Streamlit server

### 📞 Support

For issues or questions:
1. Check the `.md` files in the project root
2. Review the `modules/` folder code comments
3. Check Streamlit documentation: https://docs.streamlit.io

---

**Enjoy your enhanced Health Coach AI! 🎉**

Get started now: `streamlit run main.py`
