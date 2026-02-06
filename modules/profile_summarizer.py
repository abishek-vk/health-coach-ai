"""
profile_summarizer.py - Data compression and health profile summarization
Compresses historical health data into compact profiles with key metrics
"""

from typing import List, Dict, Optional, Any
import numpy as np
import pandas as pd


class HealthProfileSummarizer:
    """Summarizes and compresses health data into compact profiles"""
    
    @staticmethod
    def calculate_bmi(height_cm: float, weight_kg: float) -> float:
        """
        Calculate Body Mass Index
        
        Args:
            height_cm: Height in centimeters
            weight_kg: Weight in kilograms
            
        Returns:
            BMI value
        """
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 2)
    
    @staticmethod
    def categorize_bmi(bmi: float) -> str:
        """
        Categorize BMI into health categories
        
        Args:
            bmi: BMI value
            
        Returns:
            BMI category string
        """
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal Weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    @staticmethod
    def calculate_activity_level(daily_steps: float) -> str:
        """
        Categorize activity level based on daily steps
        
        Args:
            daily_steps: Average daily steps
            
        Returns:
            Activity level category
        """
        if daily_steps < 3000:
            return "Sedentary"
        elif daily_steps < 7000:
            return "Lightly Active"
        elif daily_steps < 10000:
            return "Moderately Active"
        elif daily_steps < 15000:
            return "Very Active"
        else:
            return "Extremely Active"
    
    @staticmethod
    def categorize_sleep(sleep_hours: float) -> str:
        """
        Categorize sleep quality based on hours
        
        Args:
            sleep_hours: Average sleep hours per night
            
        Returns:
            Sleep category
        """
        if sleep_hours < 5:
            return "Insufficient"
        elif sleep_hours < 7:
            return "Below Optimal"
        elif sleep_hours <= 9:
            return "Optimal"
        else:
            return "Excessive"
    
    @staticmethod
    def categorize_hydration(water_liters: float) -> str:
        """
        Categorize hydration level
        
        Args:
            water_liters: Average daily water intake in liters
            
        Returns:
            Hydration category
        """
        if water_liters < 1.5:
            return "Dehydrated"
        elif water_liters < 2.0:
            return "Below Recommended"
        elif water_liters <= 3.0:
            return "Adequate"
        else:
            return "Well Hydrated"
    
    @staticmethod
    def identify_health_risks(profile_data: Dict) -> List[str]:
        """
        Identify potential health risks from profile data
        
        Args:
            profile_data: Summarized health profile dictionary
            
        Returns:
            List of identified health risks
        """
        risks = []
        
        # BMI-related risks
        bmi_category = profile_data.get("bmi_category", "")
        if bmi_category in ["Underweight", "Obese"]:
            risks.append(f"BMI Category: {bmi_category} - Consider consulting a healthcare provider")
        
        # Sleep-related risks
        sleep_category = profile_data.get("sleep_category", "")
        if sleep_category in ["Insufficient", "Excessive"]:
            risks.append(f"Sleep Pattern: {sleep_category} - May affect overall health")
        
        # Activity-related risks
        activity = profile_data.get("activity_level", "")
        if activity == "Sedentary":
            risks.append("Sedentary Lifestyle: Increase physical activity to reduce health risks")
        
        # Hydration risks
        hydration = profile_data.get("hydration_level", "")
        if hydration in ["Dehydrated", "Below Recommended"]:
            risks.append(f"Hydration: {hydration} - Increase water intake")
        
        # Medical conditions
        medical = profile_data.get("medical_conditions", "").lower()
        if medical != "none" and medical.strip():
            risks.append(f"Medical Conditions: {profile_data.get('medical_conditions')} - Follow doctor's advice")
        
        return risks
    
    @staticmethod
    def summarize_from_records(user_records: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Compress and summarize health records into a compact profile
        
        Args:
            user_records: List of health records (from JSON)
            
        Returns:
            Compressed health profile or None if no records
        """
        if not user_records:
            return None
        
        # Extract data using pandas for efficient computation
        records_list = []
        for record in user_records:
            if "data" in record:
                records_list.append(record["data"])
            else:
                records_list.append(record)
        
        df = pd.DataFrame(records_list)
        
        # Calculate averages and statistics
        # Use latest values for user info (these shouldn't change often)
        latest_record = records_list[-1]
        
        summary_profile = {
            "age": latest_record.get("age"),
            "gender": latest_record.get("gender"),
            "height_cm": latest_record.get("height_cm"),
            "weight_kg": latest_record.get("weight_kg"),
            "medical_conditions": latest_record.get("medical_conditions", "None"),
            
            # Calculated metrics
            "average_steps": round(df["daily_steps"].mean(), 0) if "daily_steps" in df.columns else 0,
            "average_sleep_hours": round(df["sleep_hours"].mean(), 2) if "sleep_hours" in df.columns else 0,
            "average_water_intake": round(df["water_intake_liters"].mean(), 2) if "water_intake_liters" in df.columns else 0,
            
            # Statistical metrics
            "steps_std_dev": round(df["daily_steps"].std(), 0) if "daily_steps" in df.columns else 0,
            "sleep_std_dev": round(df["sleep_hours"].std(), 2) if "sleep_hours" in df.columns else 0,
            "water_std_dev": round(df["water_intake_liters"].std(), 2) if "water_intake_liters" in df.columns else 0,
            
            # Historical counts
            "total_records": len(user_records),
            "days_tracked": len(user_records)
        }
        
        # Calculate BMI and categorize
        bmi = HealthProfileSummarizer.calculate_bmi(
            summary_profile["height_cm"], 
            summary_profile["weight_kg"]
        )
        summary_profile["bmi"] = bmi
        summary_profile["bmi_category"] = HealthProfileSummarizer.categorize_bmi(bmi)
        
        # Categorize other metrics
        summary_profile["activity_level"] = HealthProfileSummarizer.calculate_activity_level(
            summary_profile["average_steps"]
        )
        summary_profile["sleep_category"] = HealthProfileSummarizer.categorize_sleep(
            summary_profile["average_sleep_hours"]
        )
        summary_profile["hydration_level"] = HealthProfileSummarizer.categorize_hydration(
            summary_profile["average_water_intake"]
        )
        
        # Identify health risks
        summary_profile["health_risks"] = HealthProfileSummarizer.identify_health_risks(
            summary_profile
        )
        
        return summary_profile
