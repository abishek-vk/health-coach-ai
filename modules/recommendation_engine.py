"""
recommendation_engine.py - Intelligent recommendation generation
Analyzes health profiles and generates personalized health recommendations
"""

from typing import List, Dict, Optional, Any
from modules.profile_summarizer import HealthProfileSummarizer


class RecommendationEngine:
    """Generates personalized health recommendations based on user profiles"""
    
    @staticmethod
    def generate_exercise_recommendations(profile: Dict[str, Any]) -> List[str]:
        """
        Generate exercise recommendations based on activity level
        
        Args:
            profile: User health profile
            
        Returns:
            List of exercise recommendations
        """
        recommendations = []
        activity_level = profile.get("activity_level", "")
        average_steps = profile.get("average_steps", 0)
        age = profile.get("age", 0)
        
        if activity_level == "Sedentary":
            recommendations.append("🎯 Start with 30 minutes of light walking daily")
            recommendations.append("🎯 Set a goal to reach 7,000 steps per day")
            recommendations.append("🎯 Try low-impact exercises like swimming or cycling")
            recommendations.append("🎯 Schedule exercise breaks every 2-3 hours if desk-bound")
        
        elif activity_level == "Lightly Active":
            recommendations.append(f"🎯 Increase steps from {int(average_steps)} to 10,000 per day")
            recommendations.append("🎯 Add 2-3 strength training sessions per week")
            recommendations.append("🎯 Include flexibility training (yoga, stretching)")
            recommendations.append("🎯 Aim for 150 minutes of moderate cardio weekly")
        
        elif activity_level == "Moderately Active":
            recommendations.append(f"🎯 Excellent! Maintain your {int(average_steps)} daily steps")
            recommendations.append("🎯 Add HIIT (High-Intensity Interval Training) sessions")
            recommendations.append("🎯 Include progressive strength training")
            recommendations.append("🎯 Consider running or advanced sports for variety")
        
        elif activity_level in ["Very Active", "Extremely Active"]:
            recommendations.append(f"🎯 Outstanding! Continue your {int(average_steps)} daily steps")
            recommendations.append("🎯 Focus on recovery and injury prevention")
            recommendations.append("🎯 Include adequate rest days (2-3 per week)")
            recommendations.append("🎯 Listen to your body and prevent overtraining")
        
        if age > 65:
            recommendations.append("🎯 Focus on balance and flexibility exercises for fall prevention")
            recommendations.append("🎯 Include strength training to maintain bone density")
        
        return recommendations
    
    @staticmethod
    def generate_diet_recommendations(profile: Dict[str, Any]) -> List[str]:
        """
        Generate diet recommendations based on BMI and health metrics
        
        Args:
            profile: User health profile
            
        Returns:
            List of diet recommendations
        """
        recommendations = []
        bmi_category = profile.get("bmi_category", "")
        bmi = profile.get("bmi", 0)
        
        if bmi_category == "Underweight":
            recommendations.append("🥗 Focus on calorie-dense, nutrient-rich foods")
            recommendations.append("🥗 Include healthy fats (nuts, avocados, olive oil)")
            recommendations.append("🥗 Eat 5-6 smaller meals throughout the day")
            recommendations.append("🥗 Consider consulting a nutritionist for a meal plan")
        
        elif bmi_category == "Normal Weight":
            recommendations.append("🥗 Maintain your current balanced diet")
            recommendations.append("🥗 Continue eating 3 balanced meals daily")
            recommendations.append("🥗 Ensure adequate protein intake (1.2-1.6g per kg)")
            recommendations.append("🥗 Eat plenty of fruits and vegetables (5+ servings daily)")
        
        elif bmi_category == "Overweight":
            recommendations.append("🥗 Create a moderate calorie deficit (500-700 kcal/day)")
            recommendations.append("🥗 Increase protein intake to preserve muscle mass")
            recommendations.append("🥗 Avoid sugary drinks and processed foods")
            recommendations.append("🥗 Eat balanced meals: 50% vegetables, 25% protein, 25% carbs")
        
        elif bmi_category == "Obese":
            recommendations.append("🥗 Consult a dietitian for a personalized meal plan")
            recommendations.append("🥗 Start with small sustainable changes to diet")
            recommendations.append("🥗 Reduce portion sizes gradually")
            recommendations.append("🥗 Minimize sugary foods, unhealthy fats, and processed foods")
            recommendations.append("🥗 Stay hydrated and track your food intake")
        
        return recommendations
    
    @staticmethod
    def generate_sleep_recommendations(profile: Dict[str, Any]) -> List[str]:
        """
        Generate sleep improvement recommendations
        
        Args:
            profile: User health profile
            
        Returns:
            List of sleep recommendations
        """
        recommendations = []
        sleep_category = profile.get("sleep_category", "")
        avg_sleep = profile.get("average_sleep_hours", 0)
        
        if sleep_category == "Insufficient":
            recommendations.append(f"😴 Your average sleep ({avg_sleep}h) is below optimal")
            recommendations.append("😴 Aim for 7-9 hours of sleep nightly")
            recommendations.append("😴 Establish a consistent sleep schedule (same time daily)")
            recommendations.append("😴 Avoid screens 30-60 minutes before bed")
            recommendations.append("😴 Keep bedroom cool, dark, and quiet")
            recommendations.append("😴 Avoid caffeine after 2 PM")
        
        elif sleep_category == "Below Optimal":
            recommendations.append(f"😴 Try to extend sleep from {avg_sleep}h to 7-9 hours")
            recommendations.append("😴 Practice relaxation techniques before bed")
            recommendations.append("😴 Limit naps to 20-30 minutes in early afternoon")
            recommendations.append("😴 Exercise regularly but not close to bedtime")
        
        elif sleep_category == "Optimal":
            recommendations.append(f"😴 Excellent! Maintain your {avg_sleep}h sleep schedule")
            recommendations.append("😴 Continue your healthy sleep habits")
            recommendations.append("😴 Monitor sleep quality, not just duration")
        
        elif sleep_category == "Excessive":
            recommendations.append(f"😴 Your sleep ({avg_sleep}h) exceeds typical needs")
            recommendations.append("😴 Excessive sleep may indicate other health issues")
            recommendations.append("😴 Consider consulting a doctor to rule out conditions")
            recommendations.append("😴 Gradual shift to 7-9 hour range may help")
        
        return recommendations
    
    @staticmethod
    def generate_hydration_reminders(profile: Dict[str, Any]) -> List[str]:
        """
        Generate hydration recommendations
        
        Args:
            profile: User health profile
            
        Returns:
            List of hydration recommendations
        """
        recommendations = []
        hydration_level = profile.get("hydration_level", "")
        water_intake = profile.get("average_water_intake", 0)
        
        if hydration_level == "Dehydrated":
            recommendations.append(f"💧 Critical: Your intake ({water_intake}L) is very low")
            recommendations.append("💧 Increase to at least 2-3 liters daily")
            recommendations.append("💧 Drink water immediately upon waking")
            recommendations.append("💧 Set hourly reminders to drink water")
            recommendations.append("💧 Increase intake during and after exercise")
        
        elif hydration_level == "Below Recommended":
            recommendations.append(f"💧 Increase from {water_intake}L to 2.5-3 liters daily")
            recommendations.append("💧 Drink a glass of water with each meal")
            recommendations.append("💧 Keep a water bottle with you throughout the day")
        
        elif hydration_level == "Adequate":
            recommendations.append(f"💧 Good! Your intake of {water_intake}L is sufficient")
            recommendations.append("💧 Maintain this hydration level")
            recommendations.append("💧 Increase intake on exercise days or hot weather")
        
        elif hydration_level == "Well Hydrated":
            recommendations.append(f"💧 Great! Your intake of {water_intake}L is excellent")
            recommendations.append("💧 Ensure it's mostly water, not sugary drinks")
            recommendations.append("💧 Monitor for overhydration if exceeding 4L daily")
        
        return recommendations
    
    @staticmethod
    def generate_health_alerts(profile: Dict[str, Any]) -> List[str]:
        """
        Generate early health risk alerts based on profile
        
        Args:
            profile: User health profile
            
        Returns:
            List of health risk alerts
        """
        alerts = []
        health_risks = profile.get("health_risks", [])
        
        # Add all identified risks
        for risk in health_risks:
            alerts.append(f"⚠️ {risk}")
        
        # Additional alerts based on medical conditions
        medical = profile.get("medical_conditions", "").lower()
        if medical != "none" and medical.strip():
            alerts.append(f"⚠️ Remember to follow medical treatment and doctor's instructions")
            alerts.append(f"⚠️ Schedule regular medical check-ups")
        
        # Age-specific alerts
        age = profile.get("age", 0)
        if age >= 50:
            alerts.append("⚠️ As you age 50+, regular health screenings are important")
            alerts.append("⚠️ Consider blood pressure and cholesterol checks annually")
        
        if age >= 65:
            alerts.append("⚠️ Age 65+: Schedule preventive health screenings")
            alerts.append("⚠️ Get flu vaccine annually and consider pneumonia vaccine")
        
        return alerts if alerts else ["✅ No major health risks identified. Keep up healthy habits!"]
    
    @staticmethod
    def generate_comprehensive_recommendations(profile: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Generate comprehensive personalized recommendations
        
        Args:
            profile: User health profile
            
        Returns:
            Dictionary containing all recommendation categories
        """
        recommendations = {
            "exercise": RecommendationEngine.generate_exercise_recommendations(profile),
            "diet": RecommendationEngine.generate_diet_recommendations(profile),
            "sleep": RecommendationEngine.generate_sleep_recommendations(profile),
            "hydration": RecommendationEngine.generate_hydration_reminders(profile),
            "health_alerts": RecommendationEngine.generate_health_alerts(profile)
        }
        
        return recommendations
