"""
file_storage.py - JSON file storage module
Handles reading/writing health records to JSON files with proper serialization
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JSONHealthStorage:
    """Manages storage of health records in JSON files"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize storage handler
        
        Args:
            data_dir: Directory to store JSON files
        """
        self.data_dir = data_dir
        self.user_records_file = os.path.join(data_dir, "user_records.json")
        self.user_profiles_file = os.path.join(data_dir, "user_profiles.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize files if they don't exist
        self._initialize_files()
    
    def _initialize_files(self):
        """Create JSON files with initial empty structures if they don't exist"""
        # Initialize user records file
        if not os.path.exists(self.user_records_file):
            with open(self.user_records_file, 'w') as f:
                json.dump({"records": []}, f, indent=2)
            logger.info(f"Created {self.user_records_file}")
        
        # Initialize user profiles file
        if not os.path.exists(self.user_profiles_file):
            with open(self.user_profiles_file, 'w') as f:
                json.dump({"profiles": []}, f, indent=2)
            logger.info(f"Created {self.user_profiles_file}")
    
    def add_health_record(self, user_id: str, health_data: Dict[str, Any]) -> bool:
        """
        Add a new health record for a user
        
        Args:
            user_id: Unique user identifier
            health_data: Dictionary containing health metrics
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read existing records
            with open(self.user_records_file, 'r') as f:
                data = json.load(f)
            
            # Create new record with timestamp
            new_record = {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "data": health_data
            }
            
            # Add to records
            data["records"].append(new_record)
            
            # Write back to file
            with open(self.user_records_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Added health record for user {user_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error adding health record: {str(e)}")
            return False
    
    def get_user_records(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all health records for a specific user
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            List of health records for the user
        """
        try:
            with open(self.user_records_file, 'r') as f:
                data = json.load(f)
            
            user_records = [
                record for record in data["records"] 
                if record["user_id"] == user_id
            ]
            
            return user_records
        
        except Exception as e:
            logger.error(f"Error retrieving user records: {str(e)}")
            return []
    
    def get_all_records(self) -> List[Dict[str, Any]]:
        """Get all health records across all users"""
        try:
            with open(self.user_records_file, 'r') as f:
                data = json.load(f)
            return data["records"]
        
        except Exception as e:
            logger.error(f"Error retrieving all records: {str(e)}")
            return []
    
    def save_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """
        Save compressed health profile for a user
        
        Args:
            user_id: Unique user identifier
            profile_data: Compressed profile dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read existing profiles
            with open(self.user_profiles_file, 'r') as f:
                data = json.load(f)
            
            # Update or add profile
            profile_exists = False
            for i, profile in enumerate(data["profiles"]):
                if profile["user_id"] == user_id:
                    profile["data"] = profile_data
                    profile["last_updated"] = datetime.now().isoformat()
                    profile_exists = True
                    break
            
            if not profile_exists:
                new_profile = {
                    "user_id": user_id,
                    "data": profile_data,
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                }
                data["profiles"].append(new_profile)
            
            # Write back to file
            with open(self.user_profiles_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved profile for user {user_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error saving profile: {str(e)}")
            return False
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve compressed health profile for a user
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            Profile data if exists, None otherwise
        """
        try:
            with open(self.user_profiles_file, 'r') as f:
                data = json.load(f)
            
            for profile in data["profiles"]:
                if profile["user_id"] == user_id:
                    return profile["data"]
            
            return None
        
        except Exception as e:
            logger.error(f"Error retrieving profile: {str(e)}")
            return None
    
    def delete_user_data(self, user_id: str) -> bool:
        """
        Delete all data for a specific user
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Delete records
            with open(self.user_records_file, 'r') as f:
                records_data = json.load(f)
            
            records_data["records"] = [
                record for record in records_data["records"]
                if record["user_id"] != user_id
            ]
            
            with open(self.user_records_file, 'w') as f:
                json.dump(records_data, f, indent=2)
            
            # Delete profile
            with open(self.user_profiles_file, 'r') as f:
                profiles_data = json.load(f)
            
            profiles_data["profiles"] = [
                profile for profile in profiles_data["profiles"]
                if profile["user_id"] != user_id
            ]
            
            with open(self.user_profiles_file, 'w') as f:
                json.dump(profiles_data, f, indent=2)
            
            logger.info(f"Deleted all data for user {user_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting user data: {str(e)}")
            return False
