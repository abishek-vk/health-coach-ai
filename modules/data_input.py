"""
data_input.py - Data input and collection module
Handles user health data collection with validation
"""

from typing import Dict, Optional, Tuple
from modules.validators import HealthDataValidator


class HealthDataCollector:
    """Collects and validates health data from users"""
    
    def __init__(self):
        """Initialize the data collector"""
        self.validator = HealthDataValidator()
    
    def collect_userinfo(self, age: int, gender: str, height: float, weight: float, 
                        medical_conditions: str) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Collect basic user information
        
        Args:
            age: User age in years
            gender: User gender
            height: User height in cm
            weight: User weight in kg
            medical_conditions: Any medical conditions (comma-separated)
            
        Returns:
            Tuple of (is_valid, error_message, data)
        """
        # Validate all inputs
        is_valid, error = self.validator.validate_age(age)
        if not is_valid:
            return False, error, None
        
        is_valid, error = self.validator.validate_gender(gender)
        if not is_valid:
            return False, error, None
        
        is_valid, error = self.validator.validate_height(height)
        if not is_valid:
            return False, error, None
        
        is_valid, error = self.validator.validate_weight(weight)
        if not is_valid:
            return False, error, None
        
        is_valid, error = self.validator.validate_medical_conditions(medical_conditions)
        if not is_valid:
            return False, error, None
        
        # Prepare data
        user_info = {
            "age": int(age),
            "gender": gender,
            "height_cm": float(height),
            "weight_kg": float(weight),
            "medical_conditions": medical_conditions if medical_conditions.strip() else "None"
        }
        
        return True, None, user_info
    
    def collect_daily_metrics(self, daily_steps: int, sleep_hours: float, 
                             water_intake: float) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Collect daily health metrics
        
        Args:
            daily_steps: Number of steps taken today
            sleep_hours: Hours of sleep last night
            water_intake: Water intake in liters
            
        Returns:
            Tuple of (is_valid, error_message, data)
        """
        # Validate inputs
        is_valid, error = self.validator.validate_steps(daily_steps)
        if not is_valid:
            return False, error, None
        
        is_valid, error = self.validator.validate_sleep_hours(sleep_hours)
        if not is_valid:
            return False, error, None
        
        is_valid, error = self.validator.validate_water_intake(water_intake)
        if not is_valid:
            return False, error, None
        
        # Prepare data
        daily_metrics = {
            "daily_steps": int(daily_steps),
            "sleep_hours": float(sleep_hours),
            "water_intake_liters": float(water_intake)
        }
        
        return True, None, daily_metrics
    
    def create_health_record(self, user_info: Dict, daily_metrics: Dict) -> Dict:
        """
        Create a complete health record combining user info and daily metrics
        
        Args:
            user_info: User information dictionary
            daily_metrics: Daily metrics dictionary
            
        Returns:
            Complete health record dictionary
        """
        health_record = {**user_info, **daily_metrics}
        return health_record
