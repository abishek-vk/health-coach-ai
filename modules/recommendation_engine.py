"""
recommendation_engine.py - Intelligent recommendation generation
Analyzes health profiles and generates personalized health recommendations
Enhanced with ML-powered predictions and user clustering for AI-driven personalization
Also supports Gemini AI for additional enhancement
"""

import logging
from typing import List, Dict, Optional, Any
from pathlib import Path

from modules.profile_summarizer import HealthProfileSummarizer
from modules.health_plan_generator import HealthPlanGenerator

try:
    from modules.gemini_integration import get_gemini_advisor
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# ML Integration
try:
    from modules.ai_health_engine import AIHealthEngine, AIRecommendationGenerator
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

# Configure logging
logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Generates personalized health recommendations based on user profiles"""
    
    # Class variables for ML engine initialization
    _ai_engine = None
    _ai_recommendation_generator = None
    _ml_initialized = False
    
    @classmethod
    def initialize_ml_engine(cls, data_dir: str = "data", model_dir: str = "models") -> bool:
        """
        Initialize and train ML models for AI-powered recommendations
        
        Args:
            data_dir: Directory containing user_records.json and user_profiles.json
            model_dir: Directory to store/load trained models
            
        Returns:
            True if initialization successful, False otherwise
        """
        if not ML_AVAILABLE:
            logger.warning("⚠️ scikit-learn not available. Using rule-based recommendations.")
            return False
        
        try:
            if cls._ml_initialized:
                logger.info("✅ ML engine already initialized")
                return True
            
            logger.info("🚀 Initializing ML Health Engine...")
            
            # Initialize engine
            cls._ai_engine = AIHealthEngine(model_dir=model_dir)
            
            # Try to load existing models
            if cls._ai_engine.load_models(model_dir):
                logger.info("✅ Loaded pre-trained ML models from disk")
                cls._ai_recommendation_generator = AIRecommendationGenerator(cls._ai_engine)
                cls._ml_initialized = True
                return True
            
            # If no saved models, train new ones
            logger.info("📊 Training ML models from health data...")
            
            # Prepare training data
            records_file = Path(data_dir) / "user_records.json"
            profiles_file = Path(data_dir) / "user_profiles.json"
            
            if not records_file.exists() or not profiles_file.exists():
                logger.warning(f"⚠️ Data files not found in {data_dir}")
                # Will use synthetic data
                pass
            
            # Prepare data and train models
            df, success = cls._ai_engine.prepare_training_data_from_json(
                str(records_file), str(profiles_file)
            )
            
            if not success:
                logger.error("❌ Failed to prepare training data")
                return False
            
            # Train predictive models
            if not cls._ai_engine.train_models(df):
                logger.error("❌ Failed to train predictive models")
                return False
            
            # Train clustering
            if not cls._ai_engine.train_clustering(df, n_clusters=4):
                logger.error("❌ Failed to train clustering model")
                return False
            
            # Save models
            cls._ai_engine.save_models(model_dir)
            
            # Initialize recommendation generator
            cls._ai_recommendation_generator = AIRecommendationGenerator(cls._ai_engine)
            
            cls._ml_initialized = True
            logger.info("✅ ML engine initialized and trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error initializing ML engine: {e}")
            return False
    
    @classmethod
    def get_ml_status(cls) -> Dict[str, Any]:
        """
        Get status of ML engine
        
        Returns:
            Dictionary with ML status information
        """
        return {
            'ml_available': ML_AVAILABLE,
            'ml_initialized': cls._ml_initialized,
            'engine': cls._ai_engine is not None,
            'recommendation_generator': cls._ai_recommendation_generator is not None
        }
    
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
    
    @classmethod
    def generate_comprehensive_recommendations(
        cls, 
        profile: Dict[str, Any], 
        use_ai_enhancement: bool = True,
        use_ml_predictions: bool = True
    ) -> Dict[str, List[str]]:
        """
        Generate comprehensive personalized recommendations using ML or rule-based logic
        
        Args:
            profile: User health profile
            use_ai_enhancement: Whether to enhance with Gemini AI (if available)
            use_ml_predictions: Whether to use ML models for predictions (if available)
            
        Returns:
            Dictionary containing all recommendation categories
        """
        # Try ML-powered recommendations first
        if use_ml_predictions and cls._ml_initialized and cls._ai_recommendation_generator:
            try:
                logger.info("🤖 Using ML-powered AI recommendations")
                
                # Prepare features for ML prediction
                user_features = {
                    'age': profile.get('age', 35),
                    'bmi': profile.get('bmi', 25),
                    'daily_steps': profile.get('average_steps', 7000),
                    'sleep_hours': profile.get('average_sleep_hours', 7.5),
                    'water_intake': profile.get('average_water_intake', 2.5),
                }
                
                # Get ML predictions
                health_risks = cls._ai_engine.predict_health_risks(user_features)
                cluster_info = cls._ai_engine.assign_user_cluster(user_features)
                
                # Generate ML-driven recommendations
                recommendations = cls._ai_recommendation_generator.generate_ml_driven_recommendations(
                    profile, health_risks, cluster_info
                )
                
                logger.info("✅ ML recommendations generated successfully")
                
            except Exception as e:
                logger.error(f"❌ Error with ML recommendations, falling back: {e}")
                # Fall back to rule-based logic
                recommendations = {
                    "exercise": RecommendationEngine.generate_exercise_recommendations(profile),
                    "diet": RecommendationEngine.generate_diet_recommendations(profile),
                    "sleep": RecommendationEngine.generate_sleep_recommendations(profile),
                    "hydration": RecommendationEngine.generate_hydration_reminders(profile),
                    "health_alerts": RecommendationEngine.generate_health_alerts(profile)
                }
        else:
            # Use rule-based recommendations
            logger.info("📋 Using rule-based recommendations")
            recommendations = {
                "exercise": RecommendationEngine.generate_exercise_recommendations(profile),
                "diet": RecommendationEngine.generate_diet_recommendations(profile),
                "sleep": RecommendationEngine.generate_sleep_recommendations(profile),
                "hydration": RecommendationEngine.generate_hydration_reminders(profile),
                "health_alerts": RecommendationEngine.generate_health_alerts(profile)
            }
        
        # Enhance with Gemini AI if available and enabled
        if use_ai_enhancement and GEMINI_AVAILABLE:
            try:
                advisor = get_gemini_advisor()
                recommendations = advisor.enhance_recommendations(recommendations, profile)
            except Exception as e:
                logger.warning(f"⚠️ Gemini enhancement skipped: {e}")
        
        return recommendations
    
    @classmethod
    def get_ml_health_risks(cls, profile: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get ML-predicted health risks for a user
        
        Args:
            profile: User health profile
            
        Returns:
            Dictionary with ML-predicted health risks or None if ML unavailable
        """
        if not cls._ml_initialized or not cls._ai_engine:
            logger.debug("ML engine not initialized")
            return None
        
        try:
            user_features = {
                'age': profile.get('age', 35),
                'bmi': profile.get('bmi', 25),
                'daily_steps': profile.get('average_steps', 7000),
                'sleep_hours': profile.get('average_sleep_hours', 7.5),
                'water_intake': profile.get('average_water_intake', 2.5),
            }
            
            return cls._ai_engine.predict_health_risks(user_features)
        except Exception as e:
            logger.error(f"Error getting ML health risks: {e}")
            return None
    
    @classmethod
    def get_user_cluster_assignment(cls, profile: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get user's cluster assignment and personalization info
        
        Args:
            profile: User health profile
            
        Returns:
            Dictionary with cluster assignment or None if ML unavailable
        """
        if not cls._ml_initialized or not cls._ai_engine:
            logger.debug("ML engine not initialized")
            return None
        
        try:
            user_features = {
                'daily_steps': profile.get('average_steps', 7000),
                'bmi': profile.get('bmi', 25),
                'sleep_hours': profile.get('average_sleep_hours', 7.5),
                'water_intake': profile.get('average_water_intake', 2.5),
            }
            
            return cls._ai_engine.assign_user_cluster(user_features)
        except Exception as e:
            logger.error(f"Error assigning user cluster: {e}")
            return None
    
    @classmethod
    def generate_health_plan(
        cls,
        profile: Dict[str, Any],
        use_ml_predictions: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive AI-personalized health plan
        Uses ML predictions if available, falls back to rule-based generation
        
        Args:
            profile: User health profile
            use_ml_predictions: Whether to use ML models for predictions
            
        Returns:
            Comprehensive health plan dictionary
        """
        logger.info("🎯 Generating Personalized Health Plan")
        
        try:
            # Get ML predictions and cluster assignment if available
            health_risks = None
            cluster_assignment = None
            cluster_id = 0
            
            if use_ml_predictions and cls._ml_initialized and cls._ai_engine:
                try:
                    # Prepare user features
                    user_features = {
                        'age': profile.get('age', 35),
                        'bmi': profile.get('bmi', 25),
                        'daily_steps': profile.get('average_steps', 7000),
                        'sleep_hours': profile.get('average_sleep_hours', 7.5),
                        'water_intake': profile.get('average_water_intake', 2.5),
                    }
                    
                    # Get ML predictions
                    health_risks = cls._ai_engine.predict_health_risks(user_features)
                    cluster_assignment = cls._ai_engine.assign_user_cluster(user_features)
                    
                    if cluster_assignment:
                        cluster_id = cluster_assignment.get('cluster_id', 0)
                        logger.info(f"✅ ML predictions obtained - Cluster {cluster_id}")
                    
                except Exception as e:
                    logger.warning(f"⚠️ ML prediction failed: {e}, using fallback")
                    health_risks = None
            
            # Generate health plan
            health_plan = HealthPlanGenerator.generate_personalized_health_plan(
                predictions=health_risks,
                cluster_id=cluster_id,
                user_profile=profile
            )
            
            logger.info("✅ Health Plan Generated Successfully")
            return health_plan
            
        except Exception as e:
            logger.error(f"❌ Error generating health plan: {e}")
            logger.warning("⚠️ Returning rule-based fallback plan")
            return HealthPlanGenerator._generate_rule_based_plan(
                cluster_id=0,
                user_profile=profile
            )
    
    @classmethod
    def get_health_plan_summary(cls, health_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a summary of the health plan for quick reference
        
        Args:
            health_plan: Generated health plan dictionary
            
        Returns:
            Summary dictionary
        """
        try:
            summary = {
                'cluster': health_plan.get('metadata', {}).get('cluster_name', 'Unknown'),
                'risk_levels': health_plan.get('metadata', {}).get('risk_summary', {}),
                'diet_focus': health_plan.get('diet_plan', {}).get('focus_area', ''),
                'activity_target': health_plan.get('activity_plan', {}).get('daily_target_steps', 0),
                'sleep_target': health_plan.get('sleep_plan', {}).get('target_sleep_hours', '7-9 hours'),
                'weekly_goals_count': len(health_plan.get('weekly_goals', {}).get('goals', [])),
                'critical_alerts': len(health_plan.get('alerts', {}).get('critical_alerts', [])),
                'has_urgent_actions': len(health_plan.get('alerts', {}).get('critical_alerts', [])) > 0
            }
            return summary
        except Exception as e:
            logger.error(f"Error getting health plan summary: {e}")
            return {}

    @staticmethod
    def get_personalized_ai_plan(profile: Dict[str, Any]) -> Optional[str]:
        """
        Get AI-generated personalized health plan
        
        Args:
            profile: User health profile
            
        Returns:
            Personalized plan or None if Gemini unavailable
        """
        if GEMINI_AVAILABLE:
            try:
                advisor = get_gemini_advisor()
                return advisor.get_personalized_plan(profile)
            except Exception as e:
                print(f"⚠️ Error generating AI plan: {e}")
        
        return None
    
    @staticmethod
    def get_health_insights(profile: Dict[str, Any]) -> Optional[str]:
        """
        Get AI health insights analysis
        
        Args:
            profile: User health profile
            
        Returns:
            Health insights or None if Gemini unavailable
        """
        if GEMINI_AVAILABLE:
            try:
                advisor = get_gemini_advisor()
                return advisor.get_health_insights(profile)
            except Exception as e:
                print(f"⚠️ Error generating insights: {e}")
        
        return None
    
    @staticmethod
    def get_motivation_message(category: str, progress: Optional[Dict] = None) -> str:
        """
        Get motivational message for health category
        
        Args:
            category: Health category (exercise, diet, sleep, etc.)
            progress: Optional progress data
            
        Returns:
            Motivational message
        """
        if GEMINI_AVAILABLE:
            try:
                advisor = get_gemini_advisor()
                return advisor.get_motivation_message(category, progress)
            except Exception as e:
                print(f"⚠️ Error generating motivation: {e}")
        
        # Fallback motivation
        messages = {
            "exercise": "💪 Keep moving! Every step counts towards your fitness goals!",
            "diet": "🥗 You're making great nutritional choices! Keep it up!",
            "sleep": "😴 Rest is crucial for health. Stick to your sleep schedule!",
            "hydration": "💧 Stay hydrated! Your body will thank you!",
            "overall": "🎯 You're on a great health journey. Keep pushing!"
        }
        return messages.get(category, messages["overall"])
