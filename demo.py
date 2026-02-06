"""
demo.py - Demonstration workflow showing complete system operation
Shows how the Personal Health Coach AI system works end-to-end
"""

import json
from datetime import datetime, timedelta
from modules.data_input import HealthDataCollector
from modules.file_storage import JSONHealthStorage
from modules.profile_summarizer import HealthProfileSummarizer
from modules.recommendation_engine import RecommendationEngine


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def print_subsection(title):
    """Print a formatted subsection header"""
    print(f"\n{'─'*80}")
    print(f"  {title}")
    print(f"{'─'*80}\n")


def demo_data_collection():
    """Demonstrate data collection with validation"""
    print_section("STEP 1: DATA COLLECTION & VALIDATION")
    
    collector = HealthDataCollector()
    
    # Example: Collecting user information
    print("📝 Collecting User Basic Information...")
    print("-" * 50)
    
    is_valid, error, user_info = collector.collect_userinfo(
        age=32,
        gender="Male",
        height=180,
        weight=85,
        medical_conditions="None"
    )
    
    if is_valid:
        print("✅ User Information Valid!")
        print(f"   → Age: {user_info['age']} years")
        print(f"   → Gender: {user_info['gender']}")
        print(f"   → Height: {user_info['height_cm']} cm")
        print(f"   → Weight: {user_info['weight_kg']} kg")
        print(f"   → Medical Conditions: {user_info['medical_conditions']}")
    else:
        print(f"❌ Validation Error: {error}")
        return None
    
    # Collecting daily metrics
    print("\n📊 Collecting Daily Health Metrics...")
    print("-" * 50)
    
    is_valid, error, daily_metrics = collector.collect_daily_metrics(
        daily_steps=8500,
        sleep_hours=7.5,
        water_intake=2.5
    )
    
    if is_valid:
        print("✅ Daily Metrics Valid!")
        print(f"   → Daily Steps: {daily_metrics['daily_steps']} steps")
        print(f"   → Sleep Hours: {daily_metrics['sleep_hours']} hours")
        print(f"   → Water Intake: {daily_metrics['water_intake_liters']} liters")
    else:
        print(f"❌ Validation Error: {error}")
        return None
    
    # Create complete record
    health_record = collector.create_health_record(user_info, daily_metrics)
    
    return {
        "user_info": user_info,
        "daily_metrics": daily_metrics,
        "health_record": health_record
    }


def demo_data_storage(user_id, collected_data):
    """Demonstrate JSON file storage"""
    print_section("STEP 2: JSON FILE STORAGE")
    
    storage = JSONHealthStorage(data_dir="data")
    
    print(f"💾 Storing Health Records for User: {user_id}")
    print("-" * 50)
    
    # Add initial record
    if storage.add_health_record(user_id, collected_data["health_record"]):
        print("✅ First health record saved!")
    
    # Simulate multiple days of data
    print("\n📅 Simulating Multiple Days of Health Data...")
    print("-" * 50)
    
    collector = HealthDataCollector()
    
    # Generate 10 days of simulated data
    for day in range(1, 11):
        # Vary metrics slightly
        import random
        steps = random.randint(6000, 12000)
        sleep = round(random.uniform(6.0, 8.5), 1)
        water = round(random.uniform(1.5, 3.5), 1)
        
        is_valid, _, daily_metrics = collector.collect_daily_metrics(
            daily_steps=steps,
            sleep_hours=sleep,
            water_intake=water
        )
        
        if is_valid:
            record = collector.create_health_record(
                collected_data["user_info"],
                daily_metrics
            )
            storage.add_health_record(user_id, record)
            print(f"   ✓ Day {day}: {steps} steps, {sleep}h sleep, {water}L water")
    
    print(f"\n✅ Total records stored: {len(storage.get_user_records(user_id))}")
    
    return storage


def demo_data_compression(storage, user_id):
    """Demonstrate data compression and health profile summarization"""
    print_section("STEP 3: DATA COMPRESSION & HEALTH PROFILE SUMMARIZATION")
    
    print(f"📦 Compressing historical data for {user_id}...")
    print("-" * 50)
    
    # Get all user records
    user_records = storage.get_user_records(user_id)
    print(f"Total records to compress: {len(user_records)}\n")
    
    # Summarize records
    profile = HealthProfileSummarizer.summarize_from_records(user_records)
    
    if profile is None:
        print("❌ Error summarizing profile")
        return None
    
    # Save profile
    storage.save_user_profile(user_id, profile)
    
    # Display compressed profile
    print("✅ Compressed Health Profile Generated!\n")
    
    print_subsection("PROFILE OVERVIEW")
    print(f"User ID: {user_id}")
    print(f"Age: {profile['age']} years | Gender: {profile['gender']}")
    print(f"Height: {profile['height_cm']} cm | Weight: {profile['weight_kg']} kg\n")
    
    print_subsection("CALCULATED HEALTH METRICS")
    print(f"BMI: {profile['bmi']} ({profile['bmi_category']})")
    print(f"Activity Level: {profile['activity_level']}")
    print(f"   → Average Daily Steps: {int(profile['average_steps']):,} ± {int(profile['steps_std_dev'])}")
    print(f"\nSleep Quality: {profile['sleep_category']}")
    print(f"   → Average Sleep: {profile['average_sleep_hours']} hours ± {profile['sleep_std_dev']}h")
    print(f"\nHydration Level: {profile['hydration_level']}")
    print(f"   → Average Water Intake: {profile['average_water_intake']}L ± {profile['water_std_dev']}L\n")
    
    print_subsection("DATA COMPRESSION STATISTICS")
    print(f"Days Tracked: {profile['days_tracked']} days")
    print(f"Total Records: {profile['total_records']} records")
    print(f"Compression Ratio: {len(user_records)} records → 1 compressed profile ✓")
    print(f"Original Data Size: ~{len(user_records) * 300} bytes")
    print(f"Compressed Size: ~{len(json.dumps(profile))} bytes")
    print(f"Storage Efficiency: {round((1 - len(json.dumps(profile))/(len(user_records)*300))*100, 1)}% reduction")
    
    if profile.get("health_risks"):
        print_subsection("IDENTIFIED HEALTH INDICATORS")
        for risk in profile["health_risks"]:
            print(f"⚠️  {risk}")
    else:
        print_subsection("HEALTH STATUS")
        print("✅ No major health risks identified!")
    
    return profile


def demo_recommendation_generation(profile):
    """Demonstrate intelligent recommendation generation"""
    print_section("STEP 4: PERSONALIZED RECOMMENDATION GENERATION")
    
    print("🤖 Generating personalized health recommendations...\n")
    
    recommendations = RecommendationEngine.generate_comprehensive_recommendations(profile)
    
    # Display Exercise Recommendations
    print_subsection("🏃 EXERCISE RECOMMENDATIONS")
    for rec in recommendations["exercise"]:
        print(f"  {rec}")
    
    # Display Diet Recommendations
    print_subsection("🥗 DIET RECOMMENDATIONS")
    for rec in recommendations["diet"]:
        print(f"  {rec}")
    
    # Display Sleep Recommendations
    print_subsection("😴 SLEEP RECOMMENDATIONS")
    for rec in recommendations["sleep"]:
        print(f"  {rec}")
    
    # Display Hydration Recommendations
    print_subsection("💧 HYDRATION RECOMMENDATIONS")
    for rec in recommendations["hydration"]:
        print(f"  {rec}")
    
    # Display Health Alerts
    print_subsection("⚠️ HEALTH ALERTS & RISK INDICATORS")
    for alert in recommendations["health_alerts"]:
        print(f"  {alert}")
    
    return recommendations


def demo_system_overview():
    """Display system architecture overview"""
    print_section("SYSTEM ARCHITECTURE & WORKFLOW")
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    PERSONAL HEALTH COACH AI SYSTEM                            ║
╚═══════════════════════════════════════════════════════════════════════════════╝

  1️⃣  INPUT LAYER: Data Collection & Validation
     └─ Modules: data_input.py, validators.py
     └─ Validates: Age, Gender, Height, Weight, Medical Conditions,
                   Daily Steps, Sleep Hours, Water Intake

  2️⃣  STORAGE LAYER: JSON File-Based Storage
     └─ Module: file_storage.py
     └─ Stores: user_records.json, user_profiles.json
     └─ Benefits: No database needed, lightweight, human-readable

  3️⃣  COMPRESSION LAYER: Data Summarization
     └─ Module: profile_summarizer.py
     └─ Compresses: Historical data → Compact health profiles
     └─ Calculates: BMI, Activity Level, Sleep Quality, Hydration Status
     └─ Identifies: Health Risks & Alerts

  4️⃣  INTELLIGENCE LAYER: Recommendation Engine
     └─ Module: recommendation_engine.py
     └─ Generates: Exercise, Diet, Sleep, Hydration recommendations
     └─ Personalized: Based on user profile & health metrics
     └─ Intelligent: Risk-aware, age-aware, condition-aware

  5️⃣  PRESENTATION LAYER: Streamlit Dashboard
     └─ App: main.py
     └─ Interface: Web-based, user-friendly
     └─ Features: Data entry, visualization, insights, recommendations

═══════════════════════════════════════════════════════════════════════════════

DATA FLOW DIAGRAM:

  User Input
      ↓
  Validation (validators.py)
      ↓
  Data Collection (data_input.py)
      ↓
  JSON Storage (file_storage.py)
      ↓
  Profile Compression (profile_summarizer.py)
      ↓
  Recommendation Generation (recommendation_engine.py)
      ↓
  Streamlit Dashboard (main.py)
      ↓
  User Insights & Recommendations

═══════════════════════════════════════════════════════════════════════════════
    """)


def main():
    """Run complete demonstration"""
    
    # Print welcome message
    print("\n")
    print("╔" + "═"*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "PERSONAL HEALTH COACH AI - COMPLETE SYSTEM DEMONSTRATION".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "═"*78 + "╝")
    
    # System Overview
    demo_system_overview()
    
    # Step 1: Data Collection
    collected_data = demo_data_collection()
    if not collected_data:
        print("❌ Data collection failed!")
        return
    
    # Step 2: Data Storage
    user_id = "demo_user_001"
    storage = demo_data_storage(user_id, collected_data)
    
    # Step 3: Data Compression
    profile = demo_data_compression(storage, user_id)
    if not profile:
        print("❌ Data compression failed!")
        return
    
    # Step 4: Recommendation Generation
    recommendations = demo_recommendation_generation(profile)
    
    # Final Summary
    print_section("DEMONSTRATION COMPLETE ✅")
    print("""
This demonstration shows how the Personal Health Coach AI Agent:

1. ✅ COLLECTS health data with comprehensive validation
2. ✅ STORES data locally in JSON files (no database required)
3. ✅ COMPRESSES historical records into compact health profiles
4. ✅ GENERATES intelligent, personalized health recommendations

KEY FEATURES DEMONSTRATED:
  • Modular architecture (5 separate, reusable modules)
  • Data validation & error handling
  • Lightweight JSON-based storage
  • Automatic data compression (10 days → 1 profile)
  • Intelligent recommendation engine
  • Multiple recommendation categories
  • Health risk identification & alerts

NEXT STEPS:
  Run the Streamlit app to interact with the full system:
  
  $ streamlit run main.py
  
This will launch an interactive web interface for:
  • User data input
  • Health summary visualization
  • Real-time recommendation generation
  • Data management capabilities

═══════════════════════════════════════════════════════════════════════════════
    """)


if __name__ == "__main__":
    main()
