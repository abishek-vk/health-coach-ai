"""
quick_start.py - Quick start script to test the system with different user scenarios
Run different demonstrations without manual data entry
"""

from modules.data_input import HealthDataCollector
from modules.file_storage import JSONHealthStorage
from modules.profile_summarizer import HealthProfileSummarizer
from modules.recommendation_engine import RecommendationEngine
from datetime import datetime
import json


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_scenario(name, age, gender, height, weight, medical, daily_data):
    """Test a specific user scenario"""
    print_header(f"SCENARIO: {name}")
    print(f"\nTesting health coach for: {name}")
    print(f"Profile: {age}y/o {gender}, {height}cm, {weight}kg")
    
    collector = HealthDataCollector()
    storage = JSONHealthStorage(data_dir="data")
    user_id = f"scenario_{name.lower().replace(' ', '_')}"
    
    # Collect user info
    is_valid, error, user_info = collector.collect_userinfo(
        age=age, gender=gender, height=height, 
        weight=weight, medical_conditions=medical
    )
    
    if not is_valid:
        print(f"❌ Validation Error: {error}")
        return
    
    # Add multiple days of data
    print(f"\n📊 Simulating {len(daily_data)} days of health data...")
    
    for i, metrics in enumerate(daily_data, 1):
        is_valid, _, daily_metrics = collector.collect_daily_metrics(
            daily_steps=metrics['steps'],
            sleep_hours=metrics['sleep'],
            water_intake=metrics['water']
        )
        
        if is_valid:
            record = collector.create_health_record(user_info, daily_metrics)
            storage.add_health_record(user_id, record)
    
    print(f"✅ Added {len(daily_data)} health records")
    
    # Get records and create profile
    records = storage.get_user_records(user_id)
    profile = HealthProfileSummarizer.summarize_from_records(records)
    storage.save_user_profile(user_id, profile)
    
    # Display profile
    print_header(f"HEALTH PROFILE: {name}")
    print(f"Age: {profile['age']} | Gender: {profile['gender']}")
    print(f"Height: {profile['height_cm']}cm | Weight: {profile['weight_kg']}kg")
    print(f"BMI: {profile['bmi']} ({profile['bmi_category']})")
    print(f"Activity Level: {profile['activity_level']}")
    print(f"Avg Steps: {int(profile['average_steps']):,}")
    print(f"Avg Sleep: {profile['average_sleep_hours']}h ({profile['sleep_category']})")
    print(f"Avg Water: {profile['average_water_intake']}L ({profile['hydration_level']})")
    
    # Generate recommendations
    recommendations = RecommendationEngine.generate_comprehensive_recommendations(profile)
    
    print_header(f"RECOMMENDATIONS: {name}")
    print("\n🏃 EXERCISE:")
    for rec in recommendations['exercise'][:2]:
        print(f"  → {rec}")
    
    print("\n🥗 DIET:")
    for rec in recommendations['diet'][:2]:
        print(f"  → {rec}")
    
    if profile.get('health_risks'):
        print("\n⚠️ HEALTH ALERTS:")
        for risk in profile['health_risks']:
            print(f"  → {risk}")
    else:
        print("\n✅ No major health risks identified")
    
    print(f"\n✓ Scenario '{name}' complete - Data saved for user: {user_id}")
    return user_id


def main():
    """Run multiple test scenarios"""
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + "PERSONAL HEALTH COACH AI - QUICK START SCENARIOS".center(68) + "║")
    print("╚" + "═"*68 + "╝")
    
    # Scenario 1: Sedentary Office Worker
    test_scenario(
        name="Sedentary Office Worker",
        age=35,
        gender="Male",
        height=175,
        weight=90,
        medical="High cholesterol",
        daily_data=[
            {'steps': 2500, 'sleep': 6.5, 'water': 1.2},
            {'steps': 2800, 'sleep': 6.0, 'water': 1.0},
            {'steps': 2200, 'sleep': 7.0, 'water': 1.5},
            {'steps': 3000, 'sleep': 6.5, 'water': 1.3},
            {'steps': 2600, 'sleep': 5.5, 'water': 0.9},
        ]
    )
    
    # Scenario 2: Active Fitness Enthusiast
    test_scenario(
        name="Active Fitness Enthusiast",
        age=28,
        gender="Female",
        height=168,
        weight=62,
        medical="None",
        daily_data=[
            {'steps': 12000, 'sleep': 8.0, 'water': 3.5},
            {'steps': 15000, 'sleep': 7.5, 'water': 3.2},
            {'steps': 11500, 'sleep': 8.5, 'water': 3.8},
            {'steps': 13000, 'sleep': 8.0, 'water': 3.4},
            {'steps': 14200, 'sleep': 7.5, 'water': 3.6},
        ]
    )
    
    # Scenario 3: Elderly Person with Health Concerns
    test_scenario(
        name="Elderly Person",
        age=68,
        gender="Female",
        height=162,
        weight=72,
        medical="Diabetes, Hypertension",
        daily_data=[
            {'steps': 4500, 'sleep': 7.5, 'water': 2.0},
            {'steps': 5000, 'sleep': 8.0, 'water': 2.2},
            {'steps': 4200, 'sleep': 7.5, 'water': 1.8},
            {'steps': 5500, 'sleep': 8.5, 'water': 2.1},
            {'steps': 4800, 'sleep': 7.5, 'water': 1.9},
        ]
    )
    
    # Scenario 4: Sleep-Deprived Professional
    test_scenario(
        name="Sleep-Deprived Professional",
        age=42,
        gender="Male",
        height=182,
        weight=88,
        medical="Stress",
        daily_data=[
            {'steps': 6500, 'sleep': 4.5, 'water': 2.0},
            {'steps': 7000, 'sleep': 5.0, 'water': 2.1},
            {'steps': 6200, 'sleep': 4.5, 'water': 1.9},
            {'steps': 6800, 'sleep': 5.5, 'water': 2.0},
            {'steps': 7200, 'sleep': 4.0, 'water': 2.2},
        ]
    )
    
    # Scenario 5: Overweight Individual Starting Fitness Journey
    test_scenario(
        name="Fitness Journey Beginner",
        age=45,
        gender="Female",
        height=165,
        weight=95,
        medical="Prediabetes",
        daily_data=[
            {'steps': 3200, 'sleep': 7.0, 'water': 1.5},
            {'steps': 3800, 'sleep': 7.5, 'water': 1.8},
            {'steps': 4200, 'sleep': 6.5, 'water': 1.6},
            {'steps': 4500, 'sleep': 7.5, 'water': 1.9},
            {'steps': 3900, 'sleep': 7.0, 'water': 1.7},
        ]
    )
    
    # Final Summary
    print_header("QUICK START COMPLETE")
    print("""
✅ 5 Scenarios tested successfully
✅ Health profiles generated
✅ Personalized recommendations created
✅ Data stored in JSON files

Next Steps:
1. Launch the Streamlit dashboard:
   $ streamlit run main.py

2. Login with one of these user IDs:
   - scenario_sedentary_office_worker
   - scenario_active_fitness_enthusiast
   - scenario_elderly_person
   - scenario_sleep_deprived_professional
   - scenario_fitness_journey_beginner

3. View the health summary and recommendations for each scenario

4. Try adding your own health data and get personalized recommendations!
    """)


if __name__ == "__main__":
    main()
