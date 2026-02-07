"""
test_ml_engine.py - Test script for AI Health Engine
Verifies that ML models train and make predictions correctly
"""

import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_ml_engine():
    """Test the AI Health Engine functionality"""
    
    logger.info("=" * 70)
    logger.info("🧪 TESTING AI HEALTH ENGINE")
    logger.info("=" * 70)
    
    try:
        # Import the engine
        from modules.ai_health_engine import AIHealthEngine, AIRecommendationGenerator
        logger.info("✅ Successfully imported AI Health Engine modules")
    except ImportError as e:
        logger.error(f"❌ Failed to import AI Health Engine: {e}")
        logger.error("Make sure scikit-learn and joblib are installed")
        return False
    
    try:
        # Initialize engine
        engine = AIHealthEngine(model_dir="models")
        logger.info("✅ AI Health Engine initialized")
        
        # Prepare training data
        logger.info("\n📊 Preparing training data...")
        df, success = engine.prepare_training_data_from_json("data/user_records.json", "data/user_profiles.json")
        
        if not success:
            logger.error("❌ Failed to prepare training data")
            return False
        
        logger.info(f"✅ Prepared {len(df)} training samples")
        
        # Train models
        logger.info("\n🧠 Training predictive models...")
        if not engine.train_models(df):
            logger.error("❌ Failed to train models")
            return False
        
        logger.info("✅ Models trained successfully")
        
        # Train clustering
        logger.info("\n🎯 Training clustering model...")
        if not engine.train_clustering(df, n_clusters=4):
            logger.error("❌ Failed to train clustering")
            return False
        
        logger.info("✅ Clustering model trained successfully")
        
        # Test prediction
        logger.info("\n🔮 Testing health risk predictions...")
        test_user = {
            'age': 35,
            'bmi': 28.5,
            'daily_steps': 6000,
            'sleep_hours': 6.5,
            'water_intake': 2.0,
        }
        
        predictions = engine.predict_health_risks(test_user)
        
        if predictions:
            logger.info("✅ Health risk predictions:")
            for risk_type, risk_data in predictions.items():
                prob = risk_data.get('probability', 0)
                level = risk_data.get('risk_level', 'Unknown')
                logger.info(f"   - {risk_type}: {prob:.1%} ({level})")
        else:
            logger.error("❌ Failed to get predictions")
            return False
        
        # Test clustering
        logger.info("\n👥 Testing user clustering...")
        cluster_info = engine.assign_user_cluster(test_user)
        
        if cluster_info:
            logger.info("✅ User clustering results:")
            logger.info(f"   - Cluster ID: {cluster_info.get('cluster_id')}")
            logger.info(f"   - Cluster Name: {cluster_info.get('cluster_name')}")
            template = cluster_info.get('template', {})
            if template:
                logger.info(f"   - Focus Area: {template.get('focus_area')}")
                priorities = template.get('priority_recommendations', [])
                if priorities:
                    logger.info(f"   - Priorities: {priorities[0]}")
        else:
            logger.error("❌ Failed to assign cluster")
            return False
        
        # Test recommendation generator
        logger.info("\n📋 Testing recommendation generator...")
        recommendation_gen = AIRecommendationGenerator(engine)
        
        profile = {
            'age': 35,
            'bmi': 28.5,
            'average_steps': 6000,
            'average_sleep_hours': 6.5,
            'average_water_intake': 2.0,
            'medical_conditions': 'None'
        }
        
        recommendations = recommendation_gen.generate_ml_driven_recommendations(
            profile, predictions, cluster_info
        )
        
        if recommendations:
            logger.info("✅ Generated ML-driven recommendations:")
            for category, recs in recommendations.items():
                if recs:
                    logger.info(f"   - {category.upper()}: {len(recs)} recommendations")
        else:
            logger.error("❌ Failed to generate recommendations")
            return False
        
        # Save models
        logger.info("\n💾 Saving trained models...")
        if engine.save_models("models"):
            logger.info("✅ Models saved successfully")
        else:
            logger.error("❌ Failed to save models")
            return False
        
        # Test loading models
        logger.info("\n📂 Testing model loading...")
        engine2 = AIHealthEngine(model_dir="models")
        if engine2.load_models("models"):
            logger.info("✅ Models loaded successfully")
        else:
            logger.error("❌ Failed to load models")
            return False
        
        # Test recommendations with loaded models
        predictions2 = engine2.predict_health_risks(test_user)
        if predictions2:
            logger.info("✅ Predictions work with loaded models")
        else:
            logger.error("❌ Failed to predict with loaded models")
            return False
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ ALL TESTS PASSED!")
        logger.info("=" * 70)
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_recommendation_engine_integration():
    """Test integration of RecommendationEngine with ML"""
    
    logger.info("\n" + "=" * 70)
    logger.info("🧪 TESTING RECOMMENDATION ENGINE INTEGRATION")
    logger.info("=" * 70)
    
    try:
        from modules.recommendation_engine import RecommendationEngine
        
        logger.info("\n🚀 Initializing ML engine via RecommendationEngine...")
        success = RecommendationEngine.initialize_ml_engine(data_dir="data", model_dir="models")
        
        if success:
            logger.info("✅ ML engine initialized successfully through RecommendationEngine")
        else:
            logger.warning("⚠️ ML engine initialization reported issues (may be using fallback)")
        
        # Test get_ml_status
        status = RecommendationEngine.get_ml_status()
        logger.info("\n📊 ML Engine Status:")
        logger.info(f"   - ML Available: {status.get('ml_available')}")
        logger.info(f"   - ML Initialized: {status.get('ml_initialized')}")
        logger.info(f"   - Engine: {status.get('engine')}")
        logger.info(f"   - Recommendation Generator: {status.get('recommendation_generator')}")
        
        # Test comprehensive recommendations with ML
        profile = {
            'age': 35,
            'bmi': 28.5,
            'average_steps': 6000,
            'average_sleep_hours': 6.5,
            'average_water_intake': 2.0,
            'medical_conditions': 'None',
            'activity_level': 'Lightly Active',
            'bmi_category': 'Overweight',
            'sleep_category': 'Below Optimal',
            'hydration_level': 'Below Recommended',
            'health_risks': []
        }
        
        logger.info("\n📋 Generating comprehensive recommendations with ML...")
        recommendations = RecommendationEngine.generate_comprehensive_recommendations(
            profile, use_ml_predictions=True, use_ai_enhancement=False
        )
        
        if recommendations:
            logger.info("✅ Comprehensive recommendations generated:")
            for category, recs in recommendations.items():
                if recs:
                    logger.info(f"   - {category.upper()}: {len(recs)} recommendations")
                    # Show first recommendation
                    if recs:
                        logger.info(f"     • {recs[0]}")
        else:
            logger.error("❌ Failed to generate comprehensive recommendations")
            return False
        
        # Test ML health risks
        logger.info("\n🔮 Getting ML health risks...")
        ml_risks = RecommendationEngine.get_ml_health_risks(profile)
        
        if ml_risks:
            logger.info("✅ ML health risks retrieved:")
            for risk_type, risk_info in ml_risks.items():
                prob = risk_info.get('probability', 0)
                level = risk_info.get('risk_level', 'Unknown')
                logger.info(f"   - {risk_type}: {prob:.1%} ({level})")
        else:
            logger.warning("⚠️ No ML health risks available (may be using rule-based only)")
        
        # Test cluster assignment
        logger.info("\n👥 Getting user cluster assignment...")
        cluster = RecommendationEngine.get_user_cluster_assignment(profile)
        
        if cluster:
            logger.info("✅ User cluster assignment retrieved:")
            logger.info(f"   - Cluster ID: {cluster.get('cluster_id')}")
            logger.info(f"   - Cluster Name: {cluster.get('cluster_name')}")
        else:
            logger.warning("⚠️ No cluster assignment available")
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ INTEGRATION TESTS PASSED!")
        logger.info("=" * 70)
        return True
        
    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    logger.info("Starting AI Health Engine tests...\n")
    
    # Run tests
    test1_success = test_ml_engine()
    test2_success = test_recommendation_engine_integration()
    
    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("📊 TEST SUMMARY")
    logger.info("=" * 70)
    logger.info(f"ML Engine Test: {'✅ PASSED' if test1_success else '❌ FAILED'}")
    logger.info(f"Integration Test: {'✅ PASSED' if test2_success else '❌ FAILED'}")
    
    if test1_success and test2_success:
        logger.info("\n✅ ALL TESTS PASSED - Ready for production!")
        sys.exit(0)
    else:
        logger.info("\n⚠️ Some tests failed - Check logs above for details")
        sys.exit(1)
