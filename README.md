# 🏥 Personal Health Coach AI Agent

A fully functional AI-powered personal health coach system built with Python, featuring intelligent health data management, compression, and personalized recommendations. The system uses local JSON file storage for lightweight, database-free operation.

## 📋 Features

### ✨ Core Features
- **📥 Health Data Collection**: Age, gender, height, weight, medical conditions, daily steps, sleep hours, water intake
- **💾 JSON-Based Storage**: Lightweight file storage without database dependencies
- **Data Compression**: Automatically compresses historical records into compact health profiles
- **Health Analysis**: BMI calculation, activity level assessment, sleep quality analysis, hydration tracking
- **Intelligent Recommendations**: Personalized exercise, diet, sleep, and hydration suggestions
- **Health Risk Detection**: Identifies potential health risks and early warning indicators
- **📱 Interactive Dashboard**: Streamlit web interface for easy data entry and visualization
- **🔍 Data Visualization**: Charts and trends for historical health data

### Architecture
- **Modular Design**: 5 independent, reusable modules
- **Clean Separation of Concerns**: Input validation, storage, summarization, and recommendations
- **Input Validation**: Comprehensive validation for all health metrics
- **Error Handling**: Robust error handling throughout the system
- **Logging**: Detailed logging for debugging and monitoring

## Project Structure

```
personal-health-coach-ai/
├── requirements.txt              # Python dependencies
├── main.py                       # Streamlit dashboard application
├── demo.py                       # Complete system demonstration
├── README.md                     # Documentation (this file)
├── modules/                      # Core application modules
│   ├── __init__.py
│   ├── validators.py             # Input validation module
│   ├── data_input.py             # Data collection & validation
│   ├── file_storage.py           # JSON file handling
│   ├── profile_summarizer.py     # Data compression & summarization
│   └── recommendation_engine.py  # Recommendation generation
└── data/                         # Local JSON storage
    ├── user_records.json         # Historical health records
    └── user_profiles.json        # Compressed health profiles
```

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
```bash
cd personal-health-coach-ai
```

2. **Create a virtual environment (recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Interactive Streamlit Dashboard
```bash
streamlit run main.py
```
This launches a web-based dashboard at `http://localhost:8501`

#### Option 2: Run Demonstration
```bash
python demo.py
```
This shows a complete end-to-end demonstration of the system in the console.

## Usage Guide

### Using the Streamlit Dashboard

#### 1. **Home Page**
- Start here to create a user account
- Enter a unique User ID to begin tracking
- Overview of system features

#### 2. **Input Health Data**
- Enter basic health information:
  - Age (1-150 years)
  - Gender (Male/Female/Other)
  - Height (30-300 cm)
  - Weight (1-300 kg)
  - Medical conditions (optional)
  
- Enter daily health metrics:
  - Daily steps (0-100,000)
  - Sleep hours (0-24 hours)
  - Water intake (0-20 liters)

#### 3. **Health Summary**
- View compressed health profile
- See calculated metrics:
  - BMI and category
  - Activity level
  - Sleep quality
  - Hydration status
- View activity and sleep trends
- Check identified health risks

#### 4. **Recommendations**
- Get personalized recommendations for:
  - **Exercise**: Based on activity level
  - **Diet**: Based on BMI and health metrics
  - **Sleep**: Based on sleep patterns
  - **Hydration**: Based on water intake
  - **Health Alerts**: Risk warnings and indicators

#### 5. **Data Management**
- View all records for a user
- Delete user data (with confirmation)

## 🔧 Module Reference

### `validators.py` - Input Validation
Validates all health data inputs with specific business rules.

**Key Classes:**
- `HealthDataValidator`: Validates age, gender, height, weight, medical conditions, steps, sleep, water

**Methods:**
- `validate_age()`: Age between 1-150
- `validate_height()`: Height between 30-300 cm
- `validate_weight()`: Weight between 1-300 kg
- `validate_steps()`: Steps between 0-100,000
- `validate_sleep_hours()`: Sleep between 0-24 hours
- `validate_water_intake()`: Water between 0-20 liters

### `data_input.py` - Data Collection
Collects user health data with validation.

**Key Classes:**
- `HealthDataCollector`: Manages health data input and collection

**Methods:**
- `collect_user_info()`: Collect basic user information
- `collect_daily_metrics()`: Collect daily health metrics
- `create_health_record()`: Combine info and metrics into one record

### `file_storage.py` - JSON Storage
Manages reading/writing health records to JSON files.

**Key Classes:**
- `JSONHealthStorage`: Manages JSON file storage

**Methods:**
- `add_health_record()`: Save new health record
- `get_user_records()`: Retrieve all records for a user
- `save_user_profile()`: Save compressed profile
- `get_user_profile()`: Retrieve compressed profile
- `delete_user_data()`: Delete all user data

### `profile_summarizer.py` - Data Compression
Compresses historical health data into compact profiles.

**Key Classes:**
- `HealthProfileSummarizer`: Summarizes and compresses health data

**Key Methods:**
- `summarize_from_records()`: Compress historical records into profile
- `calculate_bmi()`: Calculate Body Mass Index
- `categorize_bmi()`: Categorize BMI (Underweight/Normal/Overweight/Obese)
- `calculate_activity_level()`: Categorize activity (Sedentary/Lightly Active/Moderately Active/Very Active)
- `categorize_sleep()`: Categorize sleep (Insufficient/Below Optimal/Optimal/Excessive)
- `categorize_hydration()`: Categorize hydration (Dehydrated/Below Recommended/Adequate/Well Hydrated)
- `identify_health_risks()`: Identify potential health risks

### `recommendation_engine.py` - Recommendations
Generates intelligent personalized recommendations.

**Key Classes:**
- `RecommendationEngine`: Generates health recommendations

**Key Methods:**
- `generate_exercise_recommendations()`: Exercise suggestions
- `generate_diet_recommendations()`: Diet guidance
- `generate_sleep_recommendations()`: Sleep improvement tips
- `generate_hydration_reminders()`: Hydration suggestions
- `generate_health_alerts()`: Health risk alerts
- `generate_comprehensive_recommendations()`: All recommendations at once

## 📊 Data Storage Format

### user_records.json
Stores all health records with timestamps:
```json
{
  "records": [
    {
      "user_id": "user_001",
      "timestamp": "2024-02-06T10:30:00.000000",
      "data": {
        "age": 32,
        "gender": "Male",
        "height_cm": 180,
        "weight_kg": 85,
        "medical_conditions": "None",
        "daily_steps": 8500,
        "sleep_hours": 7.5,
        "water_intake_liters": 2.5
      }
    }
  ]
}
```

### user_profiles.json
Stores compressed health profiles:
```json
{
  "profiles": [
    {
      "user_id": "user_001",
      "created_at": "2024-02-06T10:30:00.000000",
      "last_updated": "2024-02-06T11:00:00.000000",
      "data": {
        "age": 32,
        "gender": "Male",
        "average_steps": 8450,
        "average_sleep_hours": 7.4,
        "average_water_intake": 2.4,
        "bmi": 26.2,
        "bmi_category": "Overweight",
        "activity_level": "Moderately Active",
        "sleep_category": "Optimal",
        "hydration_level": "Adequate",
        "health_risks": [],
        "total_records": 10
      }
    }
  ]
}
```

## 🧪 Demonstration Workflow

Run the demo to see the complete system in action:

```bash
python demo.py
```

### Demo Workflow
1. **Data Collection & Validation**: Shows input validation
2. **JSON Storage**: Demonstrates file-based storage
3. **Data Compression**: Shows how 10 records compress to 1 profile
4. **Profile Analysis**: Displays calculated health metrics
5. **Recommendation Generation**: Shows personalized recommendations

## 📝 Example Workflow

### Collecting Health Data
```python
from modules.data_input import HealthDataCollector

collector = HealthDataCollector()

# Validate and collect user info
is_valid, error, user_info = collector.collect_user_info(
    age=32,
    gender="Male",
    height=180,
    weight=85,
    medical_conditions="None"
)

# Validate and collect daily metrics
is_valid, error, daily_metrics = collector.collect_daily_metrics(
    daily_steps=8500,
    sleep_hours=7.5,
    water_intake=2.5
)

# Create complete record
health_record = collector.create_health_record(user_info, daily_metrics)
```

### Storing Data
```python
from modules.file_storage import JSONHealthStorage

storage = JSONHealthStorage(data_dir="data")

# Save health record
storage.add_health_record("user_001", health_record)

# Retrieve records
records = storage.get_user_records("user_001")
```

### Compressing Data
```python
from modules.profile_summarizer import HealthProfileSummarizer

# Compress historical records into profile
profile = HealthProfileSummarizer.summarize_from_records(user_records)

# Profile contains:
# - average_steps, average_sleep_hours, average_water_intake
# - bmi, bmi_category
# - activity_level, sleep_category, hydration_level
# - health_risks (identified risks)
```

### Generating Recommendations
```python
from modules.recommendation_engine import RecommendationEngine

# Generate all recommendations
all_recommendations = RecommendationEngine.generate_comprehensive_recommendations(profile)

# Includes:
# - exercise recommendations
# - diet guidance
# - sleep tips
# - hydration reminders
# - health alerts
```

## 🎯 Health Metrics Explained

### BMI Categories
- **Underweight**: BMI < 18.5
- **Normal Weight**: BMI 18.5-24.9
- **Overweight**: BMI 25-29.9
- **Obese**: BMI ≥ 30

### Activity Levels
- **Sedentary**: < 3,000 steps/day
- **Lightly Active**: 3,000-6,999 steps/day
- **Moderately Active**: 7,000-9,999 steps/day
- **Very Active**: 10,000-14,999 steps/day
- **Extremely Active**: ≥ 15,000 steps/day

### Sleep Categories
- **Insufficient**: < 5 hours
- **Below Optimal**: 5-6.9 hours
- **Optimal**: 7-9 hours
- **Excessive**: > 9 hours

### Hydration Levels
- **Dehydrated**: < 1.5 liters/day
- **Below Recommended**: 1.5-1.9 liters/day
- **Adequate**: 2-3 liters/day
- **Well Hydrated**: > 3 liters/day

## ⚠️ Health Risk Detection

The system automatically identifies potential health risks:
- **BMI-Related Risks**: Alerts for underweight/obese categories
- **Sleep-Related Risks**: Alerts for insufficient/excessive sleep
- **Activity Risks**: Alerts for sedentary lifestyle
- **Hydration Risks**: Alerts for dehydration
- **Medical Conditions**: Alerts for existing conditions
- **Age-Specific Risks**: Special alerts for ages 50+, 65+

## 📦 Dependencies

```
streamlit==1.28.1      # Web interface framework
pandas==2.1.1          # Data manipulation and analysis
numpy==1.24.3          # Numerical computing
python-dateutil==2.8.2 # Date/time utilities
```

## 🔒 Privacy & Security

- **No External Database**: All data stored locally in JSON files
- **Local Storage**: Data never leaves your computer
- **User-Specific**: Each user ID has isolated data
- **Easy Deletion**: Can completely delete user data on demand

## 🐛 Troubleshooting

### Streamlit Not Found
```bash
pip install streamlit --upgrade
```

### Port Already in Use
```bash
streamlit run main.py --server.port 8502
```

### Data Directory Issues
Ensure you have write permissions in the project directory. The system auto-creates the `data/` folder.

### JSON File Corruption
Delete `data/user_records.json` and/or `data/user_profiles.json` to reset storage. The system will recreate them on next run.

## 🚀 Advanced Features

### Extending the System

#### Add Custom Health Metrics
1. Update `validators.py` with new validation rules
2. Update `data_input.py` to collect new metrics
3. Update `profile_summarizer.py` to calculate metrics
4. Update `recommendation_engine.py` to generate recommendations

#### Adding More Recommendations
Simply extend the recommendation engine methods with additional logic:
```python
@staticmethod
def generate_stress_recommendations(profile: Dict[str, Any]) -> List[str]:
    """Add stress management recommendations"""
    recommendations = []
    # Add logic here
    return recommendations
```

#### Exporting Data
```python
import json

# Export user profile as JSON
with open("user_profile_export.json", "w") as f:
    json.dump(profile, f, indent=2)
```

## 📊 Performance Notes

### Data Compression Efficiency
- **10 records** → ~3,000 bytes → **1 profile** ~700 bytes
- **Compression ratio**: ~77% reduction
- **100 records** → ~30KB → **1 profile** ~700 bytes

### Scalability
- System efficiently handles 1,000+ records per user
- JSON format maintains human readability
- Suitable for personal health use; not optimized for massive datasets

## 📚 Additional Resources

### Recommended Daily Values
- **Steps**: 7,000-10,000 per day
- **Sleep**: 7-9 hours per night
- **Water**: 2-3 liters per day
- **Exercise**: 150 minutes moderate intensity weekly

### Health Resources
- WHO Physical Activity Guidelines
- American Heart Association Recommendations
- CDC Health Recommendations
- Mayo Clinic Health Information

## 📄 License

This project is provided as educational software for personal health tracking.

## 👨‍💻 Contributing

To extend this project:
1. Follow the modular architecture
2. Add comprehensive comments
3. Update documentation
4. Test all code thoroughly
5. Maintain clean separation of concerns

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review module documentation
3. Run the demo to understand the workflow
4. Check input validation rules for data errors

## 🎯 Future Enhancements

- 📱 Mobile app integration
- 📊 Advanced data analytics and trends
- 🤖 Machine learning predictions
- 📧 Email notification reminders
- 🔄 Multi-device synchronization
- 📈 Integration with fitness trackers
- 🧬 Genetic health insights
- 👥 Social features and community

## 🏆 Key Highlights

✅ **No Database Required**: Pure JSON file storage
✅ **Modular Architecture**: 5 independent, reusable modules
✅ **Comprehensive Validation**: All inputs thoroughly validated
✅ **Data Compression**: Automatic summarization of historical data
✅ **Intelligent Recommendations**: Personalized, multi-category suggestions
✅ **Interactive Dashboard**: Beautiful Streamlit interface
✅ **Production Ready**: Error handling, logging, and documentation
✅ **Easy to Extend**: Clean code structure for customization

---

**Built with ❤️ for Health & Wellness**

*Personal Health Coach AI v1.0*
