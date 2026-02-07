"""
ai_health_engine.py - Machine Learning-powered health recommendation engine
Implements predictive models for health risk assessment and user clustering for personalization
Uses local ML models (LogisticRegression, RandomForestClassifier, GradientBoostingClassifier)
and KMeans clustering for user segmentation
"""

import json
import logging
import os
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Suppress sklearn warnings
warnings.filterwarnings('ignore', category=UserWarning)


class AIHealthEngine:
    """
    Machine Learning-powered health analysis engine
    Provides predictive models and clustering for personalized recommendations
    """
    
    def __init__(self, model_dir: str = "models"):
        """
        Initialize the AI Health Engine
        
        Args:
            model_dir: Directory to store/load trained models
        """
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        
        # Model storage
        self.obesity_model = None
        self.inactivity_model = None
        self.sleep_deficiency_model = None
        self.clustering_model = None
        self.feature_scaler = None
        self.cluster_scaler = None
        
        # Cluster personalization templates
        self.cluster_templates = {}
        
        # Feature names for training
        self.feature_names = ['bmi', 'daily_steps', 'sleep_hours', 'water_intake', 'age']
        self.cluster_feature_names = ['daily_steps', 'bmi', 'sleep_hours', 'water_intake']
        
        logger.info("✅ AI Health Engine initialized")
    
    def prepare_training_data_from_json(self, records_file: str, profiles_file: str) -> Tuple[pd.DataFrame, bool]:
        """
        Prepare training data from existing JSON files
        
        Args:
            records_file: Path to user_records.json
            profiles_file: Path to user_profiles.json
            
        Returns:
            Tuple of (DataFrame with training data, success bool)
        """
        try:
            # Load profiles to get summarized data
            with open(profiles_file, 'r') as f:
                profiles_data = json.load(f)
            
            records = []
            
            # Extract features from each profile
            for profile in profiles_data.get('profiles', []):
                user_id = profile.get('user_id')
                data = profile.get('data', {})
                
                # Extract required features
                record = {
                    'user_id': user_id,
                    'age': data.get('age', 35),
                    'bmi': data.get('bmi', 25.0),
                    'daily_steps': data.get('average_steps', 7000),
                    'sleep_hours': data.get('average_sleep_hours', 7.5),
                    'water_intake': data.get('average_water_intake', 2.5),
                    'activity_level': data.get('activity_level', 'Moderately Active'),
                    'bmi_category': data.get('bmi_category', 'Normal Weight'),
                    'medical_conditions': data.get('medical_conditions', 'None'),
                }
                
                # Add risk labels based on realistic health science thresholds
                # Use probabilistic approach for more nuanced risk assessment
                
                # Obesity Risk: Probability increases with BMI (sigmoid curve centered at BMI=27)
                obesity_prob = 1 / (1 + np.exp(-(record['bmi'] - 27) / 2))
                record['obesity_risk'] = 1 if np.random.random() < obesity_prob else 0
                
                # Inactivity Risk: Probability increases as daily steps decrease (centered at 5500)
                inactivity_prob = 1 / (1 + np.exp(-(record['daily_steps'] - 5500) / 1500))
                record['inactivity_risk'] = 1 if np.random.random() < inactivity_prob else 0
                
                # Sleep Deficiency Risk: Probability increases with too little sleep
                sleep_prob = 1 / (1 + np.exp(-(record['sleep_hours'] - 6.5) / 1.5))
                record['sleep_deficiency_risk'] = 1 if np.random.random() < sleep_prob else 0
                
                records.append(record)
            
            df = pd.DataFrame(records)
            
            if len(df) == 0:
                logger.warning("⚠️ No training data found in JSON files. Using synthetic data.")
                df = self._generate_synthetic_training_data()
            else:
                logger.info(f"📊 Loaded {len(df)} user profiles for training")
            
            return df, True
            
        except Exception as e:
            logger.error(f"❌ Error preparing training data: {e}")
            logger.info("🤖 Generating synthetic training data instead")
            return self._generate_synthetic_training_data(), True
    
    def _generate_synthetic_training_data(self, num_samples: int = 200) -> pd.DataFrame:
        """
        Generate realistic synthetic health data for model training
        Creates data with meaningful health risk patterns based on medical science
        
        Args:
            num_samples: Number of synthetic samples to generate
            
        Returns:
            DataFrame with realistic synthetic health data
        """
        np.random.seed(42)
        
        # Create realistic health profiles with correlated features
        ages = np.random.normal(45, 15, num_samples)
        ages = np.clip(ages, 18, 85).astype(int)
        
        # Generate BMI with age correlation (older people tend to have higher BMI)
        base_bmi = 24 + (ages - 30) * 0.15 + np.random.normal(0, 3, num_samples)
        bmi = np.clip(base_bmi, 15, 45)
        
        # Generate daily steps (inversely correlates with BMI and age)
        base_steps = 10000 - (bmi - 25) * 400 - (ages - 30) * 50
        daily_steps = np.clip(base_steps + np.random.normal(0, 1500, num_samples), 500, 25000)
        
        # Generate sleep hours (varies with age)
        base_sleep = 7 - (ages - 30) * 0.02 + np.random.normal(0, 1, num_samples)
        sleep_hours = np.clip(base_sleep, 3, 12)
        
        # Generate water intake (somewhat independent but healthier people drink more)
        water = 2.5 + daily_steps / 8000 * 0.7 + np.random.normal(0, 0.6, num_samples)
        water_intake = np.clip(water, 0.5, 6)
        
        data = {
            'user_id': [f'synthetic_user_{i}' for i in range(num_samples)],
            'age': ages,
            'bmi': bmi,
            'daily_steps': daily_steps,
            'sleep_hours': sleep_hours,
            'water_intake': water_intake,
        }
        
        df = pd.DataFrame(data)
        
        # Create health risk labels based on REALISTIC health science thresholds
        # Obesity Risk: Based on BMI and age (higher BMI = higher risk)
        # Medical consensus: BMI >= 30 is obese, >= 25 is overweight
        obesity_probability = 1 / (1 + np.exp(-(df['bmi'] - 27) / 2))  # Sigmoid function
        df['obesity_risk'] = (np.random.random(num_samples) < obesity_probability).astype(int)
        
        # Inactivity Risk: Based on daily steps
        # Medical consensus: <5000 steps/day is sedentary, 5000-7500 is low active
        inactivity_probability = 1 / (1 + np.exp(-(df['daily_steps'] - 5500) / 1500))
        df['inactivity_risk'] = (np.random.random(num_samples) < inactivity_probability).astype(int)
        
        # Sleep Deficiency Risk: Based on sleep hours and age
        # Medical consensus: <6 hours = deficient, 6-8 = adequate, >8 = excess
        adjusted_sleep_threshold = 6.5 + (df['age'] - 40) * 0.01
        sleep_probability = 1 / (1 + np.exp(-(df['sleep_hours'] - adjusted_sleep_threshold) / 1.5))
        df['sleep_deficiency_risk'] = (np.random.random(num_samples) < sleep_probability).astype(int)
        
        logger.info(f"🔄 Generated {num_samples} realistic synthetic training samples")
        logger.info(f"  - Obesity Risk Prevalence: {df['obesity_risk'].mean():.1%}")
        logger.info(f"  - Inactivity Risk Prevalence: {df['inactivity_risk'].mean():.1%}")
        logger.info(f"  - Sleep Deficiency Risk Prevalence: {df['sleep_deficiency_risk'].mean():.1%}")
        
        return df
    
    def train_models(self, df: pd.DataFrame) -> bool:
        """
        Train predictive models for health risks
        
        Args:
            df: Training DataFrame with features and labels
            
        Returns:
            True if training successful, False otherwise
        """
        try:
            logger.info("🧠 Starting ML model training...")
            
            # Ensure required features exist
            for feature in self.feature_names:
                if feature not in df.columns:
                    logger.warning(f"⚠️ Missing feature '{feature}', using default values")
                    df[feature] = df.get(feature, 0)
            
            # Prepare features and scale them
            X = df[self.feature_names].fillna(0)
            self.feature_scaler = StandardScaler()
            X_scaled = self.feature_scaler.fit_transform(X)
            
            # Train Obesity Risk Model
            logger.info("📈 Training Obesity Risk Predictor...")
            y_obesity = df['obesity_risk'].fillna(0)
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y_obesity, test_size=0.2, random_state=42
            )
            
            self.obesity_model = RandomForestClassifier(
                n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
            )
            self.obesity_model.fit(X_train, y_train)
            obesity_score = self.obesity_model.score(X_test, y_test)
            logger.info(f"✅ Obesity Risk Model trained (Accuracy: {obesity_score:.2%})")
            
            # Train Inactivity Risk Model
            logger.info("📈 Training Inactivity Risk Predictor...")
            y_inactivity = df['inactivity_risk'].fillna(0)
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y_inactivity, test_size=0.2, random_state=42
            )
            
            self.inactivity_model = GradientBoostingClassifier(
                n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42
            )
            self.inactivity_model.fit(X_train, y_train)
            inactivity_score = self.inactivity_model.score(X_test, y_test)
            logger.info(f"✅ Inactivity Risk Model trained (Accuracy: {inactivity_score:.2%})")
            
            # Train Sleep Deficiency Risk Model
            logger.info("📈 Training Sleep Deficiency Risk Predictor...")
            y_sleep = df['sleep_deficiency_risk'].fillna(0)
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y_sleep, test_size=0.2, random_state=42
            )
            
            self.sleep_deficiency_model = LogisticRegression(random_state=42, max_iter=200)
            self.sleep_deficiency_model.fit(X_train, y_train)
            sleep_score = self.sleep_deficiency_model.score(X_test, y_test)
            logger.info(f"✅ Sleep Deficiency Model trained (Accuracy: {sleep_score:.2%})")
            
            logger.info("🎓 All predictive models trained successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error training models: {e}")
            return False
    
    def train_clustering(self, df: pd.DataFrame, n_clusters: int = 4) -> bool:
        """
        Train KMeans clustering for user segmentation and personalization
        
        Args:
            df: Training DataFrame
            n_clusters: Number of user lifestyle clusters
            
        Returns:
            True if clustering successful, False otherwise
        """
        try:
            logger.info(f"🎯 Starting User Clustering (k={n_clusters})...")
            
            # Prepare clustering features
            cluster_features = self.cluster_feature_names
            for feature in cluster_features:
                if feature not in df.columns:
                    logger.warning(f"⚠️ Missing feature '{feature}', using default")
                    df[feature] = 0
            
            X_cluster = df[cluster_features].fillna(0)
            self.cluster_scaler = StandardScaler()
            X_cluster_scaled = self.cluster_scaler.fit_transform(X_cluster)
            
            # Train clustering model
            self.clustering_model = KMeans(
                n_clusters=n_clusters, random_state=42, n_init=10
            )
            clusters = self.clustering_model.fit_predict(X_cluster_scaled)
            df['cluster'] = clusters
            
            logger.info(f"✅ Clustering model trained with {n_clusters} lifestyle clusters")
            
            # Generate personalized templates for each cluster
            self._generate_cluster_templates(df)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error training clustering model: {e}")
            return False
    
    def _generate_cluster_templates(self, df: pd.DataFrame):
        """
        Generate personalized recommendation templates for each user cluster
        
        Args:
            df: DataFrame with cluster assignments
        """
        logger.info("📋 Generating cluster-based recommendation templates...")
        
        for cluster_id in sorted(df['cluster'].unique()):
            cluster_data = df[df['cluster'] == cluster_id]
            
            # Calculate cluster characteristics
            avg_steps = cluster_data['daily_steps'].mean()
            avg_bmi = cluster_data['bmi'].mean()
            avg_sleep = cluster_data['sleep_hours'].mean()
            avg_water = cluster_data['water_intake'].mean()
            avg_age = cluster_data['age'].mean()
            
            # Determine cluster profile
            if avg_steps < 5000 and avg_bmi > 27:
                cluster_name = "Sedentary Wellness Seekers"
                focus = "activity and weight management"
            elif avg_steps >= 8000 and avg_sleep >= 7.5:
                cluster_name = "Healthy Lifestyle Champions"
                focus = "maintenance and optimization"
            elif avg_steps >= 5000 and avg_bmi < 25:
                cluster_name = "Active & Fit"
                focus = "performance and consistency"
            else:
                cluster_name = "Balanced Progressors"
                focus = "sustainable improvement"
            
            # Create personalized template
            template = {
                'cluster_id': int(cluster_id),
                'name': cluster_name,
                'size': len(cluster_data),
                'characteristics': {
                    'avg_steps': round(avg_steps, 1),
                    'avg_bmi': round(avg_bmi, 2),
                    'avg_sleep': round(avg_sleep, 1),
                    'avg_water_intake': round(avg_water, 2),
                    'avg_age': round(avg_age, 1),
                },
                'focus_area': focus,
                'priority_recommendations': self._get_cluster_priorities(
                    cluster_id, cluster_data
                )
            }
            
            self.cluster_templates[int(cluster_id)] = template
            logger.info(f"📌 Cluster {cluster_id}: {cluster_name} (n={len(cluster_data)})")
    
    def _get_cluster_priorities(self, cluster_id: int, cluster_data: pd.DataFrame) -> List[str]:
        """
        Determine priority recommendations for a specific cluster
        
        Args:
            cluster_id: Cluster identifier
            cluster_data: DataFrame subset for this cluster
            
        Returns:
            List of priority recommendation areas
        """
        priorities = []
        
        avg_steps = cluster_data['daily_steps'].mean()
        avg_bmi = cluster_data['bmi'].mean()
        avg_sleep = cluster_data['sleep_hours'].mean()
        avg_water = cluster_data['water_intake'].mean()
        
        if avg_steps < 6000:
            priorities.append("Increase daily physical activity")
        
        if avg_bmi > 27:
            priorities.append("Weight management and nutrition")
        
        if avg_sleep < 7:
            priorities.append("Improve sleep quality and duration")
        
        if avg_water < 2:
            priorities.append("Hydration awareness")
        
        if not priorities:
            priorities.append("Maintain current healthy habits")
        
        return priorities
    
    def predict_health_risks(self, user_features: Dict[str, float]) -> Dict[str, Any]:
        """
        Predict health risks for a user using trained ML models
        
        Args:
            user_features: Dictionary with keys: age, bmi, daily_steps, sleep_hours, water_intake
            
        Returns:
            Dictionary with risk predictions and confidence scores
        """
        if self.obesity_model is None or self.feature_scaler is None:
            logger.warning("⚠️ Models not trained. Train models first.")
            return {}
        
        try:
            # Extract user features for detailed logging
            bmi = user_features.get('bmi', 25)
            steps = user_features.get('daily_steps', 7000)
            sleep = user_features.get('sleep_hours', 7.5)
            water = user_features.get('water_intake', 2.5)
            age = user_features.get('age', 35)
            
            logger.info(f"\n📊 Analyzing user health data:")
            logger.info(f"   • Age: {age} years")
            logger.info(f"   • BMI: {bmi:.1f} (Reference: 18.5-24.9 is healthy)")
            logger.info(f"   • Daily Steps: {steps:,.0f} (Reference: 7000-10000 is healthy)")
            logger.info(f"   • Sleep: {sleep:.1f} hours (Reference: 6-8 hours is healthy)")
            logger.info(f"   • Water Intake: {water:.1f} liters")
            
            # Prepare feature vector
            feature_vector = np.array([[bmi, steps, sleep, water, age]])
            
            # Scale features
            feature_scaled = self.feature_scaler.transform(feature_vector)
            
            # Get predictions and probabilities
            obesity_pred = self.obesity_model.predict(feature_scaled)[0]
            obesity_prob = self.obesity_model.predict_proba(feature_scaled)[0][1]
            
            inactivity_pred = self.inactivity_model.predict(feature_scaled)[0]
            inactivity_prob = self.inactivity_model.predict_proba(feature_scaled)[0][1]
            
            sleep_pred = self.sleep_deficiency_model.predict(feature_scaled)[0]
            sleep_prob = self.sleep_deficiency_model.predict_proba(feature_scaled)[0][1]
            
            logger.info(f"\n🎯 ML Risk Predictions:")
            logger.info(f"   • Obesity Risk: {obesity_prob:.1%} {'⚠️ HIGH' if obesity_prob > 0.6 else '✅ LOW'}")
            if obesity_prob > 0.3:
                if bmi > 25:
                    logger.warning(f"     → BMI {bmi:.1f} is {'overweight' if bmi < 30 else 'HIGH - obese'} range")
            
            logger.info(f"   • Inactivity Risk: {inactivity_prob:.1%} {'⚠️ HIGH' if inactivity_prob > 0.6 else '✅ LOW'}")
            if inactivity_prob > 0.3:
                if steps < 7000:
                    logger.warning(f"     → {steps:,.0f} steps/day is below recommended 7000-10000")
            
            logger.info(f"   • Sleep Deficiency Risk: {sleep_prob:.1%} {'⚠️ HIGH' if sleep_prob > 0.6 else '✅ LOW'}")
            if sleep_prob > 0.3:
                if sleep < 6.5:
                    logger.warning(f"     → {sleep:.1f} hours/night is below recommended 6.5-8 hours")
            
            
            return {
                'obesity_risk': {
                    'predicted': bool(obesity_pred),
                    'probability': float(obesity_prob),
                    'risk_level': self._risk_level(obesity_prob)
                },
                'inactivity_risk': {
                    'predicted': bool(inactivity_pred),
                    'probability': float(inactivity_prob),
                    'risk_level': self._risk_level(inactivity_prob)
                },
                'sleep_deficiency_risk': {
                    'predicted': bool(sleep_pred),
                    'probability': float(sleep_prob),
                    'risk_level': self._risk_level(sleep_prob)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error making predictions: {e}")
            return {}
    
    def assign_user_cluster(self, user_features: Dict[str, float]) -> Dict[str, Any]:
        """
        Assign user to a lifestyle cluster
        
        Args:
            user_features: Dictionary with cluster features
            
        Returns:
            Dictionary with cluster assignment and personalization info
        """
        if self.clustering_model is None or self.cluster_scaler is None:
            logger.warning("⚠️ Clustering model not trained")
            return {}
        
        try:
            # Prepare feature vector for clustering
            feature_vector = np.array([[
                user_features.get('daily_steps', 7000),
                user_features.get('bmi', 25),
                user_features.get('sleep_hours', 7.5),
                user_features.get('water_intake', 2.5),
            ]])
            
            # Scale features
            feature_scaled = self.cluster_scaler.transform(feature_vector)
            
            # Predict cluster
            cluster_id = self.clustering_model.predict(feature_scaled)[0]
            
            # Get cluster template
            template = self.cluster_templates.get(int(cluster_id), {})
            
            logger.info(
                f"👥 Cluster Assignment - Cluster {cluster_id}: {template.get('name', 'Unknown')}"
            )
            
            return {
                'cluster_id': int(cluster_id),
                'cluster_name': template.get('name', f'Cluster {cluster_id}'),
                'template': template,
                'is_personalized': True
            }
            
        except Exception as e:
            logger.error(f"❌ Error assigning cluster: {e}")
            return {}
    
    @staticmethod
    def _risk_level(probability: float) -> str:
        """Convert probability to risk level"""
        if probability < 0.3:
            return "Low"
        elif probability < 0.6:
            return "Moderate"
        elif probability < 0.8:
            return "High"
        else:
            return "Critical"
    
    def save_models(self, model_dir: Optional[str] = None) -> bool:
        """
        Save trained models to disk using joblib
        
        Args:
            model_dir: Directory to save models (uses self.model_dir if None)
            
        Returns:
            True if successful, False otherwise
        """
        model_dir = model_dir or self.model_dir
        os.makedirs(model_dir, exist_ok=True)
        
        try:
            if self.obesity_model:
                joblib.dump(self.obesity_model, os.path.join(model_dir, 'obesity_model.joblib'))
                logger.info("💾 Saved obesity_model.joblib")
            
            if self.inactivity_model:
                joblib.dump(self.inactivity_model, os.path.join(model_dir, 'inactivity_model.joblib'))
                logger.info("💾 Saved inactivity_model.joblib")
            
            if self.sleep_deficiency_model:
                joblib.dump(self.sleep_deficiency_model, os.path.join(model_dir, 'sleep_model.joblib'))
                logger.info("💾 Saved sleep_model.joblib")
            
            if self.feature_scaler:
                joblib.dump(self.feature_scaler, os.path.join(model_dir, 'feature_scaler.joblib'))
                logger.info("💾 Saved feature_scaler.joblib")
            
            if self.clustering_model:
                joblib.dump(self.clustering_model, os.path.join(model_dir, 'clustering_model.joblib'))
                logger.info("💾 Saved clustering_model.joblib")
            
            if self.cluster_scaler:
                joblib.dump(self.cluster_scaler, os.path.join(model_dir, 'cluster_scaler.joblib'))
                logger.info("💾 Saved cluster_scaler.joblib")
            
            # Save cluster templates as JSON
            if self.cluster_templates:
                with open(os.path.join(model_dir, 'cluster_templates.json'), 'w') as f:
                    json.dump(self.cluster_templates, f, indent=2)
                logger.info("💾 Saved cluster_templates.json")
            
            logger.info(f"✅ All models saved to {model_dir}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving models: {e}")
            return False
    
    def load_models(self, model_dir: Optional[str] = None) -> bool:
        """
        Load trained models from disk
        
        Args:
            model_dir: Directory to load models from
            
        Returns:
            True if successful, False otherwise
        """
        model_dir = model_dir or self.model_dir
        
        try:
            obesity_path = os.path.join(model_dir, 'obesity_model.joblib')
            if os.path.exists(obesity_path):
                self.obesity_model = joblib.load(obesity_path)
                logger.info("📂 Loaded obesity_model.joblib")
            
            inactivity_path = os.path.join(model_dir, 'inactivity_model.joblib')
            if os.path.exists(inactivity_path):
                self.inactivity_model = joblib.load(inactivity_path)
                logger.info("📂 Loaded inactivity_model.joblib")
            
            sleep_path = os.path.join(model_dir, 'sleep_model.joblib')
            if os.path.exists(sleep_path):
                self.sleep_deficiency_model = joblib.load(sleep_path)
                logger.info("📂 Loaded sleep_model.joblib")
            
            scaler_path = os.path.join(model_dir, 'feature_scaler.joblib')
            if os.path.exists(scaler_path):
                self.feature_scaler = joblib.load(scaler_path)
                logger.info("📂 Loaded feature_scaler.joblib")
            
            clustering_path = os.path.join(model_dir, 'clustering_model.joblib')
            if os.path.exists(clustering_path):
                self.clustering_model = joblib.load(clustering_path)
                logger.info("📂 Loaded clustering_model.joblib")
            
            cluster_scaler_path = os.path.join(model_dir, 'cluster_scaler.joblib')
            if os.path.exists(cluster_scaler_path):
                self.cluster_scaler = joblib.load(cluster_scaler_path)
                logger.info("📂 Loaded cluster_scaler.joblib")
            
            templates_path = os.path.join(model_dir, 'cluster_templates.json')
            if os.path.exists(templates_path):
                with open(templates_path, 'r') as f:
                    self.cluster_templates = json.load(f)
                logger.info("📂 Loaded cluster_templates.json")
            
            all_loaded = all([
                self.obesity_model, self.inactivity_model, self.sleep_deficiency_model,
                self.feature_scaler, self.clustering_model, self.cluster_scaler
            ])
            
            if all_loaded:
                logger.info("✅ All models loaded successfully from disk")
                return True
            else:
                logger.warning("⚠️ Some models not found. May need retraining.")
                return False
            
        except Exception as e:
            logger.error(f"❌ Error loading models: {e}")
            return False


class AIRecommendationGenerator:
    """
    Generates AI-powered recommendations using ML predictions and clustering
    """
    
    def __init__(self, ai_engine: AIHealthEngine):
        """
        Initialize recommendation generator
        
        Args:
            ai_engine: Initialized AIHealthEngine instance
        """
        self.engine = ai_engine
    
    def generate_ml_driven_recommendations(
        self, 
        user_profile: Dict[str, Any],
        health_risks: Dict[str, Any],
        cluster_info: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """
        Generate recommendations combining ML predictions and cluster personalization
        
        Args:
            user_profile: User's health profile
            health_risks: ML-predicted health risks
            cluster_info: User's cluster assignment
            
        Returns:
            Dictionary with personalized recommendations
        """
        recommendations = {
            'exercise': [],
            'diet': [],
            'sleep': [],
            'hydration': [],
            'health_alerts': []
        }
        
        # Get cluster-based recommendations
        cluster_template = cluster_info.get('template', {})
        cluster_name = cluster_info.get('cluster_name', 'Personalized')
        
        logger.info(f"🎯 Generating AI-driven recommendations for {cluster_name}")
        
        # Exercise recommendations based on inactivity risk
        inactivity_risk = health_risks.get('inactivity_risk', {})
        inactivity_prob = inactivity_risk.get('probability', 0)
        
        if inactivity_prob > 0.7:
            recommendations['exercise'] = [
                "🎯 Critical inactivity detected",
                f"🎯 Your steps are {user_profile.get('average_steps', 0):.0f} - Target 10,000 daily",
                "🎯 Start with 30-minute walks, gradually increase intensity",
                "🎯 Add strength training 2-3x weekly"
            ]
        elif inactivity_prob > 0.4:
            recommendations['exercise'] = [
                f"🎯 Moderate activity needed - Current: {user_profile.get('average_steps', 0):.0f} steps",
                "🎯 Increase to 8,000-10,000 steps daily",
                "🎯 Include 150 mins moderate cardio weekly",
                "🎯 Add flexibility training"
            ]
        else:
            recommendations['exercise'] = [
                f"🎯 Excellent activity level: {user_profile.get('average_steps', 0):.0f} steps",
                "🎯 Maintain current routine",
                "🎯 Consider HIIT or advanced training",
                "🎯 Focus on recovery and form"
            ]
        
        # Diet recommendations based on BMI category + obesity risk
        obesity_risk = health_risks.get('obesity_risk', {})
        obesity_prob = obesity_risk.get('probability', 0)
        bmi = user_profile.get('bmi', 25)
        bmi_category = user_profile.get('bmi_category', 'Normal Weight')
        
        # Check BMI category first for specific guidance
        if bmi_category == "Underweight":
            recommendations['diet'] = [
                f"🥗 Underweight detected - BMI: {bmi:.1f}",
                "🥗 Focus on calorie-dense, nutrient-rich foods",
                "🥗 Include healthy fats (nuts, avocados, olive oil)",
                "🥗 Eat 5-6 smaller meals throughout the day",
                "🥗 Consider consulting a nutritionist for a meal plan"
            ]
        elif obesity_prob > 0.7:
            recommendations['diet'] = [
                "🥗 High obesity risk indicated",
                f"🥗 Your BMI: {bmi:.1f} - Consult nutritionist",
                "🥗 Create 500-700 kcal daily deficit",
                "🥗 Track food intake daily",
                "🥗 Prioritize protein and whole grains"
            ]
        elif obesity_prob > 0.4:
            recommendations['diet'] = [
                f"🥗 Moderate weight management needed - BMI: {bmi:.1f}",
                "🥗 Increase protein intake",
                "🥗 Reduce processed foods and sugary drinks",
                "🥗 Eat balanced meals: 50% veg, 25% protein, 25% carbs"
            ]
        else:
            recommendations['diet'] = [
                f"🥗 Excellent diet balance - BMI: {bmi:.1f}",
                "🥗 Maintain current nutrition habits",
                "🥗 Continue 3 balanced meals daily",
                "🥗 Include 5+ fruit/veg servings daily"
            ]
        
        # Sleep recommendations based on sleep deficiency risk
        sleep_risk = health_risks.get('sleep_deficiency_risk', {})
        sleep_prob = sleep_risk.get('probability', 0)
        avg_sleep = user_profile.get('average_sleep_hours', 7.5)
        
        if sleep_prob > 0.7:
            recommendations['sleep'] = [
                "😴 Sleep deficiency risk detected",
                f"😴 Your sleep: {avg_sleep:.1f}h - Target 7-9 hours",
                "😴 Establish consistent sleep schedule",
                "😴 No screens 30-60 mins before bed",
                "😴 Keep bedroom cool, dark, quiet"
            ]
        elif sleep_prob > 0.4:
            recommendations['sleep'] = [
                f"😴 Optimize sleep - Current: {avg_sleep:.1f}h",
                "😴 Extend to 7-9 hours nightly",
                "😴 Use relaxation techniques",
                "😴 Avoid caffeine after 2 PM"
            ]
        else:
            recommendations['sleep'] = [
                f"😴 Excellent sleep pattern: {avg_sleep:.1f}h",
                "😴 Maintain your sleep routine",
                "😴 Continue monitoring sleep quality",
                "😴 Ensure adequate rest days"
            ]
        
        # Hydration recommendations
        water_intake = user_profile.get('average_water_intake', 2.5)
        
        if water_intake < 1.5:
            recommendations['hydration'] = [
                f"💧 Dehydration risk - Current: {water_intake:.1f}L",
                "💧 Increase to 2.5-3 liters daily",
                "💧 Drink water with every meal",
                "💧 Set hourly reminders"
            ]
        elif water_intake < 2.0:
            recommendations['hydration'] = [
                f"💧 Improve hydration - Current: {water_intake:.1f}L",
                "💧 Target 2.5-3 liters daily",
                "💧 Carry water bottle throughout day"
            ]
        else:
            recommendations['hydration'] = [
                f"💧 Good hydration: {water_intake:.1f}L",
                "💧 Maintain current intake",
                "💧 Increase on exercise days"
            ]
        
        # Health alerts based on ML predictions
        recommendations['health_alerts'] = self._generate_ml_alerts(health_risks, user_profile)
        
        # Add cluster-based personalization message
        priority_recs = cluster_template.get('priority_recommendations', [])
        if priority_recs:
            logger.info(f"👥 Applying CLuster personalization: {priority_recs[0]}")
        
        logger.info(f"✅ AI-driven recommendations generated for {cluster_name}")
        
        return recommendations
    
    def _generate_ml_alerts(self, health_risks: Dict[str, Any], user_profile: Dict) -> List[str]:
        """Generate health alerts based on ML predictions"""
        alerts = []
        
        obesity = health_risks.get('obesity_risk', {})
        inactivity = health_risks.get('inactivity_risk', {})
        sleep = health_risks.get('sleep_deficiency_risk', {})
        bmi_category = user_profile.get('bmi_category', '')
        
        # Check for critical risks
        critical_risks = []
        
        if obesity.get('probability', 0) > 0.8:
            critical_risks.append("Obesity")
        if inactivity.get('probability', 0) > 0.8:
            critical_risks.append("Inactivity")
        if sleep.get('probability', 0) > 0.8:
            critical_risks.append("Sleep Deficiency")
        if bmi_category == "Underweight":
            critical_risks.append("Underweight Status")
        
        if critical_risks:
            alerts.append(f"⚠️ [ML-CRITICAL] High-risk patterns detected: {', '.join(critical_risks)}")
            alerts.append("⚠️ Consider consulting a healthcare professional")
        
        # BMI-related alerts
        if bmi_category == "Underweight":
            alerts.append("⚠️ BMI: Underweight status detected - Focus on nutritious weight gain")
            alerts.append("⚠️ Consult a healthcare provider or nutritionist for guidance")
        
        # Age-related alerts
        age = user_profile.get('age', 0)
        if age >= 50:
            if obesity.get('probability', 0) > 0.6:
                alerts.append("⚠️ Age 50+: Weight management is critical for long-term health")
            if inactivity.get('probability', 0) > 0.6:
                alerts.append("⚠️ Age 50+: Regular exercise prevents age-related decline")
        
        if age >= 65:
            alerts.append("⚠️ Age 65+: Schedule regular preventive health screenings")
            alerts.append("⚠️ Consider balance and falls-prevention exercises")
        
        # Medical conditions alert
        medical = user_profile.get('medical_conditions', '').lower()
        if medical != 'none' and medical.strip():
            alerts.append(f"⚠️ Medical conditions noted: Follow doctor's treatment plan")
        
        if not alerts:
            alerts.append("✅ No major ML-detected health risks. Continue healthy habits!")
        
        return alerts
