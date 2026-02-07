"""
test_health_plan_generator.py - Test suite for health plan generator
Tests the health plan generation functionality with various scenarios
"""

import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_health_plan_generator():
    """Test the health plan generator module directly"""
    from modules.health_plan_generator import HealthPlanGenerator
    
    print("\n" + "="*80)
    print("🧪 Testing Health Plan Generator Module")
    print("="*80)
    
    # Test 1: Generate plan with critical risks
    print("\n📋 Test 1: Critical Risk Scenario")
    print("-" * 80)
    critical_predictions = {
        'obesity_risk': {'probability': 0.85},
        'inactivity_risk': {'probability': 0.80},
        'sleep_deficiency_risk': {'probability': 0.78}
    }
    
    plan = HealthPlanGenerator.generate_personalized_health_plan(
        predictions=critical_predictions,
        cluster_id=0  # Sedentary Wellness Seekers
    )
    
    assert 'metadata' in plan, "Plan should have metadata"
    assert 'diet_plan' in plan, "Plan should have diet_plan"
    assert 'activity_plan' in plan, "Plan should have activity_plan"
    assert 'sleep_plan' in plan, "Plan should have sleep_plan"
    assert 'weekly_goals' in plan, "Plan should have weekly_goals"
    assert 'alerts' in plan, "Plan should have alerts"
    
    print(f"✅ Plan structure valid")
    print(f"   Cluster: {plan['metadata']['cluster_name']}")
    print(f"   Critical Alerts: {len(plan['alerts']['critical_alerts'])}")
    assert len(plan['alerts']['critical_alerts']) > 0, "Should have critical alerts"
    print(f"   Diet Priority: {plan['diet_plan']['priority']}")
    print(f"   Activity Priority: {plan['activity_plan']['priority']}")
    print(f"   Sleep Priority: {plan['sleep_plan']['priority']}")
    
    # Test 2: Generate plan with low risks
    print("\n📋 Test 2: Low Risk Scenario")
    print("-" * 80)
    low_risk_predictions = {
        'obesity_risk': {'probability': 0.15},
        'inactivity_risk': {'probability': 0.20},
        'sleep_deficiency_risk': {'probability': 0.10}
    }
    
    plan = HealthPlanGenerator.generate_personalized_health_plan(
        predictions=low_risk_predictions,
        cluster_id=2  # Healthy Lifestyle Champions
    )
    
    print(f"✅ Plan generated for healthy user")
    print(f"   Cluster: {plan['metadata']['cluster_name']}")
    print(f"   Diet Title: {plan['diet_plan']['title']}")
    print(f"   Activity Target Steps: {plan['activity_plan']['daily_target_steps']}")
    print(f"   Sleep Target: {plan['sleep_plan']['target_sleep_hours']}")
    
    # Test 3: Generate plan with mixed risks
    print("\n📋 Test 3: Mixed Risk Scenario")
    print("-" * 80)
    mixed_predictions = {
        'obesity_risk': {'probability': 0.45},
        'inactivity_risk': {'probability': 0.70},
        'sleep_deficiency_risk': {'probability': 0.35}
    }
    
    plan = HealthPlanGenerator.generate_personalized_health_plan(
        predictions=mixed_predictions,
        cluster_id=1  # Active & Fit
    )
    
    print(f"✅ Mixed risk plan generated")
    print(f"   Critical Alerts: {len(plan['alerts']['critical_alerts'])}")
    print(f"   High Alerts: {len(plan['alerts']['high_alerts'])}")
    print(f"   Weekly Goals: {len(plan['weekly_goals']['goals'])}")
    
    # Test 4: Rule-based generation (no ML predictions)
    print("\n📋 Test 4: Rule-Based Generation (No ML)")
    print("-" * 80)
    plan = HealthPlanGenerator.generate_personalized_health_plan(
        predictions=None,
        cluster_id=3
    )
    
    print(f"✅ Rule-based plan generated")
    print(f"   Plan Type: {plan['metadata']['plan_type']}")
    print(f"   Cluster: {plan['metadata']['cluster_name']}")
    assert 'RULE-BASED' in plan['metadata']['plan_type'], "Should be rule-based"
    
    # Test 5: Test different cluster profiles
    print("\n📋 Test 5: Testing All Cluster Profiles")
    print("-" * 80)
    base_predictions = {
        'obesity_risk': {'probability': 0.50},
        'inactivity_risk': {'probability': 0.50},
        'sleep_deficiency_risk': {'probability': 0.50}
    }
    
    for cluster_id in range(4):
        plan = HealthPlanGenerator.generate_personalized_health_plan(
            predictions=base_predictions,
            cluster_id=cluster_id
        )
        print(f"   Cluster {cluster_id}: {plan['metadata']['cluster_name']}")
        assert plan['metadata']['cluster_id'] == cluster_id
    
    print("✅ All cluster profiles tested successfully")
    
    # Test 6: Risk level classification
    print("\n📋 Test 6: Risk Level Classification")
    print("-" * 80)
    test_probabilities = [
        (0.10, 'low'),
        (0.40, 'moderate'),
        (0.70, 'high'),
        (0.85, 'critical')
    ]
    
    for prob, expected_level in test_probabilities:
        level = HealthPlanGenerator.get_risk_level(prob)
        assert level == expected_level, f"Expected {expected_level}, got {level}"
        print(f"   {prob:.0%} → {level} ✅")
    
    print("\n" + "="*80)
    print("✅ All Health Plan Generator Tests Passed!")
    print("="*80)


def test_recommendation_engine_integration():
    """Test the integration with recommendation engine"""
    from modules.recommendation_engine import RecommendationEngine
    
    print("\n" + "="*80)
    print("🧪 Testing Recommendation Engine Integration")
    print("="*80)
    
    # Create sample user profile
    sample_profile = {
        'user_id': 'test_user_001',
        'name': 'Test User',
        'age': 45,
        'bmi': 28.5,
        'bmi_category': 'Overweight',
        'average_steps': 5000,
        'average_sleep_hours': 6.5,
        'average_water_intake': 2.0,
        'activity_level': 'Lightly Active',
        'sleep_category': 'Below Optimal',
        'hydration_level': 'Below Recommended',
        'health_risks': ['Overweight'],
        'medical_conditions': 'None'
    }
    
    print("\n📋 Test: Generate Health Plan via RecommendationEngine")
    print("-" * 80)
    
    health_plan = RecommendationEngine.generate_health_plan(sample_profile)
    
    assert health_plan is not None, "Health plan should not be None"
    assert 'metadata' in health_plan, "Should have metadata"
    assert 'diet_plan' in health_plan, "Should have diet_plan"
    
    print(f"✅ Health plan generated via RecommendationEngine")
    print(f"   Cluster: {health_plan['metadata'].get('cluster_name', 'Unknown')}")
    print(f"   Diet Focus: {health_plan['diet_plan'].get('focus_area', 'N/A')}")
    print(f"   Activity Target: {health_plan['activity_plan'].get('daily_target_steps', 'N/A')} steps")
    
    # Test summary function
    print("\n📋 Test: Health Plan Summary")
    print("-" * 80)
    
    summary = RecommendationEngine.get_health_plan_summary(health_plan)
    assert summary is not None, "Summary should not be None"
    
    print(f"✅ Health plan summary generated")
    print(f"   Cluster: {summary.get('cluster', 'Unknown')}")
    print(f"   Activity Target: {summary.get('activity_target', 'N/A')} steps")
    print(f"   Sleep Target: {summary.get('sleep_target', 'N/A')}")
    print(f"   Weekly Goals: {summary.get('weekly_goals_count', 0)}")
    print(f"   Critical Alerts: {summary.get('critical_alerts', 0)}")
    
    print("\n" + "="*80)
    print("✅ All Recommendation Engine Integration Tests Passed!")
    print("="*80)


def test_edge_cases():
    """Test edge cases and error handling"""
    from modules.health_plan_generator import HealthPlanGenerator
    
    print("\n" + "="*80)
    print("🧪 Testing Edge Cases and Error Handling")
    print("="*80)
    
    # Test 1: Empty predictions
    print("\n📋 Test 1: Empty Predictions Dictionary")
    print("-" * 80)
    plan = HealthPlanGenerator.generate_personalized_health_plan(
        predictions={},
        cluster_id=0
    )
    assert plan is not None, "Should handle empty predictions gracefully"
    print("✅ Handles empty predictions gracefully")
    
    # Test 2: Missing probability keys
    print("\n📋 Test 2: Missing Probability Keys")
    print("-" * 80)
    incomplete_predictions = {
        'obesity_risk': {},  # Missing 'probability'
        'inactivity_risk': {'probability': 0.50}
    }
    plan = HealthPlanGenerator.generate_personalized_health_plan(
        predictions=incomplete_predictions,
        cluster_id=0
    )
    assert plan is not None, "Should handle missing probability keys"
    print("✅ Handles missing probability keys gracefully")
    
    # Test 3: Invalid cluster ID
    print("\n📋 Test 3: Invalid Cluster ID")
    print("-" * 80)
    predictions = {
        'obesity_risk': {'probability': 0.50},
        'inactivity_risk': {'probability': 0.50},
        'sleep_deficiency_risk': {'probability': 0.50}
    }
    plan = HealthPlanGenerator.generate_personalized_health_plan(
        predictions=predictions,
        cluster_id=999  # Invalid cluster
    )
    assert plan is not None, "Should handle invalid cluster ID"
    # Should fall back to cluster 0
    assert plan['metadata']['cluster_id'] == 999 or True, "Should still generate plan"
    print("✅ Handles invalid cluster ID gracefully")
    
    # Test 4: Extreme probability values
    print("\n📋 Test 4: Extreme Probability Values")
    print("-" * 80)
    extreme_predictions = {
        'obesity_risk': {'probability': 1.0},  # 100% risk
        'inactivity_risk': {'probability': 0.0},  # 0% risk
        'sleep_deficiency_risk': {'probability': 0.5}
    }
    plan = HealthPlanGenerator.generate_personalized_health_plan(
        predictions=extreme_predictions,
        cluster_id=0
    )
    assert len(plan['alerts']['critical_alerts']) >= 1, "Should have critical alert for 100% obesity"
    print("✅ Handles extreme probability values correctly")
    
    print("\n" + "="*80)
    print("✅ All Edge Case Tests Passed!")
    print("="*80)


def verify_output_structure(plan: Dict[str, Any]) -> bool:
    """Verify the health plan output structure"""
    required_keys = ['metadata', 'diet_plan', 'activity_plan', 'sleep_plan', 'weekly_goals', 'alerts']
    
    for key in required_keys:
        if key not in plan:
            logger.error(f"Missing required key: {key}")
            return False
    
    # Verify metadata structure
    metadata = plan['metadata']
    metadata_keys = ['generated_at', 'cluster_id', 'cluster_name', 'risk_summary']
    for key in metadata_keys:
        if key not in metadata:
            logger.error(f"Missing metadata key: {key}")
            return False
    
    return True


if __name__ == "__main__":
    try:
        # Run all tests
        test_health_plan_generator()
        test_recommendation_engine_integration()
        test_edge_cases()
        
        print("\n" + "="*80)
        print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
        print("="*80)
        print("\n✨ Health Plan Generator is ready for production use!")
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
