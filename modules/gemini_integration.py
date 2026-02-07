"""
gemini_integration.py - Gemini API Integration for Enhanced Health Recommendations
Provides AI-powered personalization using Google's Generative AI

UNIFIED API CALL STRATEGY:
- Single Gemini API request generates all recommendations (sleep, diet, fitness, wellness)
- Structured JSON response parsed into recommendation categories
- Rate limiting ensures no more than 5 requests/minute
- Caching prevents duplicate API calls for same user profile
- All public methods maintained for backward compatibility
"""

import os
import json
import logging
import hashlib
from typing import List, Dict, Optional, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Import rate-limited request manager
from .gemini_request_manager import GeminiRequestManager

# Setup logging for rate limiting
logger = logging.getLogger(__name__)


# Load environment variables
load_dotenv()


# =====================================================================
# MODEL CONFIGURATION - CENTRALIZED
# =====================================================================
# Preferred model with fallback options (in order of preference)
# Updated to use latest available Gemini 2.5 models
PREFERRED_MODELS = [
    "gemini-2.5-flash",      # Preferred: Latest, fastest, cost-efficient
    "gemini-2.5-pro",        # Fallback: Latest, more capable
    "gemini-2.0-flash",      # Fallback: Stable, proven
    "gemini-flash-latest",   # Fallback: Always points to latest
]

# This will be set during initialization
ACTIVE_MODEL_NAME = None


class GeminiHealthAdvisor:
    """Leverages Gemini API for personalized health recommendations with rate limiting
    
    Uses unified single-request architecture to generate all recommendations
    in one API call, then caches and parses results for individual methods.
    """
    
    def __init__(self):
        """Initialize Gemini API with credentials from environment and request manager"""
        global ACTIVE_MODEL_NAME
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.enabled = os.getenv("ENABLE_GEMINI_ENHANCEMENTS", "true").lower() == "true"
        self.model = None
        self.request_manager = None  # Rate-limited request handler
        self.initialization_error = None
        
        # Cache for unified analysis results - keyed by profile hash
        self._analysis_cache = {}
        self._cache_max_size = 50  # Keep last 50 profiles
        
        if self.enabled and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                
                # Try models in order of preference
                for model_name in PREFERRED_MODELS:
                    try:
                        candidate_model = genai.GenerativeModel(model_name)
                        # Test if model is accessible with a simple request
                        test_response = candidate_model.generate_content(
                            "This is a test message.",
                            stream=False
                        )
                        # If successful, use this model
                        self.model = candidate_model
                        ACTIVE_MODEL_NAME = model_name
                        
                        # Initialize request manager with rate limiting
                        self.request_manager = GeminiRequestManager(
                            model=candidate_model,
                            requests_per_minute=5,
                            max_retries=3,
                            retry_wait_seconds=35,
                            logger=logger
                        )
                        
                        print(f"✅ Gemini API initialized with model: {model_name}")
                        print(f"✅ Rate limiting enabled: 5 requests/minute with 3 retries")
                        print(f"✅ Unified health analysis enabled: Single API call for all recommendations")
                        return
                    except Exception as model_error:
                        error_msg = str(model_error)
                        print(f"⚠️ Model {model_name} unavailable: {error_msg[:100]}")
                        
                        # Store quota errors for diagnostic purposes
                        if "429" in error_msg or "quota" in error_msg.lower():
                            self.initialization_error = f"API quota exceeded: {error_msg[:150]}"
                        
                        continue
                
                # If all models failed
                if self.initialization_error:
                    print(f"⚠️ {self.initialization_error}")
                    print("💡 Solution: Check your Gemini API quota and billing at https://aistudio.google.com/")
                else:
                    print("❌ No Gemini models available. Disabling AI enhancements.")
                
                self.enabled = False
                ACTIVE_MODEL_NAME = None
                
            except Exception as e:
                print(f"⚠️ Warning: Failed to initialize Gemini API: {e}")
                self.enabled = False
                ACTIVE_MODEL_NAME = None
        else:
            self.enabled = False
            ACTIVE_MODEL_NAME = None
    
    def _profile_to_hash(self, profile: Dict[str, Any]) -> str:
        """
        Generate a hash of profile for caching purposes
        
        Args:
            profile: User health profile
            
        Returns:
            Hash string of profile
        """
        profile_str = json.dumps(profile, sort_keys=True)
        return hashlib.md5(profile_str.encode()).hexdigest()
    
    def generate_full_health_analysis(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        UNIFIED FUNCTION: Generate complete health analysis in a single API call.
        
        This function consolidates all health recommendation generation into ONE
        structured Gemini API request, returning categorized recommendations for:
        - Sleep optimization
        - Diet suggestions
        - Fitness guidance
        - Mental wellness insights
        
        Results are cached to prevent duplicate API calls for same profile.
        
        Args:
            profile: User health profile dictionary
            
        Returns:
            Dictionary with structured analysis:
            {
                "sleep": [...recommendations],
                "diet": [...recommendations],
                "fitness": [...recommendations],
                "wellness": [...recommendations],
                "personalized_plan": "30-day plan...",
                "health_insights": "Key insights...",
                "timestamp": "2026-02-07T12:00:00",
                "api_calls_made": 1
            }
        """
        if not self.enabled or not self.request_manager:
            logger.warning("Gemini AI disabled. Returning empty analysis.")
            return {
                "sleep": [],
                "diet": [],
                "fitness": [],
                "wellness": [],
                "personalized_plan": "AI enhancements disabled.",
                "health_insights": "",
                "api_calls_made": 0
            }
        
        # Check cache first
        profile_hash = self._profile_to_hash(profile)
        if profile_hash in self._analysis_cache:
            logger.info(f"📦 CACHE HIT: Using cached analysis for profile (hash: {profile_hash[:8]}...)")
            result = self._analysis_cache[profile_hash].copy()
            result["from_cache"] = True
            result["cache_hit"] = True
            logger.info(f"   ✓ Reusing cached result (no API call made)")
            logger.info(f"   ✓ Recommendations: {len(result.get('sleep', []))} sleep, "
                       f"{len(result.get('diet', []))} diet, {len(result.get('fitness', []))} fitness, "
                       f"{len(result.get('wellness', []))} wellness")
            return result
        
        try:
            # Build comprehensive health context
            context = self._build_health_context(profile)
            
            # Single unified prompt requesting all recommendations in STRICT JSON format
            unified_prompt = f"""
UNIFIED HEALTH ANALYSIS REQUEST - STRICT JSON OUTPUT REQUIRED

Analyze this user's health profile and generate COMPREHENSIVE recommendations in ALL categories.
You MUST respond ONLY with valid JSON, nothing else. No markdown, no explanations, just pure JSON.

USER HEALTH PROFILE:
{context}

REQUIRED: Return ONLY this JSON structure (valid JSON only, no comments):
{{
  "sleep": [
    "😴 [Specific sleep recommendation 1 based on their sleep category and metrics]",
    "😴 [Specific sleep recommendation 2]",
    "😴 [Specific sleep recommendation 3]",
    "😴 [Specific sleep recommendation 4]",
    "😴 [Specific sleep recommendation 5]"
  ],
  "diet": [
    "🥗 [Specific nutrition recommendation 1 based on their BMI and health goals]",
    "🥗 [Specific nutrition recommendation 2]",
    "🥗 [Specific nutrition recommendation 3]",
    "🥗 [Specific nutrition recommendation 4]",
    "🥗 [Specific nutrition recommendation 5]"
  ],
  "fitness": [
    "💪 [Specific exercise recommendation 1 based on activity level and age]",
    "💪 [Specific exercise recommendation 2]",
    "💪 [Specific exercise recommendation 3]",
    "💪 [Specific exercise recommendation 4]",
    "💪 [Specific exercise recommendation 5]"
  ],
  "wellness": [
    "🧠 [Mental wellness and stress management recommendation 1]",
    "🧠 [Mental wellness recommendation 2]",
    "🧠 [Mental wellness recommendation 3]",
    "🧠 [Mental wellness recommendation 4]"
  ],
  "personalized_plan": "WEEK 1: [Focus areas]. WEEK 2-3: [Progression]. WEEK 4: [Goals and expected outcomes]. [150-200 total words describing their 30-day health plan]",
  "health_insights": "[3-4 key insights: top strengths, areas for improvement, quick wins, and realistic long-term outlook. 100-150 words total]"
}}

CRITICAL REQUIREMENTS:
1. Return ONLY valid JSON - no markdown code blocks, no explanations, no extra text
2. All arrays must contain strings only
3. Each recommendation must be specific to their profile
4. Use emojis as shown above
5. Make recommendations practical, safe, and achievable
6. Be encouraging but realistic"""

            logger.info(f"📊 Generating unified health analysis for profile (hash: {profile_hash[:8]}...)")
            logger.info("📝 Making SINGLE Gemini API call for all recommendations (sleep, diet, fitness, wellness)")
            
            # Make SINGLE API call
            response_text = self.request_manager.generate(unified_prompt)
            
            logger.info(f"📥 Received response from Gemini API: {len(response_text)} characters")
            
            # Parse structured response
            analysis = self._parse_unified_response(response_text)
            
            # Add metadata
            analysis["api_calls_made"] = 1
            analysis["from_cache"] = False
            analysis["cache_hit"] = False
            analysis["timestamp"] = self._get_timestamp()
            
            # Cache the result
            self._analysis_cache[profile_hash] = analysis.copy()
            
            # Trim cache if too large
            if len(self._analysis_cache) > self._cache_max_size:
                oldest_key = next(iter(self._analysis_cache))
                del self._analysis_cache[oldest_key]
                logger.debug(f"🗑️ Cache trimmed. Current size: {len(self._analysis_cache)}")
            
            logger.info(f"✅ Unified analysis complete. 1 API call processed and cached.")
            logger.info(f"   📊 Recommendations generated:")
            logger.info(f"      • Sleep: {len(analysis.get('sleep', []))} recommendations")
            logger.info(f"      • Diet: {len(analysis.get('diet', []))} recommendations")
            logger.info(f"      • Fitness: {len(analysis.get('fitness', []))} recommendations")
            logger.info(f"      • Wellness: {len(analysis.get('wellness', []))} recommendations")
            logger.info(f"      • Personalized plan: {len(analysis.get('personalized_plan', ''))} chars")
            logger.info(f"      • Health insights: {len(analysis.get('health_insights', ''))} chars")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error generating unified health analysis: {e}")
            return {
                "sleep": [],
                "diet": [],
                "fitness": [],
                "wellness": [],
                "personalized_plan": "Error generating personalized plan.",
                "health_insights": "",
                "api_calls_made": 0,
                "error": str(e)
            }
    
    def _parse_unified_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse unified JSON response from Gemini
        
        Safely loads JSON response with error handling for malformed responses
        
        Args:
            response_text: Full response text from Gemini
            
        Returns:
            Parsed dictionary with categories (safely handles parsing errors)
        """
        sections = {
            "sleep": [],
            "diet": [],
            "fitness": [],
            "wellness": [],
            "personalized_plan": "",
            "health_insights": ""
        }
        
        try:
            # Clean the response text - remove markdown code blocks if present
            clean_response = response_text.strip()
            
            # Handle markdown code block wrapping (e.g., ```json ... ```)
            if clean_response.startswith("```"):
                # Remove opening ```json or ```
                clean_response = clean_response.split("\n", 1)[1] if "\n" in clean_response else clean_response
                # Remove closing ```
                if clean_response.endswith("```"):
                    clean_response = clean_response.rsplit("\n", 1)[0] if "\n" in clean_response else clean_response
                clean_response = clean_response.strip()
            
            # Attempt to parse JSON
            parsed_json = json.loads(clean_response)
            
            # Validate and extract each field with logging
            if isinstance(parsed_json, dict):
                # Extract sleep recommendations (array expected)
                if "sleep" in parsed_json and isinstance(parsed_json["sleep"], list):
                    sections["sleep"] = [str(item).strip() for item in parsed_json["sleep"] if item]
                    logger.debug(f"✓ Parsed {len(sections['sleep'])} sleep recommendations from JSON")
                
                # Extract diet recommendations (array expected)
                if "diet" in parsed_json and isinstance(parsed_json["diet"], list):
                    sections["diet"] = [str(item).strip() for item in parsed_json["diet"] if item]
                    logger.debug(f"✓ Parsed {len(sections['diet'])} diet recommendations from JSON")
                
                # Extract fitness recommendations (array expected)
                if "fitness" in parsed_json and isinstance(parsed_json["fitness"], list):
                    sections["fitness"] = [str(item).strip() for item in parsed_json["fitness"] if item]
                    logger.debug(f"✓ Parsed {len(sections['fitness'])} fitness recommendations from JSON")
                
                # Extract wellness recommendations (array expected)
                if "wellness" in parsed_json and isinstance(parsed_json["wellness"], list):
                    sections["wellness"] = [str(item).strip() for item in parsed_json["wellness"] if item]
                    logger.debug(f"✓ Parsed {len(sections['wellness'])} wellness recommendations from JSON")
                
                # Extract personalized plan (string expected)
                if "personalized_plan" in parsed_json:
                    sections["personalized_plan"] = str(parsed_json["personalized_plan"]).strip()
                    if sections["personalized_plan"]:
                        logger.debug(f"✓ Parsed personalized plan: {len(sections['personalized_plan'])} chars")
                
                # Extract health insights (string expected)
                if "health_insights" in parsed_json:
                    sections["health_insights"] = str(parsed_json["health_insights"]).strip()
                    if sections["health_insights"]:
                        logger.debug(f"✓ Parsed health insights: {len(sections['health_insights'])} chars")
                
                logger.info(f"✅ Successfully parsed JSON response with {len(sections['sleep'])} sleep, "
                           f"{len(sections['diet'])} diet, {len(sections['fitness'])} fitness, "
                           f"{len(sections['wellness'])} wellness recommendations")
                return sections
            else:
                logger.error(f"Parsed JSON is not a dictionary: {type(parsed_json)}")
                return sections
                
        except json.JSONDecodeError as je:
            logger.error(f"❌ Failed to parse response as JSON. Error: {str(je)[:150]}")
            logger.debug(f"Response text (first 500 chars): {response_text[:500]}")
            
            # Fallback: Try to extract recommendations from semi-structured text
            logger.info("Attempting fallback parsing for semi-structured response...")
            return self._parse_fallback_response(response_text, sections)
            
        except Exception as e:
            logger.error(f"Unexpected error parsing unified response: {e}")
            return sections
    
    def _parse_fallback_response(self, response_text: str, sections: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback parser for semi-structured text responses when JSON parsing fails
        
        Attempts to extract recommendations from markdown-formatted text
        
        Args:
            response_text: Response text from Gemini
            sections: Base sections dictionary to populate
            
        Returns:
            Parsed dictionary with extracted recommendations
        """
        try:
            lines = response_text.split('\n')
            current_section = None
            
            for i, line in enumerate(lines):
                line_stripped = line.strip()
                if not line_stripped:
                    continue
                
                # Section detection - only when ### prefix is present (strict detection)
                is_header_line = line_stripped.startswith("###")
                
                if is_header_line:
                    # Only change section on actual header lines with ###
                    if "sleep" in line_stripped.lower():
                        current_section = "sleep"
                        logger.debug(f"Line {i}: Detected SLEEP section header")
                        continue
                    elif ("diet" in line_stripped.lower() or "nutrition" in line_stripped.lower()):
                        current_section = "diet"
                        logger.debug(f"Line {i}: Detected DIET section header")
                        continue
                    elif ("fitness" in line_stripped.lower() or "exercise" in line_stripped.lower()):
                        current_section = "fitness"
                        logger.debug(f"Line {i}: Detected FITNESS section header")
                        continue
                    elif ("wellness" in line_stripped.lower() or "mental" in line_stripped.lower()):
                        current_section = "wellness"
                        logger.debug(f"Line {i}: Detected WELLNESS section header")
                        continue
                    elif ("personalized" in line_stripped.lower() or "30-day" in line_stripped.lower()):
                        current_section = "personalized_plan"
                        logger.debug(f"Line {i}: Detected PLAN section header")
                        continue
                    elif ("insight" in line_stripped.lower() or "key health" in line_stripped.lower()):
                        current_section = "health_insights"
                        logger.debug(f"Line {i}: Detected INSIGHTS section header")
                        continue
                
                # Now process content based on current section
                if not current_section:
                    continue
                
                if line_stripped.startswith(('•', '-', '🌙', '😴', '🥗', '💪', '🧠')):
                    # Bullet point - add to list sections
                    if current_section in ["sleep", "diet", "fitness", "wellness"]:
                        sections[current_section].append(line_stripped)
                        logger.debug(f"Line {i}: Added bullet to {current_section}")
                elif current_section in ["personalized_plan", "health_insights"]:
                    # Accumulate paragraph content (don't process as new section)
                    if sections[current_section]:
                        sections[current_section] += " " + line_stripped
                    else:
                        sections[current_section] = line_stripped
                    logger.debug(f"Line {i}: Accumulated to {current_section}: {line_stripped[:50]}...")
            
            # Clean up accumulated text
            sections["personalized_plan"] = sections["personalized_plan"].strip() if sections["personalized_plan"] else ""
            sections["health_insights"] = sections["health_insights"].strip() if sections["health_insights"] else ""
            
            logger.warning(f"⚠️ Fallback parsing extracted {len(sections['sleep'])} sleep, "
                          f"{len(sections['diet'])} diet, {len(sections['fitness'])} fitness, "
                          f"{len(sections['wellness'])} wellness, "
                          f"plan: {len(sections['personalized_plan'])} chars, "
                          f"insights: {len(sections['health_insights'])} chars")
            
            return sections
            
        except Exception as e:
            logger.error(f"Fallback parser also failed: {e}")
            return sections
    
    def _get_timestamp(self) -> str:
        """Get ISO format timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def enhance_recommendations(
        self, 
        recommendations: Dict[str, List[str]], 
        profile: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """
        Enhance standard recommendations with AI-powered personalization.
        
        NOW USES UNIFIED API: Calls generate_full_health_analysis() which makes
        a single API request instead of multiple separate calls.
        
        Args:
            recommendations: Dictionary of recommendation categories
            profile: User health profile for context
            
        Returns:
            Enhanced recommendations dictionary
        """
        if not self.enabled:
            return recommendations
        
        try:
            # Get unified analysis (single API call)
            analysis = self.generate_full_health_analysis(profile)
            
            if "api_calls_made" not in analysis or analysis["api_calls_made"] == 0:
                logger.warning("Unified analysis failed. Returning standard recommendations.")
                return recommendations
            
            # Merge AI recommendations with standard ones
            enhanced = recommendations.copy()
            
            # Add AI-generated recommendations
            if analysis.get("sleep"):
                enhanced["sleep"] = analysis["sleep"] + recommendations.get("sleep", [])
            
            if analysis.get("diet"):
                enhanced["diet"] = analysis["diet"] + recommendations.get("diet", [])
            
            if analysis.get("fitness"):
                enhanced["exercise"] = analysis["fitness"] + recommendations.get("exercise", [])
            
            if analysis.get("wellness"):
                enhanced["mental_wellness"] = analysis["wellness"]
            
            logger.info(f"✓ Recommendations enhanced via unified analysis (1 API call total)")
            return enhanced
            
        except Exception as e:
            logger.error(f"Warning: Gemini enhancement failed: {e}")
            return recommendations
    
    
    
    def get_personalized_plan(self, profile: Dict[str, Any]) -> str:
        """
        Generate a complete personalized health plan using Gemini.
        
        NOW USES UNIFIED API: Extracts the 30-day plan from generate_full_health_analysis()
        which makes a single API request (no additional calls).
        
        Args:
            profile: User health profile
            
        Returns:
            Personalized health plan as formatted string
        """
        if not self.enabled or not self.request_manager:
            return "AI enhancements disabled. Using standard recommendations."
        
        try:
            # Get unified analysis (single API call, may be cached)
            analysis = self.generate_full_health_analysis(profile)
            
            plan = analysis.get("personalized_plan", "")
            if plan:
                logger.info("✓ Personalized plan extracted from unified analysis (already counted in 1 API call)")
                return plan
            
            return "Unable to generate personalized plan. Using standard recommendations."
            
        except Exception as e:
            logger.error(f"Error generating personalized plan: {e}")
            return "Unable to generate AI plan. Please use standard recommendations."
    
    
    def get_health_insights(self, profile: Dict[str, Any]) -> str:
        """
        Generate health insights and analysis using Gemini.
        
        NOW USES UNIFIED API: Extracts insights from generate_full_health_analysis()
        which makes a single API request (no additional calls).
        
        Args:
            profile: User health profile
            
        Returns:
            Health insights analysis
        """
        if not self.enabled or not self.request_manager:
            return ""
        
        try:
            # Get unified analysis (single API call, may be cached)
            analysis = self.generate_full_health_analysis(profile)
            
            insights = analysis.get("health_insights", "")
            if insights:
                logger.info("✓ Health insights extracted from unified analysis (already counted in 1 API call)")
                return insights
            
            return ""
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return ""
    
    
    def get_motivation_message(self, category: str, progress: Optional[Dict] = None) -> str:
        """
        Generate motivational messages for different health categories.
        
        Note: This method makes a separate API call since it's category-specific
        and often called outside the main recommendation flow. Consider including
        in unified analysis if needed for multiple categories simultaneously.
        
        Args:
            category: Health category (exercise, diet, sleep, etc.)
            progress: Optional progress data
            
        Returns:
            Motivational message
        """
        if not self.enabled or not self.request_manager:
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
            
            response = self.request_manager.generate_with_fallback(
                prompt,
                fallback_response=f"💪 Keep pushing towards your {category} goals!"
            )
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating motivation message: {e}")
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
        # DEPRECATED: This method is no longer used by enhance_recommendations()
        # which now uses the unified generate_full_health_analysis() instead.
        # Kept for backward compatibility if called directly.
        
        if not self.request_manager:
            return standard_recommendations
            
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
            
            response = self.request_manager.generate_with_fallback(
                prompt,
                fallback_response=""
            )
            
            # Parse response into list
            if response:
                suggestions = [
                    line.strip() 
                    for line in response.split('\n') 
                    if line.strip() and line.strip().startswith(('•', '-', '🎯', '🥗', '😴', '💧'))
                ]
                
                # Combine standard + AI suggestions
                enhanced = standard_recommendations.copy()
                enhanced.extend(suggestions[:2])  # Add up to 2 AI suggestions
                
                logger.warning(f"WARNING: Deprecated _get_ai_suggestions() called for {category}. "
                              f"Use unified generate_full_health_analysis() instead.")
                return enhanced
            else:
                return standard_recommendations
            
        except Exception as e:
            logger.error(f"Error enhancing {category} suggestions: {e}")
            return standard_recommendations


# Singleton instance
_gemini_advisor = None


def get_gemini_advisor() -> GeminiHealthAdvisor:
    """Get or create Gemini advisor instance"""
    global _gemini_advisor
    if _gemini_advisor is None:
        _gemini_advisor = GeminiHealthAdvisor()
    return _gemini_advisor


def get_active_model_name() -> Optional[str]:
    """Get the currently active Gemini model name"""
    global ACTIVE_MODEL_NAME
    if ACTIVE_MODEL_NAME is None:
        # Ensure advisor is initialized
        get_gemini_advisor()
    return ACTIVE_MODEL_NAME
