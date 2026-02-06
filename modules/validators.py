"""
validators.py - Input validation module
Validates health data inputs and ensures data integrity
"""

import re
from datetime import datetime
from typing import Tuple, Optional


class HealthDataValidator:
    """Validates user health input data with specific rules and constraints"""
    
    @staticmethod
    def validate_age(age: int) -> Tuple[bool, Optional[str]]:
        """
        Validate age input
        
        Args:
            age: Age in years
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(age, (int, float)):
            return False, "Age must be a number"
        
        age = int(age)
        if age < 1 or age > 150:
            return False, "Age must be between 1 and 150"
        
        return True, None
    
    @staticmethod
    def validate_gender(gender: str) -> Tuple[bool, Optional[str]]:
        """Validate gender input"""
        valid_genders = ["Male", "Female", "Other"]
        if gender not in valid_genders:
            return False, f"Gender must be one of: {', '.join(valid_genders)}"
        return True, None
    
    @staticmethod
    def validate_height(height: float) -> Tuple[bool, Optional[str]]:
        """
        Validate height in cm
        
        Args:
            height: Height in centimeters
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            height = float(height)
        except:
            return False, "Height must be a valid number"
        
        if height < 30 or height > 300:
            return False, "Height must be between 30 and 300 cm"
        
        return True, None
    
    @staticmethod
    def validate_weight(weight: float) -> Tuple[bool, Optional[str]]:
        """Validate weight in kg"""
        try:
            weight = float(weight)
        except:
            return False, "Weight must be a valid number"
        
        if weight < 1 or weight > 300:
            return False, "Weight must be between 1 and 300 kg"
        
        return True, None
    
    @staticmethod
    def validate_medical_conditions(conditions: str) -> Tuple[bool, Optional[str]]:
        """Validate medical conditions input"""
        if not isinstance(conditions, str):
            return False, "Medical conditions must be text"
        
        if len(conditions) > 500:
            return False, "Medical conditions text is too long (max 500 characters)"
        
        return True, None
    
    @staticmethod
    def validate_steps(steps: int) -> Tuple[bool, Optional[str]]:
        """Validate daily steps"""
        try:
            steps = int(steps)
        except:
            return False, "Steps must be a whole number"
        
        if steps < 0 or steps > 100000:
            return False, "Steps must be between 0 and 100,000"
        
        return True, None
    
    @staticmethod
    def validate_sleep_hours(sleep: float) -> Tuple[bool, Optional[str]]:
        """Validate sleep hours (0-24)"""
        try:
            sleep = float(sleep)
        except:
            return False, "Sleep hours must be a valid number"
        
        if sleep < 0 or sleep > 24:
            return False, "Sleep hours must be between 0 and 24"
        
        return True, None
    
    @staticmethod
    def validate_water_intake(water: float) -> Tuple[bool, Optional[str]]:
        """Validate water intake in liters"""
        try:
            water = float(water)
        except:
            return False, "Water intake must be a valid number"
        
        if water < 0 or water > 20:
            return False, "Water intake must be between 0 and 20 liters"
        
        return True, None
    
    @staticmethod
    def validate_all_data(age, gender, height, weight, medical_conditions, steps, sleep, water) -> Tuple[bool, Optional[str]]:
        """
        Validate all health data together
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        validators = [
            (age, HealthDataValidator.validate_age),
            (gender, HealthDataValidator.validate_gender),
            (height, HealthDataValidator.validate_height),
            (weight, HealthDataValidator.validate_weight),
            (medical_conditions, HealthDataValidator.validate_medical_conditions),
            (steps, HealthDataValidator.validate_steps),
            (sleep, HealthDataValidator.validate_sleep_hours),
            (water, HealthDataValidator.validate_water_intake),
        ]
        
        for value, validator_func in validators:
            is_valid, error_msg = validator_func(value)
            if not is_valid:
                return False, error_msg
        
        return True, None
