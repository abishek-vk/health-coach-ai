"""
health_plan_generator.py - AI Personalized Health Plan Generator
Generates comprehensive, risk-aware health plans using ML predictions and user clustering
Produces structured plans for diet, activity, sleep, and weekly goals with automatic risk alerts
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

# Configure logging
logger = logging.getLogger(__name__)


class HealthPlanGenerator:
    """Generates AI-personalized health plans based on ML predictions and user clustering"""
    
    # Cluster-specific personalization templates
    CLUSTER_PROFILES = {
        0: {
            'name': 'Sedentary Wellness Seekers',
            'focus': 'activity and weight management',
            'diet_emphasis': 'calorie control and nutrition basics',
            'activity_emphasis': 'building a foundation for active living',
            'sleep_emphasis': 'establishing consistent sleep routines',
            'personality': 'motivational and gradual progression'
        },
        1: {
            'name': 'Active & Fit',
            'focus': 'performance and consistency',
            'diet_emphasis': 'athletic performance nutrition',
            'activity_emphasis': 'optimizing and challenging current level',
            'sleep_emphasis': 'recovery and sleep quality',
            'personality': 'ambitious and results-focused'
        },
        2: {
            'name': 'Healthy Lifestyle Champions',
            'focus': 'maintenance and optimization',
            'diet_emphasis': 'balanced nutrition and healthy habits',
            'activity_emphasis': 'maintaining and exploring new activities',
            'sleep_emphasis': 'sleep tracking and optimization',
            'personality': 'wellness enthusiast and sustainable habits'
        },
        3: {
            'name': 'Balanced Progressors',
            'focus': 'sustainable improvement',
            'diet_emphasis': 'gradual dietary improvements',
            'activity_emphasis': 'steady activity increases',
            'sleep_emphasis': 'sleep habit development',
            'personality': 'steady and committed to progress'
        }
    }
    
    # Risk level mappings
    RISK_LEVELS = {
        'low': {'threshold': 0.3, 'emoji': '✅', 'label': 'Low Risk'},
        'moderate': {'threshold': 0.6, 'emoji': '⚠️', 'label': 'Moderate Risk'},
        'high': {'threshold': 0.75, 'emoji': '⚠️⚠️', 'label': 'High Risk'},
        'critical': {'threshold': 1.0, 'emoji': '🚨', 'label': 'Critical Risk'}
    }
    
    @staticmethod
    def get_risk_level(probability: float) -> str:
        """
        Convert probability to risk level string
        
        Args:
            probability: Risk probability (0-1)
            
        Returns:
            Risk level: 'low', 'moderate', 'high', or 'critical'
        """
        if probability < 0.3:
            return 'low'
        elif probability < 0.6:
            return 'moderate'
        elif probability < 0.75:
            return 'high'
        else:
            return 'critical'
    
    @classmethod
    def generate_personalized_health_plan(
        cls, 
        predictions: Optional[Dict[str, Any]] = None,
        cluster_id: int = 0,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive AI-personalized health plan
        
        Args:
            predictions: ML predictions dict with obesity_risk, inactivity_risk, sleep_deficiency_risk
                        Each should have 'probability' key. E.g.,
                        {
                            'obesity_risk': {'probability': 0.65},
                            'inactivity_risk': {'probability': 0.40},
                            'sleep_deficiency_risk': {'probability': 0.50}
                        }
            cluster_id: User's lifestyle cluster ID (0-3)
            user_profile: Optional user profile dict for additional context
            
        Returns:
            Comprehensive health plan dictionary with:
            - diet_plan: Personalized diet recommendations
            - activity_plan: Physical activity recommendations
            - sleep_plan: Sleep improvement recommendations
            - weekly_goals: Weekly target goals
            - alerts: Risk alerts if any risk > 0.75
        """
        logger.info("🎯 Generating AI Personalized Health Plan")
        
        try:
            # Gracefully handle missing predictions
            if predictions is None:
                logger.warning("⚠️ ML predictions unavailable, using rule-based plan generation")
                return cls._generate_rule_based_plan(cluster_id, user_profile)
            
            # Validate predictions structure
            if not isinstance(predictions, dict):
                logger.warning("⚠️ Invalid predictions format, using rule-based plan generation")
                return cls._generate_rule_based_plan(cluster_id, user_profile)
            
            # Extract risk probabilities with fallback defaults
            obesity_prob = cls._extract_risk_probability(predictions, 'obesity_risk', 0.5)
            inactivity_prob = cls._extract_risk_probability(predictions, 'inactivity_risk', 0.5)
            sleep_prob = cls._extract_risk_probability(predictions, 'sleep_deficiency_risk', 0.5)
            
            # Get cluster profile
            cluster_profile = cls.CLUSTER_PROFILES.get(cluster_id, cls.CLUSTER_PROFILES[0])
            
            logger.info(f"👥 Cluster: {cluster_profile['name']} (ID: {cluster_id})")
            logger.info(f"📊 Risk Levels - Obesity: {obesity_prob:.1%}, Inactivity: {inactivity_prob:.1%}, Sleep: {sleep_prob:.1%}")
            
            # Generate plan components
            plan = {
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'cluster_id': cluster_id,
                    'cluster_name': cluster_profile['name'],
                    'risk_summary': {
                        'obesity_risk': {
                            'probability': round(obesity_prob, 3),
                            'level': cls.get_risk_level(obesity_prob),
                            'emoji': cls.RISK_LEVELS[cls.get_risk_level(obesity_prob)]['emoji']
                        },
                        'inactivity_risk': {
                            'probability': round(inactivity_prob, 3),
                            'level': cls.get_risk_level(inactivity_prob),
                            'emoji': cls.RISK_LEVELS[cls.get_risk_level(inactivity_prob)]['emoji']
                        },
                        'sleep_deficiency_risk': {
                            'probability': round(sleep_prob, 3),
                            'level': cls.get_risk_level(sleep_prob),
                            'emoji': cls.RISK_LEVELS[cls.get_risk_level(sleep_prob)]['emoji']
                        }
                    }
                },
                'diet_plan': cls._generate_diet_plan(obesity_prob, cluster_profile),
                'activity_plan': cls._generate_activity_plan(inactivity_prob, cluster_profile),
                'sleep_plan': cls._generate_sleep_plan(sleep_prob, cluster_profile),
                'weekly_goals': cls._generate_weekly_goals(
                    obesity_prob, inactivity_prob, sleep_prob, cluster_profile
                ),
                'alerts': cls._generate_alerts(obesity_prob, inactivity_prob, sleep_prob)
            }
            
            logger.info("✅ Health Plan Generated Successfully")
            return plan
            
        except Exception as e:
            logger.error(f"❌ Error generating health plan: {e}")
            logger.warning("⚠️ Falling back to rule-based plan generation")
            return cls._generate_rule_based_plan(cluster_id, user_profile)
    
    @staticmethod
    def _extract_risk_probability(
        predictions: Dict[str, Any],
        risk_type: str,
        default: float = 0.5
    ) -> float:
        """
        Safely extract risk probability from predictions dict
        
        Args:
            predictions: Predictions dictionary
            risk_type: Type of risk ('obesity_risk', 'inactivity_risk', 'sleep_deficiency_risk')
            default: Default value if extraction fails
            
        Returns:
            Risk probability as float between 0-1
        """
        try:
            if risk_type in predictions:
                risk_data = predictions[risk_type]
                if isinstance(risk_data, dict) and 'probability' in risk_data:
                    return float(risk_data['probability'])
                elif isinstance(risk_data, (int, float)):
                    return float(risk_data)
            return default
        except (TypeError, ValueError, KeyError):
            return default
    
    @classmethod
    def _generate_diet_plan(cls, obesity_risk: float, cluster: Dict[str, str]) -> Dict[str, Any]:
        """
        Generate personalized diet plan based on obesity risk and cluster
        
        Args:
            obesity_risk: Obesity risk probability (0-1)
            cluster: Cluster profile dictionary
            
        Returns:
            Diet plan dictionary
        """
        risk_level = cls.get_risk_level(obesity_risk)
        
        base_plan = {
            'focus_area': cluster['diet_emphasis'],
            'risk_level': risk_level,
            'risk_emoji': cls.RISK_LEVELS[risk_level]['emoji'],
        }
        
        if risk_level == 'critical':
            base_plan['title'] = '🚨 CRITICAL: Intensive Diet Intervention Plan'
            base_plan['priority'] = 'URGENT'
            base_plan['recommendations'] = [
                "🥗 Consult a registered dietitian immediately",
                f"🥗 Create a 700-800 kcal daily calorie deficit",
                "🥗 Track every meal using an app (e.g., MyFitnessPal)",
                "🥗 Eliminate sugary drinks, processed foods, and high-fat foods",
                "🥗 Eat 5-6 smaller meals instead of 3 large ones",
                "🥗 Prioritize lean protein (chicken, fish, tofu) at every meal",
                "🥗 Include vegetables in 50% of your plate",
                "🥗 Avoid eating after 7 PM",
                "🥗 Weekly weigh-ins and dietary review with healthcare provider"
            ]
            base_plan['daily_structure'] = {
                'breakfast': 'High protein (eggs, Greek yogurt) + fiber (oatmeal, berries)',
                'snack_1': 'Apple with almond butter or protein bar',
                'lunch': 'Lean protein + vegetables + brown rice/quinoa',
                'snack_2': 'Cucumber, carrots, or nuts (small portion)',
                'dinner': 'Grilled fish/chicken + steamed vegetables + light carbs'
            }
            base_plan['foods_to_avoid'] = [
                'Sugary drinks (soda, energy drinks)',
                'Processed snacks (chips, cookies)',
                'Fried foods',
                'High-fat dairy',
                'White bread and pasta',
                'Alcohol'
            ]
        
        elif risk_level == 'high':
            base_plan['title'] = '⚠️⚠️ HIGH RISK: Intensive Weight Management Plan'
            base_plan['priority'] = 'HIGH'
            base_plan['recommendations'] = [
                "🥗 Maintain a 500-600 kcal daily deficit",
                "🥗 Schedule consultation with a nutritionist",
                "🥗 Meal prep on weekends for consistency",
                "🥗 Reduce portion sizes by 25-30%",
                "🥗 Increase protein to preserve muscle mass (1.2-1.5g per kg body weight)",
                "🥗 Eat more whole grains, less refined carbs",
                "🥗 Limit sugary foods to 1-2 times per week",
                "🥗 Stay hydrated: 8-10 glasses of water daily",
                "🥗 Monitor progress weekly and adjust as needed"
            ]
            base_plan['daily_structure'] = {
                'breakfast': 'Protein-rich breakfast (whole grain toast + eggs)',
                'snack_1': 'Fruit or yogurt',
                'lunch': 'Balanced meal (protein + veggies + complex carbs)',
                'snack_2': 'Nuts or fruit',
                'dinner': 'Light, balanced dinner'
            }
            base_plan['foods_to_limit'] = [
                'Sugary beverages',
                'Deep fried foods',
                'High-fat meats',
                'Refined grains',
                'High-sugar snacks'
            ]
        
        elif risk_level == 'moderate':
            base_plan['title'] = '⚠️ MODERATE RISK: Balanced Weight Management Plan'
            base_plan['priority'] = 'MEDIUM'
            base_plan['recommendations'] = [
                "🥗 Maintain a 250-350 kcal daily deficit",
                "🥗 Eat balanced meals (50% veg, 25% protein, 25% smart carbs)",
                "🥗 Include whole grains in most meals",
                "🥗 Reduce added sugars and processed foods",
                "🥗 Include healthy fats (olive oil, avocado, nuts)",
                "🥗 Drink water before each meal",
                "🥗 Eat mindfully and chew slowly (25-30 min per meal)",
                "🥗 Weekly meal planning to maintain consistency"
            ]
            base_plan['daily_structure'] = {
                'breakfast': 'Whole grain cereal/toast + fruit + dairy',
                'snack_1': 'Fruit or yogurt',
                'lunch': 'Balanced lunch with veggies, protein, and grains',
                'snack_2': 'Healthy snack (nuts, fruit)',
                'dinner': 'Balanced dinner similar to lunch'
            }
            base_plan['healthy_foods_to_emphasize'] = [
                'Lean proteins (chicken, fish, legumes)',
                'Whole grains (brown rice, quinoa, whole wheat)',
                'Colorful vegetables',
                'Fruits (especially berries)',
                'Low-fat dairy',
                'Healthy fats (nuts, seeds, olive oil)'
            ]
        
        else:  # low risk
            base_plan['title'] = '✅ LOW RISK: Healthy Diet Maintenance Plan'
            base_plan['priority'] = 'MAINTAIN'
            base_plan['recommendations'] = [
                "🥗 Excellent diet maintained - keep it up!",
                "🥗 Continue 3 balanced meals and healthy snacks daily",
                "🥗 Maintain consistent portion control",
                "🥗 Include variety: different colored vegetables and protein sources",
                "🥗 Stay hydrated (8+ glasses of water daily)",
                "🥗 Limit processed foods to <20% of daily calories",
                "🥗 Monthly check-ins to monitor stability",
                "🥗 Experiment with new healthy recipes to maintain interest"
            ]
            base_plan['daily_structure'] = {
                'breakfast': 'Your current balanced breakfast routine',
                'snack_1': 'Healthy snack of choice',
                'lunch': 'Your current balanced lunch',
                'snack_2': 'Healthy snack or rest day',
                'dinner': 'Your current balanced dinner'
            }
            base_plan['maintenance_tips'] = [
                'Continue current eating patterns',
                'Periodically review nutrition balance',
                'Enjoy treats in moderation (10-15% of weekly calories)',
                'Stay flexible and listen to hunger/fullness cues'
            ]
        
        return base_plan
    
    @classmethod
    def _generate_activity_plan(cls, inactivity_risk: float, cluster: Dict[str, str]) -> Dict[str, Any]:
        """
        Generate personalized activity plan based on inactivity risk and cluster
        
        Args:
            inactivity_risk: Inactivity risk probability (0-1)
            cluster: Cluster profile dictionary
            
        Returns:
            Activity plan dictionary
        """
        risk_level = cls.get_risk_level(inactivity_risk)
        
        base_plan = {
            'focus_area': cluster['activity_emphasis'],
            'risk_level': risk_level,
            'risk_emoji': cls.RISK_LEVELS[risk_level]['emoji'],
        }
        
        if risk_level == 'critical':
            base_plan['title'] = '🚨 CRITICAL: Urgent Activity Intervention Plan'
            base_plan['priority'] = 'URGENT'
            base_plan['daily_target_steps'] = 10000
            base_plan['weekly_target_minutes'] = 300
            base_plan['recommendations'] = [
                "🎯 Start immediately: your sedentary lifestyle poses serious health risks",
                "🎯 Begin with 10-15 min walks daily, gradually increase",
                "🎯 Target 10,000 steps daily (track with pedometer or app)",
                "🎯 Add 30 min strength training 2-3 times per week",
                "🎯 Break up sitting: stand/walk every 30-45 minutes",
                "🎯 Consider working with a personal trainer",
                "🎯 Join group fitness classes for motivation",
                "🎯 Schedule daily activity like meals - make it non-negotiable"
            ]
            base_plan['weekly_schedule'] = {
                'monday': '30 min brisk walk + light stretching',
                'tuesday': 'Strength training (full body, 30 min)',
                'wednesday': '30 min brisk walk or cycling',
                'thursday': 'Strength training (upper body focus, 30 min)',
                'friday': '30 min brisk walk + light stretching',
                'saturday': 'Fun activity (dance, recreational sports, hiking)',
                'sunday': 'Active recovery (light yoga or gentle walk)'
            }
            base_plan['progression'] = [
                'Week 1-2: Focus on 5,000+ steps daily',
                'Week 3-4: Increase to 7,500 steps',
                'Week 5-6: Target 10,000 steps consistently',
                'Week 7+: Add intensity and variety'
            ]
        
        elif risk_level == 'high':
            base_plan['title'] = '⚠️⚠️ HIGH RISK: Intensive Physical Activity Plan'
            base_plan['priority'] = 'HIGH'
            base_plan['daily_target_steps'] = 9000
            base_plan['weekly_target_minutes'] = 240
            base_plan['recommendations'] = [
                "🎯 Increase activity significantly - your current level is concerning",
                "🎯 Aim for 9,000+ steps daily (use app to track)",
                "🎯 Include 30-40 min of moderate-intensity exercise 4-5 times/week",
                "🎯 Add strength training 2-3 times per week",
                "🎯 Take movement breaks every hour if desk-bound",
                "🎯 Use stairs instead of elevators",
                "🎯 Park farther away to increase walking",
                "🎯 Consider group fitness classes for accountability"
            ]
            base_plan['weekly_schedule'] = {
                'monday': '30 min moderate cardio (walking, cycling, swimming)',
                'tuesday': '30 min strength training',
                'wednesday': '30 min moderate cardio',
                'thursday': '30 min strength training OR group fitness class',
                'friday': '30 min moderate cardio',
                'saturday': 'Fun activity (sports, hiking, active recreation)',
                'sunday': 'Rest day or light activity (casual walk)'
            }
            base_plan['daily_habits'] = [
                'Walk or bike for short trips',
                'Use standing desk 50% of work time',
                'Take short walking breaks every hour',
                'Stretch during commercial breaks',
                'Park farther away from destinations'
            ]
        
        elif risk_level == 'moderate':
            base_plan['title'] = '⚠️ MODERATE RISK: Activity Improvement Plan'
            base_plan['priority'] = 'MEDIUM'
            base_plan['daily_target_steps'] = 8000
            base_plan['weekly_target_minutes'] = 180
            base_plan['recommendations'] = [
                "🎯 Gradually increase activity to optimal levels",
                "🎯 Target 8,000-9,000 steps daily",
                "🎯 Include 150-180 min of moderate activity per week",
                "🎯 Add 1-2 strength training sessions per week",
                "🎯 Vary activities to stay engaged",
                "🎯 Build movement into daily routine",
                "🎯 Find activities you enjoy (not just exercise)",
                "🎯 Share goals with friends for accountability"
            ]
            base_plan['weekly_schedule'] = {
                'monday': '30 min walking or cycling',
                'tuesday': '30 min strength training',
                'wednesday': '30 min moderate activity',
                'thursday': 'Rest or light activity',
                'friday': '30 min walking or group fitness',
                'saturday': 'Fun activity or recreational sport',
                'sunday': 'Light activity (casual walk) or rest'
            }
            base_plan['activity_ideas'] = [
                'Walking groups',
                'Yoga or Pilates classes',
                'Dancing',
                'Swimming',
                'Cycling',
                'Sports leagues',
                'Hiking'
            ]
        
        else:  # low risk
            base_plan['title'] = '✅ LOW RISK: Active Maintenance Plan'
            base_plan['priority'] = 'MAINTAIN'
            base_plan['daily_target_steps'] = 10000
            base_plan['weekly_target_minutes'] = 300
            base_plan['recommendations'] = [
                "🎯 Excellent activity level - maintain and optimize!",
                "🎯 Continue your current daily activity (10,000+ steps)",
                "🎯 Maintain or increase exercise variety",
                "🎯 Periodically increase intensity or try new activities",
                "🎯 Balance cardio and strength training",
                "🎯 Include flexibility and balance work",
                "🎯 Set new fitness goals for continued progression",
                "🎯 Share habits with others to inspire them"
            ]
            base_plan['weekly_schedule'] = {
                'monday': 'Your preferred cardio activity',
                'tuesday': 'Strength training',
                'wednesday': 'Moderate activity (walking, cycling)',
                'thursday': 'Strength or flexibility training',
                'friday': 'Cardio or group fitness class',
                'saturday': 'Fun activity or intensive exercise',
                'sunday': 'Active recovery (yoga, light walk) or rest'
            }
            base_plan['advancement_suggestions'] = [
                'Increase intensity or duration gradually',
                'Try new sports or activities',
                'Set performance goals',
                'Challenge yourself weekly',
                'Consider fitness competitions'
            ]
        
        return base_plan
    
    @classmethod
    def _generate_sleep_plan(cls, sleep_risk: float, cluster: Dict[str, str]) -> Dict[str, Any]:
        """
        Generate personalized sleep plan based on sleep deficiency risk and cluster
        
        Args:
            sleep_risk: Sleep deficiency risk probability (0-1)
            cluster: Cluster profile dictionary
            
        Returns:
            Sleep plan dictionary
        """
        risk_level = cls.get_risk_level(sleep_risk)
        
        base_plan = {
            'focus_area': cluster['sleep_emphasis'],
            'risk_level': risk_level,
            'risk_emoji': cls.RISK_LEVELS[risk_level]['emoji'],
        }
        
        if risk_level == 'critical':
            base_plan['title'] = '🚨 CRITICAL: Urgent Sleep Recovery Plan'
            base_plan['priority'] = 'URGENT'
            base_plan['target_sleep_hours'] = '8-9 hours'
            base_plan['recommendations'] = [
                "😴 Your sleep deficiency is critical and requires immediate intervention",
                "😴 Consult a sleep specialist if no improvement within 2 weeks",
                "😴 Establish strict sleep schedule: same bedtime and wake time daily",
                "😴 Target 8-9 hours of sleep nightly",
                "😴 Create dark, cool (65-68°F), quiet sleeping environment",
                "😴 No screens 90 minutes before bed",
                "😴 Avoid caffeine after 12 PM, alcohol 4+ hours before bed",
                "😴 Do 10-15 min relaxation routine before bed",
                "😴 Consider melatonin or magnesium (consult doctor first)",
                "😴 Exercise daily but not within 4 hours of bedtime"
            ]
            base_plan['bedtime_routine'] = [
                '8:30 PM: Stop all screen use',
                '8:30-9:15 PM: Relaxation (meditation, reading, stretching)',
                '9:15 PM: Warm bath or shower',
                '9:30 PM: In bed with lights off',
                '10:00 PM: Target sleep start time'
            ]
            base_plan['morning_routine'] = [
                'Consistent wake time (even weekends)',
                'Immediate light exposure (10-15 min)',
                'Morning exercise (helps regulate sleep cycle)',
                'No napping during day'
            ]
            base_plan['sleep_hygiene_essentials'] = [
                'Blackout curtains or sleep mask',
                'White noise machine',
                'Temperature control (fan or AC)',
                'Comfortable mattress and pillows',
                'Bedding changes 2x weekly'
            ]
        
        elif risk_level == 'high':
            base_plan['title'] = '⚠️⚠️ HIGH RISK: Sleep Improvement Plan'
            base_plan['priority'] = 'HIGH'
            base_plan['target_sleep_hours'] = '7.5-9 hours'
            base_plan['recommendations'] = [
                "😴 Your sleep is significantly below optimal - prioritize immediately",
                "😴 Establish consistent sleep schedule (same bedtime/wake time)",
                "😴 Target 7.5-9 hours nightly",
                "😴 Create optimal sleep environment (dark, cool, quiet)",
                "😴 Reduce screen time 60 minutes before bed",
                "😴 Limit caffeine to before 2 PM",
                "😴 Avoid alcohol, especially before bed",
                "😴 Incorporate relaxation techniques (deep breathing, meditation)",
                "😴 Exercise regularly but not near bedtime",
                "😴 Track sleep and identify patterns"
            ]
            base_plan['bedtime_routine'] = [
                '9:00 PM: Dim lights, reduce stimulation',
                '9:30 PM: Relaxation activity (reading, meditation)',
                '10:00 PM: Prepare bedroom (cool, dark)',
                '10:30 PM: Lights out, target sleep time'
            ]
            base_plan['sleep_hygiene_tips'] = [
                'Consistent wake time (even weekends)',
                'No caffeine after 2 PM',
                'Exercise 4-6 hours before bed',
                'Light snack 2 hours before bed',
                'Comfortable temperature (65-68°F optimal)'
            ]
            base_plan['what_to_avoid'] = [
                'Alcohol (disrupts sleep quality)',
                'Heavy meals 3 hours before bed',
                'Intense exercise 4 hours before bed',
                'Long naps (max 20-30 minutes)',
                'Clock-watching at night'
            ]
        
        elif risk_level == 'moderate':
            base_plan['title'] = '⚠️ MODERATE RISK: Sleep Optimization Plan'
            base_plan['priority'] = 'MEDIUM'
            base_plan['target_sleep_hours'] = '7-9 hours'
            base_plan['recommendations'] = [
                "😴 Improve sleep quality and consistency",
                "😴 Target 7-9 hours nightly with consistent schedule",
                "😴 Optimize bedroom environment (dark, quiet, cool)",
                "😴 Limit screens 45 minutes before bed",
                "😴 Establish pre-sleep routine (wind-down period)",
                "😴 Moderate caffeine intake (none after 3 PM)",
                "😴 Consider relaxation techniques",
                "😴 Regular exercise promotes better sleep",
                "😴 Monitor and track sleep patterns",
                "😴 Adjust schedule to find optimal sleep window"
            ]
            base_plan['bedtime_routine'] = [
                '10:00 PM: Begin winding down',
                '10:30 PM: No screens, relaxation activity',
                '11:00 PM: In bed, lights out',
                '11:30 PM: Target sleep time'
            ]
            base_plan['daily_habits'] = [
                'Consistent wake time (within 1 hour on weekends)',
                'Morning light exposure',
                'Exercise regularly (morning or afternoon)',
                'Afternoon relaxation',
                'No large meals before bed'
            ]
            base_plan['optimization_strategies'] = [
                'Keep bedroom cool (65-68°F)',
                'Use blackout curtains if needed',
                'White noise if it helps you',
                'Consistent pre-sleep routine',
                'Track sleep quality in sleep app'
            ]
        
        else:  # low risk
            base_plan['title'] = '✅ LOW RISK: Sleep Maintenance Plan'
            base_plan['priority'] = 'MAINTAIN'
            base_plan['target_sleep_hours'] = '7-9 hours'
            base_plan['recommendations'] = [
                "😴 Excellent sleep pattern - maintain it!",
                "😴 Continue your consistent sleep schedule",
                "😴 Keep up your sleep hygiene habits",
                "😴 Periodically assess sleep quality",
                "😴 Let mild disruptions not derail you",
                "😴 Share sleep tips with others",
                "😴 Continue regular exercise",
                "😴 Stay consistent even on weekends",
                "😴 Adjust routine seasonally if needed"
            ]
            base_plan['maintenance_tips'] = [
                'Consistent sleep and wake times',
                'Comfortable sleep environment',
                'Regular pre-sleep routine',
                'Active lifestyle',
                'Minimal stress management'
            ]
            base_plan['continuous_improvement'] = [
                'Monitor how different activities affect sleep',
                'Optimize bedroom further if interested',
                'Experiment with sleep schedule slightly',
                'Ensure fitness routine supports sleep'
            ]
        
        return base_plan
    
    @classmethod
    def _generate_weekly_goals(
        cls,
        obesity_risk: float,
        inactivity_risk: float,
        sleep_risk: float,
        cluster: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Generate weekly goal targets based on all risks and cluster
        
        Args:
            obesity_risk: Obesity risk probability
            inactivity_risk: Inactivity risk probability
            sleep_risk: Sleep deficiency risk probability
            cluster: Cluster profile dictionary
            
        Returns:
            Weekly goals dictionary
        """
        goals = {
            'week_number': 1,
            'duration': '7 days',
            'cluster_name': cluster['name'],
            'goals': []
        }
        
        # Obesity-related goals
        obesity_level = cls.get_risk_level(obesity_risk)
        if obesity_level == 'critical':
            goals['goals'].append({
                'category': 'Nutrition',
                'priority': 'CRITICAL',
                'target': 'Achieve 700-800 kcal deficit daily',
                'measurement': 'Calorie tracker (MyFitnessPal)',
                'success_criteria': 'Log all meals, deficit maintained 6/7 days',
                'points': 50
            })
        elif obesity_level == 'high':
            goals['goals'].append({
                'category': 'Nutrition',
                'priority': 'HIGH',
                'target': 'Achieve 500-600 kcal deficit daily',
                'measurement': 'Food tracking app',
                'success_criteria': 'Deficit maintained on 5/7 days',
                'points': 40
            })
        elif obesity_level == 'moderate':
            goals['goals'].append({
                'category': 'Nutrition',
                'priority': 'MEDIUM',
                'target': 'Reduce processed food intake by 30%',
                'measurement': 'Food journal notes',
                'success_criteria': '4+ days with minimal processed foods',
                'points': 30
            })
        else:
            goals['goals'].append({
                'category': 'Nutrition',
                'priority': 'MAINTAIN',
                'target': 'Maintain balanced eating patterns',
                'measurement': 'Food journal',
                'success_criteria': '5+ days with balanced meals',
                'points': 20
            })
        
        # Inactivity-related goals
        inactivity_level = cls.get_risk_level(inactivity_risk)
        if inactivity_level == 'critical':
            goals['goals'].append({
                'category': 'Physical Activity',
                'priority': 'CRITICAL',
                'target': 'Achieve 10,000 steps daily AND 3 strength sessions',
                'measurement': 'Pedometer/fitness tracker',
                'success_criteria': '10,000+ steps on 6/7 days, 3 strength sessions',
                'points': 50
            })
        elif inactivity_level == 'high':
            goals['goals'].append({
                'category': 'Physical Activity',
                'priority': 'HIGH',
                'target': 'Achieve 9,000 steps AND 4 workout sessions',
                'measurement': 'Fitness app tracking',
                'success_criteria': '9,000+ steps on 5/7 days, 4 exercise sessions',
                'points': 40
            })
        elif inactivity_level == 'moderate':
            goals['goals'].append({
                'category': 'Physical Activity',
                'priority': 'MEDIUM',
                'target': 'Achieve 8,000 steps AND 3 exercise sessions',
                'measurement': 'Fitness tracker',
                'success_criteria': '8,000+ steps on 4/7 days, 3 sessions completed',
                'points': 30
            })
        else:
            goals['goals'].append({
                'category': 'Physical Activity',
                'priority': 'MAINTAIN',
                'target': 'Maintain 10,000+ steps and weekly workouts',
                'measurement': 'Fitness app',
                'success_criteria': 'Consistent activity maintained',
                'points': 20
            })
        
        # Sleep-related goals
        sleep_level = cls.get_risk_level(sleep_risk)
        if sleep_level == 'critical':
            goals['goals'].append({
                'category': 'Sleep',
                'priority': 'CRITICAL',
                'target': 'Sleep 8-9 hours nightly with consistent schedule',
                'measurement': 'Sleep tracking app or journal',
                'success_criteria': '8+ hours on 6/7 nights, same bedtime',
                'points': 50
            })
        elif sleep_level == 'high':
            goals['goals'].append({
                'category': 'Sleep',
                'priority': 'HIGH',
                'target': 'Sleep 7.5-9 hours with consistent schedule',
                'measurement': 'Sleep app + journal',
                'success_criteria': '7.5+ hours on 5/7 nights',
                'points': 40
            })
        elif sleep_level == 'moderate':
            goals['goals'].append({
                'category': 'Sleep',
                'priority': 'MEDIUM',
                'target': 'Improve to 7-9 hours with bedtime routine',
                'measurement': 'Sleep tracker',
                'success_criteria': '7+ hours on 4/7 nights, routine 5+ nights',
                'points': 30
            })
        else:
            goals['goals'].append({
                'category': 'Sleep',
                'priority': 'MAINTAIN',
                'target': 'Maintain 7-9 hours and sleep quality',
                'measurement': 'Sleep quality notes',
                'success_criteria': 'Consistent sleep maintained',
                'points': 20
            })
        
        # Overview
        goals['overview'] = {
            'total_max_points': sum(g['points'] for g in goals['goals']),
            'focus_areas': [g['category'] for g in goals['goals']],
            'priority_level': max(
                (g['priority'] for g in goals['goals']),
                key=lambda p: ['MAINTAIN', 'MEDIUM', 'HIGH', 'CRITICAL'].index(p)
            )
        }
        
        return goals
    
    @classmethod
    def _generate_alerts(
        cls,
        obesity_risk: float,
        inactivity_risk: float,
        sleep_risk: float
    ) -> Dict[str, Any]:
        """
        Generate health risk alerts for probabilities > 0.75
        
        Args:
            obesity_risk: Obesity risk probability
            inactivity_risk: Inactivity risk probability
            sleep_risk: Sleep deficiency risk probability
            
        Returns:
            Alerts dictionary
        """
        alerts = {
            'timestamp': datetime.now().isoformat(),
            'critical_alerts': [],
            'high_alerts': [],
            'recommendations': []
        }
        
        # Check for critical alerts (>0.75)
        if obesity_risk > 0.75:
            alerts['critical_alerts'].append({
                'type': 'CRITICAL OBESITY RISK',
                'emoji': '🚨',
                'message': f'Obesity risk probability: {obesity_risk:.1%} - CRITICAL',
                'action': 'Immediately consult with a healthcare provider and registered dietitian',
                'urgency': 'IMMEDIATE'
            })
            alerts['recommendations'].append(
                'Schedule urgent appointment with primary care physician and nutritionist'
            )
        
        if inactivity_risk > 0.75:
            alerts['critical_alerts'].append({
                'type': 'CRITICAL INACTIVITY RISK',
                'emoji': '🚨',
                'message': f'Inactivity risk probability: {inactivity_risk:.1%} - CRITICAL',
                'action': 'Begin structured exercise program immediately under professional guidance',
                'urgency': 'IMMEDIATE'
            })
            alerts['recommendations'].append(
                'Work with a personal trainer or fitness specialist to start safely'
            )
        
        if sleep_risk > 0.75:
            alerts['critical_alerts'].append({
                'type': 'CRITICAL SLEEP DEFICIENCY',
                'emoji': '🚨',
                'message': f'Sleep deficiency risk probability: {sleep_risk:.1%} - CRITICAL',
                'action': 'Implement sleep intervention immediately; consider sleep specialist',
                'urgency': 'IMMEDIATE'
            })
            alerts['recommendations'].append(
                'Consult a sleep specialist or sleep medicine doctor if no improvement in 2 weeks'
            )
        
        # Check for high alerts (0.6-0.75)
        if 0.6 < obesity_risk <= 0.75:
            alerts['high_alerts'].append({
                'type': 'HIGH OBESITY RISK',
                'emoji': '⚠️⚠️',
                'message': f'Obesity risk probability: {obesity_risk:.1%} - HIGH',
                'action': 'Schedule appointment with nutritionist and begin weight management plan',
                'urgency': 'WEEK 1'
            })
        
        if 0.6 < inactivity_risk <= 0.75:
            alerts['high_alerts'].append({
                'type': 'HIGH INACTIVITY RISK',
                'emoji': '⚠️⚠️',
                'message': f'Inactivity risk probability: {inactivity_risk:.1%} - HIGH',
                'action': 'Begin structured activity program outlined in your health plan',
                'urgency': 'WEEK 1'
            })
        
        if 0.6 < sleep_risk <= 0.75:
            alerts['high_alerts'].append({
                'type': 'HIGH SLEEP DEFICIENCY RISK',
                'emoji': '⚠️⚠️',
                'message': f'Sleep deficiency risk probability: {sleep_risk:.1%} - HIGH',
                'action': 'Implement sleep improvement plan with strict sleep schedule',
                'urgency': 'WEEK 1'
            })
        
        # Overall alert summary
        alerts['summary'] = {
            'has_critical': len(alerts['critical_alerts']) > 0,
            'has_high': len(alerts['high_alerts']) > 0,
            'total_alerts': len(alerts['critical_alerts']) + len(alerts['high_alerts']),
            'next_steps': alerts['recommendations'] if alerts['recommendations'] else [
                'Continue following your personalized health plan',
                'Monitor progress weekly',
                'Schedule regular check-ups'
            ]
        }
        
        return alerts
    
    @classmethod
    def _generate_rule_based_plan(
        cls,
        cluster_id: int,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a rule-based health plan when ML predictions are unavailable
        
        Args:
            cluster_id: User's lifestyle cluster ID
            user_profile: Optional user profile for additional context
            
        Returns:
            Rule-based health plan dictionary
        """
        logger.info("📋 Generating rule-based health plan (ML unavailable)")
        
        cluster_profile = cls.CLUSTER_PROFILES.get(cluster_id, cls.CLUSTER_PROFILES[0])
        
        plan = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'cluster_id': cluster_id,
                'cluster_name': cluster_profile['name'],
                'plan_type': 'RULE-BASED (ML unavailable)',
                'warning': 'Generated without ML predictions - based on cluster profile only'
            },
            'diet_plan': {
                'title': f'🥗 Standard Diet Plan for {cluster_profile["name"]}',
                'focus_area': cluster_profile['diet_emphasis'],
                'recommendations': [
                    "🥗 Eat 3 balanced meals daily",
                    "🥗 Include vegetables in 50% of your meals",
                    "🥗 Choose whole grains over refined grains",
                    "🥗 Include lean protein in each meal",
                    "🥗 Limit processed foods and sugary drinks",
                    "🥗 Drink 2.5-3 liters of water daily",
                    "🥗 Eat mindfully and avoid emotional eating",
                    "🥗 Plan meals ahead when possible"
                ]
            },
            'activity_plan': {
                'title': f'🎯 Physical Activity Plan for {cluster_profile["name"]}',
                'focus_area': cluster_profile['activity_emphasis'],
                'daily_target_steps': 8000,
                'weekly_target_minutes': 150,
                'recommendations': [
                    "🎯 Aim for 150 minutes of moderate activity weekly",
                    "🎯 Target 8,000+ steps daily",
                    "🎯 Include 2-3 strength training sessions weekly",
                    "🎯 Vary activities to maintain interest",
                    "🎯 Move regularly throughout the day",
                    "🎯 Find activities you enjoy",
                    "🎯 Exercise at a time that fits your schedule",
                    "🎯 Track your progress with an app"
                ]
            },
            'sleep_plan': {
                'title': f'😴 Sleep Plan for {cluster_profile["name"]}',
                'focus_area': cluster_profile['sleep_emphasis'],
                'target_sleep_hours': '7-9 hours',
                'recommendations': [
                    "😴 Maintain consistent sleep schedule (same bedtime/wake time)",
                    "😴 Target 7-9 hours of sleep nightly",
                    "😴 Create a comfortable sleep environment",
                    "😴 Limit screens 30 minutes before bed",
                    "😴 Avoid caffeine in afternoon and evening",
                    "😴 Exercise regularly for better sleep",
                    "😴 Use relaxation techniques if needed",
                    "😴 Be consistent, even on weekends"
                ]
            },
            'weekly_goals': {
                'week_number': 1,
                'duration': '7 days',
                'goals': [
                    {
                        'category': 'Nutrition',
                        'target': '6/7 days with balanced meals',
                        'points': 25
                    },
                    {
                        'category': 'Physical Activity',
                        'target': '5/7 days with exercise or 8,000+ steps',
                        'points': 25
                    },
                    {
                        'category': 'Sleep',
                        'target': '5/7 nights with 7+ hours',
                        'points': 25
                    },
                    {
                        'category': 'Hydration',
                        'target': 'Drink water with each meal',
                        'points': 15
                    }
                ],
                'total_max_points': 90
            },
            'alerts': {
                'timestamp': datetime.now().isoformat(),
                'info_message': 'No ML-based risk alerts (ML unavailable)',
                'recommendations': [
                    '📈 Get baseline health measurements (BMI, steps, sleep hours)',
                    '📈 Track health metrics for 1-2 weeks',
                    '📈 Schedule with healthcare provider for assessment',
                    '✅ Follow this plan consistently for best results'
                ]
            }
        }
        
        logger.info("✅ Rule-based health plan generated successfully")
        return plan
