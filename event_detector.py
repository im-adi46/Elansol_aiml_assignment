from datetime import datetime
import json

class EventDetector:
    """Handles event creation and formatting"""
    
    def __init__(self):
        self.event_count = 0
    
    def create_event(self, event_type, value):
        """
        Create a structured event dictionary
        
        Args:
            event_type (str): Type of event (e.g., 'motion_detected')
            value (int): Numeric value or metric
            
        Returns:
            dict: Structured event data
        """
        self.event_count += 1
        
        event = {
            "event_id": self.event_count,
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "value": value,
            "metadata": {
                "source": "video_pipeline",
                "version": "1.0"
            }
        }
        
        return event
    
    def format_for_api(self, event):
        """
        Format event for API transmission
        
        Args:
            event (dict): Event dictionary
            
        Returns:
            str: JSON formatted string
        """
        return json.dumps(event, indent=2)