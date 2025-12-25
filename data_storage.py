import json
import os
from datetime import datetime

class DataStorage:
    """Handles event data storage to JSON file"""
    
    def __init__(self, filename='events.json'):
        """
        Initialize storage
        
        Args:
            filename (str): Path to JSON storage file
        """
        self.filename = filename
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Create or fix storage file if missing or empty"""
        if (not os.path.exists(self.filename)) or os.stat(self.filename).st_size == 0:
            with open(self.filename, 'w') as f:
                json.dump({"events": []}, f, indent=2)

    
    def save_event(self, event):
        """
        Save event to storage
        
        Args:
            event (dict): Event data to save
        """
        try:
            # Read existing data
            with open(self.filename, 'r') as f:
                data = json.load(f)
            
            # Append new event
            data['events'].append(event)
            
            # Write back to file with explicit flush
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
                f.flush()  # Ensure data is written to disk
                
            print(f"✓ Event saved to {self.filename}: {event['event_type']} at {event['timestamp']}")
            return True
            
        except Exception as e:
            print(f"✗ Error saving event: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_all_events(self):
        """
        Retrieve all stored events
        
        Returns:
            list: All events
        """
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return data['events']
        except Exception as e:
            print(f"Error reading events: {e}")
            return []
    
    def get_events_by_type(self, event_type):
        """
        Filter events by type
        
        Args:
            event_type (str): Type of event to filter
            
        Returns:
            list: Filtered events
        """
        all_events = self.get_all_events()
        return [e for e in all_events if e['event_type'] == event_type]
    
    def clear_storage(self):
        """Clear all stored events"""
        with open(self.filename, 'w') as f:
            json.dump({"events": []}, f, indent=2)
        print("Storage cleared")