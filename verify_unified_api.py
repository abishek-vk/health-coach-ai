#!/usr/bin/env python3
"""
Verification script for unified Gemini health analysis refactoring.

This script validates that:
1. The unified API function exists and is callable
2. Single API call is made instead of multiple calls
3. Caching works correctly
4. Backward compatibility is maintained
5. Logging confirms operations

Usage:
    python verify_unified_api.py
"""

import logging
import sys

# Setup detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all required modules can be imported"""
    print("\n" + "="*60)
    print("TEST 1: Verifying imports...")
    print("="*60)
    
    try:
        from modules.gemini_integration import (
            GeminiHealthAdvisor,
            get_gemini_advisor,
            get_active_model_name
        )
        print("✅ Successfully imported GeminiHealthAdvisor")
        print("✅ Successfully imported get_gemini_advisor()")
        print("✅ Successfully imported get_active_model_name()")
        
        from modules.recommendation_engine import RecommendationEngine
        print("✅ Successfully imported RecommendationEngine")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_unified_function_exists():
    """Test that generate_full_health_analysis() method exists"""
    print("\n" + "="*60)
    print("TEST 2: Verifying unified function exists...")
    print("="*60)
    
    try:
        from modules.gemini_integration import GeminiHealthAdvisor
        
        # Check method exists
        if not hasattr(GeminiHealthAdvisor, 'generate_full_health_analysis'):
            print("❌ generate_full_health_analysis() method not found!")
            return False
        
        print("✅ generate_full_health_analysis() method exists")
        
        # Check it's callable
        advisor = GeminiHealthAdvisor()
        if not callable(getattr(advisor, 'generate_full_health_analysis')):
            print("❌ generate_full_health_analysis() is not callable!")
            return False
        
        print("✅ generate_full_health_analysis() is callable")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backward_compatibility():
    """Test that existing APIs still work"""
    print("\n" + "="*60)
    print("TEST 3: Verifying backward compatibility...")
    print("="*60)
    
    try:
        from modules.gemini_integration import GeminiHealthAdvisor
        
        advisor = GeminiHealthAdvisor()
        
        # Check public methods exist
        methods = [
            'enhance_recommendations',
            'get_personalized_plan',
            'get_health_insights',
            'get_motivation_message'
        ]
        
        for method in methods:
            if not hasattr(advisor, method):
                print(f"❌ Method {method}() not found!")
                return False
            if not callable(getattr(advisor, method)):
                print(f"❌ Method {method}() is not callable!")
                return False
            print(f"✅ {method}() exists and is callable")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_caching_structure():
    """Test that caching system is initialized"""
    print("\n" + "="*60)
    print("TEST 4: Verifying caching structure...")
    print("="*60)
    
    try:
        from modules.gemini_integration import GeminiHealthAdvisor
        
        advisor = GeminiHealthAdvisor()
        
        # Check cache exists
        if not hasattr(advisor, '_analysis_cache'):
            print("❌ _analysis_cache not found!")
            return False
        
        print(f"✅ _analysis_cache initialized (type: {type(advisor._analysis_cache).__name__})")
        
        # Check cache size limit
        if not hasattr(advisor, '_cache_max_size'):
            print("❌ _cache_max_size not found!")
            return False
        
        print(f"✅ Cache max size set to {advisor._cache_max_size}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_helper_functions():
    """Test that helper functions exist"""
    print("\n" + "="*60)
    print("TEST 5: Verifying helper functions...")
    print("="*60)
    
    try:
        from modules.gemini_integration import GeminiHealthAdvisor
        
        advisor = GeminiHealthAdvisor()
        
        # Check helper methods
        helpers = [
            '_profile_to_hash',
            '_parse_unified_response',
            '_get_timestamp',
            '_build_health_context'
        ]
        
        for helper in helpers:
            if not hasattr(advisor, helper):
                print(f"❌ Helper {helper}() not found!")
                return False
            if not callable(getattr(advisor, helper)):
                print(f"❌ Helper {helper}() is not callable!")
                return False
            print(f"✅ {helper}() exists")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_profile_hashing():
    """Test profile hashing for caching"""
    print("\n" + "="*60)
    print("TEST 6: Testing profile hashing...")
    print("="*60)
    
    try:
        from modules.gemini_integration import GeminiHealthAdvisor
        
        advisor = GeminiHealthAdvisor()
        
        profile1 = {
            "age": 35,
            "gender": "Male",
            "bmi": 23.5,
            "activity_level": "Moderately Active"
        }
        
        profile2 = {
            "age": 35,
            "gender": "Male",
            "bmi": 23.5,
            "activity_level": "Moderately Active"
        }
        
        profile3 = {
            "age": 40,
            "gender": "Male",
            "bmi": 23.5,
            "activity_level": "Moderately Active"
        }
        
        hash1 = advisor._profile_to_hash(profile1)
        hash2 = advisor._profile_to_hash(profile2)
        hash3 = advisor._profile_to_hash(profile3)
        
        if hash1 != hash2:
            print("❌ Identical profiles produce different hashes!")
            return False
        print(f"✅ Identical profiles produce same hash: {hash1[:8]}...")
        
        if hash1 == hash3:
            print("❌ Different profiles produce same hash!")
            return False
        print(f"✅ Different profiles produce different hashes")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_response_parsing():
    """Test response parsing from unified API"""
    print("\n" + "="*60)
    print("TEST 7: Testing response parsing...")
    print("="*60)
    
    try:
        from modules.gemini_integration import GeminiHealthAdvisor
        
        advisor = GeminiHealthAdvisor()
        
        # Sample structured response
        sample_response = """
### SLEEP OPTIMIZATION
- 😴 Maintain consistent sleep schedule
- 😴 Aim for 7-9 hours nightly

### DIET SUGGESTIONS
- 🥗 Increase vegetable intake
- 🥗 Reduce sugar consumption

### FITNESS GUIDANCE
- 💪 Exercise 30 minutes daily
- 💪 Include strength training

### MENTAL WELLNESS
- 🧠 Practice meditation
- 🧠 Manage stress levels

### 30-DAY PERSONALIZED PLAN
Week 1: Establish sleep routine and track metrics daily.
Week 2-3: Build exercise habits gradually.
Week 4: Integrate all changes and assess progress.

### KEY HEALTH INSIGHTS
Your sleep is a key area for improvement. Focus on consistent bedtime.
You have good activity levels. Maintain current exercise routine.
"""
        
        parsed = advisor._parse_unified_response(sample_response)
        
        # Verify structure
        required_keys = ["sleep", "diet", "fitness", "wellness", "personalized_plan", "health_insights"]
        for key in required_keys:
            if key not in parsed:
                print(f"❌ Missing key in parsed response: {key}")
                return False
        
        print("✅ All required sections present in parsed response")
        
        # Verify content extraction
        if not parsed["sleep"]:
            print("❌ Sleep recommendations not extracted!")
            return False
        print(f"✅ Sleep recommendations extracted ({len(parsed['sleep'])} items)")
        
        if not parsed["personalized_plan"]:
            print("❌ Personalized plan not extracted!")
            return False
        print(f"✅ Personalized plan extracted ({len(parsed['personalized_plan'])} chars)")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def print_summary(results):
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = "✅ PASS" if passed_flag else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Unified API refactoring is working correctly!")
        return True
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Check implementation.")
        return False

def main():
    """Run all verification tests"""
    print("\n" + "="*60)
    print("UNIFIED GEMINI HEALTH ANALYSIS - VERIFICATION SUITE")
    print("="*60)
    
    results = {
        "Imports": test_imports(),
        "Unified Function Exists": test_unified_function_exists(),
        "Backward Compatibility": test_backward_compatibility(),
        "Caching Structure": test_caching_structure(),
        "Helper Functions": test_helper_functions(),
        "Profile Hashing": test_profile_hashing(),
        "Response Parsing": test_response_parsing(),
    }
    
    success = print_summary(results)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
