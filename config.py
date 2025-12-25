# Configuration settings for the video processing pipeline

# Video source settings
VIDEO_SOURCE = 0  # 0 for webcam, or path to video file like 'video.mp4'

# Motion detection thresholds
MOTION_THRESHOLD = 5000  # Minimum pixel change to detect motion
BLUR_KERNEL_SIZE = (21, 21)  # Gaussian blur kernel size
THRESHOLD_VALUE = 25  # Binary threshold value

# Storage settings
STORAGE_FILE = 'events.json'

# REST API settings
REST_API_URL = 'http://localhost:5000/events'

# Display settings
SHOW_FPS = True
SHOW_MOTION_INDICATOR = True