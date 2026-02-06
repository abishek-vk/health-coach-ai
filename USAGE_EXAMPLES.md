"""
USAGE_EXAMPLES.md - Comprehensive Usage Examples
Shows how to use the Personal Health Coach AI system programmatically
"""

# Personal Health Coach AI - Usage Examples

This document provides comprehensive code examples showing how to use each module of the Personal Health Coach AI system.

## Table of Contents
1. [Basic Usage](#basic-usage)
2. [Data Input & Validation](#data-input--validation)
3. [File Storage Operations](#file-storage-operations)
4. [Data Compression & Summarization](#data-compression--summarization)
5. [Recommendation Generation](#recommendation-generation)
6. [Complete Workflows](#complete-workflows)

---

## Basic Usage

### Initialize the System

```python
from modules.data_input import HealthDataCollector
from modules.file_storage import JSONHealthStorage
from modules.profile_summarizer import HealthProfileSummarizer
from modules.recommendation_engine import RecommendationEngine
from modules.validators import HealthDataValidator

# Create instances
collector = HealthDataCollector()
storage = JSONHealthStorage(data_dir="data")
validator = HealthDataValidator()
```

---

## Data Input & Validation

### Example 1: Validate Individual Health Metrics

```python
from modules.validators import HealthDataValidator

validator = HealthDataValidator()

# Validate age
is_valid, error = validator.validate_age(32)
if is_valid:
    print("✅ Age is valid")
else:
    print(f"❌ Error: {error}")

# Validate height
is_valid, error = validator.validate_height(180)
print(f"Height validation: {is_valid}")

# Validate weight
is_valid, error = validator.validate_weight(85)
print(f"Weight validation: {is_valid}")

# Validate steps
is_valid, error = validator.validate_steps(8500)
print(f"Steps validation: {is_valid}")
```

### Example 2: Collect User Information with Validation

```python
from modules.data_input import HealthDataCollector

collector = HealthDataCollector()

# Collect user info - returns (is_valid, error, data)
is_valid, error, user_info = collector.collect_user_info(
    age=32,
    gender="Male",
    height=180,
    weight=85,
    medical_conditions="None"
)

if is_valid:
    print("User info collected successfully!")
    print(f"Age: {user_info['age']}")
    print(f"Gender: {user_info['gender']}")
    print(f"BMI: {user_info['height_cm']} x {user_info['weight_kg']}")
else:
    print(f"Validation error: {error}")
```

### Example 3: Collect Daily Health Metrics

```python
from modules.data_input import HealthDataCollector

collector = HealthDataCollector()

# Collect daily metrics
is_valid, error, daily_metrics = collector.collect_daily_metrics(
    daily_steps=8500,
    sleep_hours=7.5,
    water_intake=2.5
)

if is_valid:
    print("Daily metrics collected!")
    print(f"Steps: {daily_metrics['daily_steps']}")
    print(f"Sleep: {daily_metrics['sleep_hours']} hours")
    print(f"Water: {daily_metrics['water_intake_liters']} liters")
else:
    print(f"Validation error: {error}")
```

### Example 4: Create Complete Health Record

```python
from modules.data_input import HealthDataCollector

collector = HealthDataCollector()

# Collect info
is_valid, _, user_info = collector.collect_user_info(32, "Male", 180, 85, "None")
is_valid, _, daily_metrics = collector.collect_daily_metrics(8500, 7.5, 2.5)

# Combine into one record
health_record = collector.create_health_record(user_info, daily_metrics)
print(f"Complete record with {len(health_record)} fields")
```

---

## File Storage Operations

### Example 1: Create Storage Instance

```python
from modules.file_storage import JSONHealthStorage

# Create storage with default data directory
storage = JSONHealthStorage()  # Uses "data" directory

# Or specify custom directory
storage = JSONHealthStorage(data_dir="my_health_data")
```

### Example 2: Add Health Records

```python
# Add a single health record
health_record = {
    "age": 32,
    "gender": "Male",
    "height_cm": 180,
    "weight_kg": 85,
    "medical_conditions": "None",
    "daily_steps": 8500,
    "sleep_hours": 7.5,
    "water_intake_liters": 2.5
}

success = storage.add_health_record("user_001", health_record)
if success:
    print("✅ Record saved successfully")
else:
    print("❌ Error saving record")
```

### Example 3: Retrieve User Records

```python
# Get all records for a specific user
user_records = storage.get_user_records("user_001")
print(f"Found {len(user_records)} records for user_001")

# Access individual record
for record in user_records:
    timestamp = record["timestamp"]
    data = record["data"]
    print(f"{timestamp}: {data['daily_steps']} steps")

# Get all records across all users
all_records = storage.get_all_records()
print(f"Total records in system: {len(all_records)}")
```

### Example 4: Save and Retrieve User Profiles

```python
# Save a compressed profile
profile_data = {
    "age": 32,
    "gender": "Male",
    "average_steps": 8500,
    "average_sleep_hours": 7.5,
    "bmi": 26.23,
    "bmi_category": "Overweight",
    "activity_level": "Moderately Active"
}

success = storage.save_user_profile("user_001", profile_data)

# Retrieve profile later
profile = storage.get_user_profile("user_001")
if profile:
    print(f"Profile for user_001:")
    print(f"  BMI: {profile['bmi']} ({profile['bmi_category']})")
    print(f"  Activity: {profile['activity_level']}")
```

### Example 5: Delete User Data

```python
# Delete all data for a user (permanent)
success = storage.delete_user_data("user_001")
if success:
    print("✅ All data for user_001 deleted")
else:
    print("❌ Error deleting data")
```

---

## Data Compression & Summarization

### Example 1: Calculate BMI and Categorize

```python
from modules.profile_summarizer import HealthProfileSummarizer

# Calculate BMI
bmi = HealthProfileSummarizer.calculate_bmi(height_cm=180, weight_kg=85)
print(f"BMI: {bmi}")

# Categorize BMI
category = HealthProfileSummarizer.categorize_bmi(bmi)
print(f"Category: {category}")

# All BMI categories:
# Underweight (< 18.5), Normal Weight (18.5-24.9), 
# Overweight (25-29.9), Obese (≥ 30)
```

### Example 2: Categorize Activity Level

```python
from modules.profile_summarizer import HealthProfileSummarizer

# Categorize by average steps
avg_steps = 8500
activity = HealthProfileSummarizer.calculate_activity_level(avg_steps)
print(f"Activity Level: {activity}")

# Activity categories by steps:
# Sedentary (< 3000), Lightly Active (3000-6999),
# Moderately Active (7000-9999), Very Active (10000-14999),
# Extremely Active (≥ 15000)
```

### Example 3: Categorize Sleep Quality

```python
from modules.profile_summarizer import HealthProfileSummarizer

# Categorize sleep
avg_sleep = 7.5
sleep_category = HealthProfileSummarizer.categorize_sleep(avg_sleep)
print(f"Sleep Quality: {sleep_category}")

# Sleep categories:
# Insufficient (< 5h), Below Optimal (5-6.9h),
# Optimal (7-9h), Excessive (> 9h)
```

### Example 4: Categorize Hydration Level

```python
from modules.profile_summarizer import HealthProfileSummarizer

# Categorize hydration
avg_water = 2.5
hydration = HealthProfileSummarizer.categorize_hydration(avg_water)
print(f"Hydration: {hydration}")

# Hydration categories:
# Dehydrated (< 1.5L), Below Recommended (1.5-1.9L),
# Adequate (2-3L), Well Hydrated (> 3L)
```

### Example 5: Identify Health Risks

```python
from modules.profile_summarizer import HealthProfileSummarizer

# Example profile
profile = {
    "bmi_category": "Obese",
    "sleep_category": "Insufficient",
    "activity_level": "Sedentary",
    "hydration_level": "Dehydrated",
    "medical_conditions": "Diabetes"
}

# Identify risks
risks = HealthProfileSummarizer.identify_health_risks(profile)
for risk in risks:
    print(f"⚠️ {risk}")
```

### Example 6: Compress Historical Records

```python
from modules.file_storage import JSONHealthStorage
from modules.profile_summarizer import HealthProfileSummarizer

storage = JSONHealthStorage()

# Get all records for a user
user_records = storage.get_user_records("user_001")

# Compress into a profile
profile = HealthProfileSummarizer.summarize_from_records(user_records)

if profile:
    print(f"Profile Summary:")
    print(f"  Total records: {profile['total_records']}")
    print(f"  Days tracked: {profile['days_tracked']}")
    print(f"  Avg steps: {int(profile['average_steps']):,}")
    print(f"  Avg sleep: {profile['average_sleep_hours']}h")
    print(f"  Avg water: {profile['average_water_intake']}L")
    print(f"  Compression achieved: {profile['total_records']} records → 1 profile")
```

---

## Recommendation Generation

### Example 1: Generate Exercise Recommendations

```python
from modules.recommendation_engine import RecommendationEngine

profile = {
    "activity_level": "Sedentary",
    "average_steps": 2500,
    "age": 35
}

exercise_recs = RecommendationEngine.generate_exercise_recommendations(profile)
print("🏃 Exercise Recommendations:")
for rec in exercise_recs:
    print(f"  {rec}")
```

### Example 2: Generate Diet Recommendations

```python
from modules.recommendation_engine import RecommendationEngine

profile = {
    "bmi_category": "Overweight",
    "bmi": 27.5,
    "age": 40
}

diet_recs = RecommendationEngine.generate_diet_recommendations(profile)
print("🥗 Diet Recommendations:")
for rec in diet_recs:
    print(f"  {rec}")
```

### Example 3: Generate Sleep Recommendations

```python
from modules.recommendation_engine import RecommendationEngine

profile = {
    "sleep_category": "Insufficient",
    "average_sleep_hours": 4.5,
    "age": 35
}

sleep_recs = RecommendationEngine.generate_sleep_recommendations(profile)
print("😴 Sleep Recommendations:")
for rec in sleep_recs:
    print(f"  {rec}")
```

### Example 4: Generate Hydration Recommendations

```python
from modules.recommendation_engine import RecommendationEngine

profile = {
    "hydration_level": "Dehydrated",
    "average_water_intake": 1.2
}

hydration_recs = RecommendationEngine.generate_hydration_reminders(profile)
print("💧 Hydration Recommendations:")
for rec in hydration_recs:
    print(f"  {rec}")
```

### Example 5: Generate Health Alerts

```python
from modules.recommendation_engine import RecommendationEngine

profile = {
    "health_risks": ["BMI Category: Obese - Consider consulting a healthcare provider"],
    "medical_conditions": "Diabetes",
    "age": 55
}

alerts = RecommendationEngine.generate_health_alerts(profile)
print("⚠️ Health Alerts:")
for alert in alerts:
    print(f"  {alert}")
```

### Example 6: Generate All Recommendations at Once

```python
from modules.recommendation_engine import RecommendationEngine

# Complete profile from summarizer
profile = {
    "age": 32,
    "gender": "Male",
    "bmi": 26.23,
    "bmi_category": "Overweight",
    "activity_level": "Moderately Active",
    "average_steps": 8339,
    "sleep_category": "Optimal",
    "average_sleep_hours": 7.49,
    "hydration_level": "Adequate",
    "average_water_intake": 2.37,
    "health_risks": [],
    "medical_conditions": "None"
}

# Get all recommendations
all_recs = RecommendationEngine.generate_comprehensive_recommendations(profile)

print("Exercise:", len(all_recs['exercise']), "recommendations")
print("Diet:", len(all_recs['diet']), "recommendations")
print("Sleep:", len(all_recs['sleep']), "recommendations")
print("Hydration:", len(all_recs['hydration']), "recommendations")
print("Alerts:", len(all_recs['health_alerts']), "alerts")
```

---

## Complete Workflows

### Workflow 1: New User Registration and First Health Entry

```python
from modules.data_input import HealthDataCollector
from modules.file_storage import JSONHealthStorage

# Initialize
collector = HealthDataCollector()
storage = JSONHealthStorage()
user_id = "new_user_john"

# Collect user info
is_valid, _, user_info = collector.collect_user_info(
    age=30,
    gender="Male",
    height=175,
    weight=80,
    medical_conditions="None"
)

if not is_valid:
    print("Invalid user info")
    exit()

# Collect daily metrics
is_valid, _, daily_metrics = collector.collect_daily_metrics(
    daily_steps=7500,
    sleep_hours=7.0,
    water_intake=2.5
)

if not is_valid:
    print("Invalid metrics")
    exit()

# Create and save record
health_record = collector.create_health_record(user_info, daily_metrics)
success = storage.add_health_record(user_id, health_record)

if success:
    print(f"✅ User {user_id} registered and first record saved!")
```

### Workflow 2: Track Multiple Days and View Summary

```python
from modules.data_input import HealthDataCollector
from modules.file_storage import JSONHealthStorage
from modules.profile_summarizer import HealthProfileSummarizer
from modules.recommendation_engine import RecommendationEngine
import random

user_id = "user_john"
collector = HealthDataCollector()
storage = JSONHealthStorage()

# Simulate tracking for 7 days
print("📊 Tracking health for 7 days...\n")
for day in range(1, 8):
    # Generate realistic varying data
    steps = random.randint(6000, 12000)
    sleep = round(random.uniform(6, 9), 1)
    water = round(random.uniform(1.5, 3.5), 1)
    
    # User info stays same
    is_valid, _, user_info = collector.collect_user_info(32, "Male", 180, 85, "None")
    
    # Get daily metrics
    is_valid, _, daily_metrics = collector.collect_daily_metrics(steps, sleep, water)
    
    # Save record
    record = collector.create_health_record(user_info, daily_metrics)
    storage.add_health_record(user_id, record)
    
    print(f"Day {day}: {steps} steps, {sleep}h sleep, {water}L water ✓")

# Get summary
print("\n" + "="*50)
print("HEALTH PROFILE SUMMARY")
print("="*50 + "\n")

records = storage.get_user_records(user_id)
profile = HealthProfileSummarizer.summarize_from_records(records)
storage.save_user_profile(user_id, profile)

print(f"Days tracked: {profile['days_tracked']}")
print(f"Average steps: {int(profile['average_steps']):,}")
print(f"Average sleep: {profile['average_sleep_hours']}h")
print(f"Average water: {profile['average_water_intake']}L")
print(f"BMI: {profile['bmi']} ({profile['bmi_category']})")
print(f"Activity level: {profile['activity_level']}")

# Get recommendations
recs = RecommendationEngine.generate_comprehensive_recommendations(profile)
print(f"\nRecommendations generated: {len(recs['exercise'])} exercise tips")
```

### Workflow 3: Monitor Health Progress Over Time

```python
from modules.file_storage import JSONHealthStorage
from modules.profile_summarizer import HealthProfileSummarizer

user_id = "user_john"
storage = JSONHealthStorage()

# Get records over time
records = storage.get_user_records(user_id)
print(f"Total records for {user_id}: {len(records)}\n")

# Show first and latest records
first = records[0]['data']
latest = records[-1]['data']

print("PROGRESS COMPARISON:")
print("─" * 50)
print(f"First record - Steps: {first['daily_steps']}, Sleep: {first['sleep_hours']}h")
print(f"Latest record - Steps: {latest['daily_steps']}, Sleep: {latest['sleep_hours']}h")
print("─" * 50)

# Analyze trend
avg_first_3 = sum([r['data']['daily_steps'] for r in records[:3]]) / 3
avg_last_3 = sum([r['data']['daily_steps'] for r in records[-3:]]) / 3
improvement = ((avg_last_3 - avg_first_3) / avg_first_3) * 100

print(f"\nActivity trend: {improvement:+.1f}% change in steps")
if improvement > 0:
    print("✅ You're becoming more active!")
elif improvement < 0:
    print("⚠️ Your activity level has decreased")
else:
    print("➡️ Your activity level is stable")
```

### Workflow 4: Export User Health Data to JSON

```python
from modules.file_storage import JSONHealthStorage
import json

user_id = "user_john"
storage = JSONHealthStorage()

# Get all records
records = storage.get_user_records(user_id)
profile = storage.get_user_profile(user_id)

# Create export
export = {
    "user_id": user_id,
    "profile": profile,
    "historical_records": [r['data'] for r in records]
}

# Save to file
with open(f"export_{user_id}.json", "w") as f:
    json.dump(export, f, indent=2)

print(f"✅ Exported data for {user_id} to export_{user_id}.json")
```

### Workflow 5: Compare Two Users (Healthcare Provider Use Case)

```python
from modules.file_storage import JSONHealthStorage
from modules.profile_summarizer import HealthProfileSummarizer

storage = JSONHealthStorage()

# Get profiles
user1_recs = storage.get_user_records("user_john")
user2_recs = storage.get_user_records("user_jane")

profile1 = HealthProfileSummarizer.summarize_from_records(user1_recs)
profile2 = HealthProfileSummarizer.summarize_from_records(user2_recs)

print("USER COMPARISON REPORT")
print("="*60)
print(f"{'Metric':<20} {'User 1':<20} {'User 2':<20}")
print("="*60)

print(f"{'Age':<20} {profile1['age']:<20} {profile2['age']:<20}")
print(f"{'BMI':<20} {profile1['bmi']:<20} {profile2['bmi']:<20}")
print(f"{'Activity Level':<20} {profile1['activity_level']:<20} {profile2['activity_level']:<20}")
print(f"{'Sleep Quality':<20} {profile1['sleep_category']:<20} {profile2['sleep_category']:<20}")
print(f"{'Hydration':<20} {profile1['hydration_level']:<20} {profile2['hydration_level']:<20}")
```

---

## Error Handling Best Practices

```python
from modules.data_input import HealthDataCollector
from modules.file_storage import JSONHealthStorage

collector = HealthDataCollector()
storage = JSONHealthStorage()

try:
    # Validate before processing
    is_valid, error, data = collector.collect_user_info(
        age=150,  # At max
        gender="Male",
        height=180,
        weight=85,
        medical_conditions="None"
    )
    
    if not is_valid:
        print(f"⚠️ Validation error: {error}")
    else:
        # Process valid data
        print("✅ Data is valid")
        
except Exception as e:
    print(f"❌ Unexpected error: {str(e)}")
```

---

## Tips & Best Practices

1. **Always Validate First**: Check if data is valid before storing
2. **Use Try-Except**: Wrap file operations in error handling
3. **Keep User IDs Consistent**: Use same ID for same user across sessions
4. **Regular Backups**: Periodically copy the `data/` directory
5. **Check Return Values**: Always verify operation success
6. **Profile After Multiple Records**: Generate profiles only after 5+ days of data

For more examples and use cases, see `README.md` and `SETUP_INSTRUCTIONS.md`.
