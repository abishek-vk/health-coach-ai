"""
gemini_integration.py - Gemini API Integration for Enhanced Health Recommendations
Provides AI-powered personalization using Google's Generative AI
"""

import os
from typing import List, Dict, Optional, Any
import google.generativeai as genai
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class GeminiHealthAdvisor:
    """Leverages Gemini API for personalized health recommendations"""
    
    def __init__(self):
        """Initialize Gemini API with credentials from environment"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.enabled = os.getenv("ENABLE_GEMINI_ENHANCEMENTS", "true").lower() == "true"
        
        if self.enabled and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                # Use gemini-pro (stable, widely available model)
                self.model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                print(f"⚠️ Warning: Failed to initialize Gemini API: {e}")
                self.enabled = False
        else:
            self.enabled = False
    
    def enhance_recommendations(
        self, 
        recommendations: Dict[str, List[str]], 
        profile: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """
        Enhance standard recommendations with AI-powered personalization
        
        Args:
            recommendations: Dictionary of recommendation categories
            profile: User health profile for context
            
        Returns:
            Enhanced recommendations dictionary
        """
        if not self.enabled:
            return recommendations
        
        try:
            # Create context-aware prompt based on user profile
            context = self._build_health_context(profile)
            enhanced = recommendations.copy()
            
            # Get AI enhancements for exercise recommendations
            enhanced["exercise"] = self._get_ai_suggestions(
                recommendations["exercise"],
                context,
                "exercise and fitness"
            )
            
            # Get AI enhancements for diet recommendations
            enhanced["diet"] = self._get_ai_suggestions(
                recommendations["diet"],
                context,
                "nutrition and diet"
            )
            
            # Get AI enhancements for sleep recommendations
            enhanced["sleep"] = self._get_ai_suggestions(
                recommendations["sleep"],
                context,
                "sleep optimization"
            )
            
            return enhanced
            
        except Exception as e:
            print(f"⚠️ Warning: Gemini enhancement failed: {e}")
            return recommendations
    
    def get_personalized_plan(self, profile: Dict[str, Any]) -> str:
        """
        Generate a complete personalized health plan using Gemini
        
        Args:
            profile: User health profile
            
        Returns:
            Personalized health plan as formatted string
        """
        if not self.enabled:
            return "AI enhancements disabled. Using standard recommendations."
        
        try:
            context = self._build_health_context(profile)
            
            prompt = f"""Based on this health profile:
{context}

Create a comprehensive, personalized 30-day health improvement plan. Include:
1. Weekly goals and milestones
2. Specific exercise routines (with time and intensity)
3. Meal planning guidelines
4. Sleep optimization strategies
5. Risk mitigation steps
6. Progress tracking metrics

Keep recommendations safe, practical, and achievable."""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"⚠️ Error generating personalized plan: {e}")
            return "Unable to generate AI plan. Please use standard recommendations."
    
    def get_health_insights(self, profile: Dict[str, Any]) -> str:
        """
        Generate health insights and analysis using Gemini
        
        Args:
            profile: User health profile
            
        Returns:
            Health insights analysis
        """
        if not self.enabled:
            return ""
        
        try:
            context = self._build_health_context(profile)
            
            prompt = f"""Analyze this health profile and provide brief insights:
{context}

Provide 3-4 key insights about the person's current health status, highlighting:
- Strengths in their health habits
- Areas of concern
- Quick wins they could achieve
- Long-term health outlook

Keep it encouraging and actionable. Limit to 150 words."""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"⚠️ Error generating insights: {e}")
            return ""
    
    def get_motivation_message(self, category: str, progress: Optional[Dict] = None) -> str:
        """
        Generate motivational messages for different health categories
        
        Args:
            category: Health category (exercise, diet, sleep, etc.)
            progress: Optional progress data
            
        Returns:
            Motivational message
        """
        if not self.enabled:
            return f"Keep up your {category} goals!"
        
        try:
            prompt = f"""Generate a brief, personalized motivational message about {category}.
            
Progress context: {progress if progress else 'New user starting journey'}

The message should be:
- Encouraging but realistic
- Specific to the category
- Actionable
- 2-3 sentences max
- Use emojis appropriately"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"💪 Keep pushing towards your {category} goals!"
    
    # =====================================================================
    # PRIVATE HELPER METHODS
    # =====================================================================
    
    def _build_health_context(self, profile: Dict[str, Any]) -> str:
        """Build detailed health context for Gemini prompt"""
        
        age = profile.get("age", "Unknown")
        gender = profile.get("gender", "Unknown")
        bmi = profile.get("bmi", "Unknown")
        bmi_category = profile.get("bmi_category", "Unknown")
        activity_level = profile.get("activity_level", "Unknown")
        avg_steps = profile.get("average_steps", 0)
        avg_sleep = profile.get("average_sleep_hours", 0)
        sleep_category = profile.get("sleep_category", "Unknown")
        water_intake = profile.get("average_water_intake", 0)
        hydration = profile.get("hydration_level", "Unknown")
        medical = profile.get("medical_conditions", "None")
        medications = profile.get("medications", "None")
        goals = profile.get("health_goals", "Improve overall health")
        risks = profile.get("health_risks", [])
        
        context = f"""
        Age: {age} years old
        Gender: {gender}
        
        Physical Metrics:
        - BMI: {bmi} ({bmi_category})
        - Activity Level: {activity_level}
        - Average Daily Steps: {int(avg_steps)}
        
        Lifestyle Habits:
        - Sleep: {avg_sleep} hours/night ({sleep_category})
        - Water Intake: {water_intake}L/day ({hydration})
        
        Medical Information:
        - Conditions: {medical}
        - Medications: {medications}
        
        Health Goals: {goals}
        
        Identified Risk Factors: {', '.join(risks) if risks else 'None identified'}
        """
        
        return context.strip()
    
    def _get_ai_suggestions(
        self, 
        standard_recommendations: List[str], 
        context: str, 
        category: str
    ) -> List[str]:
        """
        Get AI-enhanced suggestions for a recommendation category
        
        Args:
            standard_recommendations: Base recommendations
            context: Health context
            category: Category of recommendations
            
        Returns:
            Enhanced recommendations list
        """
        try:
            prompt = f"""Given this health context:
{context}

And these standard {category} recommendations:
{chr(10).join(f'- {r}' for r in standard_recommendations)}

Provide 2 additional personalized {category} recommendations that are:
- Specific to their profile
- Practical and achievable
- Different from the standard ones
- Include relevant emoji

Format as bullet points only, no explanations."""
            
            response = self.model.generate_content(prompt)
            
            # Parse response into list
            suggestions = [
                line.strip() 
                for line in response.text.split('\n') 
                if line.strip() and line.strip().startswith(('•', '-', '🎯', '🥗', '😴', '💧'))
            ]
            
            # Combine standard + AI suggestions
            enhanced = standard_recommendations.copy()
            enhanced.extend(suggestions[:2])  # Add up to 2 AI suggestions
            
            return enhanced
            
        except Exception as e:
            print(f"⚠️ Error enhancing {category} suggestions: {e}")
            return standard_recommendations


# Singleton instance
_gemini_advisor = None


def get_gemini_advisor() -> GeminiHealthAdvisor:
    """Get or create Gemini advisor instance"""
    global _gemini_advisor
    if _gemini_advisor is None:
        _gemini_advisor = GeminiHealthAdvisor()
    return _gemini_advisor
