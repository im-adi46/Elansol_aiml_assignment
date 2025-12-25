import cv2
import numpy as np
import time
from datetime import datetime
from event_detector import EventDetector
from data_storage import DataStorage
import requests

class VideoProcessor:
    """Main video processing pipeline"""
    
    def __init__(self, source=0):
        """
        Initialize video processor
        Args:
            source: 0 for webcam, or path to video file
        """
        self.cap = cv2.VideoCapture(source)
        self.previous_frame = None
        self.event_detector = EventDetector()
        self.storage = DataStorage('events.json')
        
        # FPS calculation
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        
    def calculate_fps(self):
        """Calculate current FPS"""
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        
        if elapsed_time > 1:
            self.fps = self.frame_count / elapsed_time
            self.frame_count = 0
            self.start_time = time.time()
            
        return self.fps
    
    def process_frame(self, frame):
        """
        Apply image processing techniques
        Returns: processed frame
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (21, 21), 0)
        
        return blurred
    
    def detect_motion(self, current_frame, previous_frame):
        """
        Detect motion between frames
        Returns: motion detected (bool), motion value (int)
        """
        if previous_frame is None:
            return False, 0
        
        # Compute absolute difference between frames
        frame_diff = cv2.absdiff(previous_frame, current_frame)
        
        # Apply threshold
        thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
        
        # Dilate to fill gaps
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Calculate motion value (number of changed pixels)
        motion_value = np.sum(thresh) / 255
        
        # Detect motion if significant change
        motion_detected = motion_value > 5000
        
        return motion_detected, int(motion_value)
    
    def run(self):
        """Main processing loop"""
        print("Starting video processing... Press 'q' to quit")
        
        try:
            while True:
                # Read frame
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Failed to read frame")
                    break
                
                # Process frame
                processed = self.process_frame(frame)
                
                # Detect motion
                motion_detected, motion_value = self.detect_motion(
                    processed, self.previous_frame
                )
                
                # Update previous frame
                self.previous_frame = processed.copy()
                
                # Handle motion event
                if motion_detected:
                    event = self.event_detector.create_event(
                        event_type="motion_detected",
                        value=motion_value
                    )
                    
                    # Store event
                    requests.post("http://localhost:5000/events", json=event)

                    
                    print(f"Motion detected! Value: {motion_value}")
                
                # Calculate FPS
                fps = self.calculate_fps()
                
                # Display frame with info
                display_frame = frame.copy()
                cv2.putText(display_frame, f"FPS: {fps:.2f}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                if motion_detected:
                    cv2.putText(display_frame, "MOTION DETECTED", (10, 70),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                cv2.imshow('Video Feed', display_frame)
                
                # Quit on 'q' press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Release resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        print("Cleanup complete")

if __name__ == "__main__":
    # Use 0 for webcam or provide video file path
    processor = VideoProcessor(source=0)
    processor.run()