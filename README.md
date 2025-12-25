# Real-Time Computer Vision Pipeline

A simple Python application that processes video streams, detects motion events, and communicates them in real-time.

## 📋 Features

- **Real-time video processing** from webcam or video file
- **Motion detection** using frame differencing
- **Event generation** with timestamps and metrics
- **Data storage** in JSON format
- **WebSocket communication** for real-time event streaming
- **REST API** alternative for event transmission
- **FPS calculation** and display
- **Modular architecture** for easy maintenance

## 🏗️ Project Structure

```
cv_pipeline/
├── main.py                 # Main video processing pipeline
├── event_detector.py       # Event creation and formatting
├── data_storage.py         # JSON file storage handler
├── websocket_client.py     # WebSocket client for sending events
├── websocket_server.py     # WebSocket server for receiving events
├── rest_api.py            # Flask REST API server
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── events.json           # Storage file (auto-generated)
└── README.md             # This file
```

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd cv_pipeline
```

### 2. Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

For REST API support, also install Flask:
```bash
pip install flask
```

## 🎯 How to Run

### Option 1: Basic Setup (Video Processing + File Storage)

Just run the main application:

```bash
python main.py
```

This will:
- Start video capture from your webcam
- Detect motion events
- Save events to `events.json`
- Display FPS and motion indicators

Press **'q'** to quit.

### Option 2: With WebSocket Server

**Terminal 1** - Start WebSocket server:
```bash
python websocket_server.py
```

**Terminal 2** - Run main application:
```bash
python main.py
```

### Option 3: With REST API

**Terminal 1** - Start REST API server:
```bash
python rest_api.py
```

**Terminal 2** - Run main application (modify to use REST):
```bash
python main.py
```

## 🔧 Configuration

Edit `config.py` to customize:

- **VIDEO_SOURCE**: `0` for webcam, or `'path/to/video.mp4'` for video file
- **MOTION_THRESHOLD**: Sensitivity of motion detection (lower = more sensitive)
- **STORAGE_FILE**: Path to JSON storage file

## 📊 How It Works

### 1. Video Input & Processing
- Captures frames from webcam or video file using OpenCV
- Converts frames to grayscale
- Applies Gaussian blur to reduce noise

### 2. Motion Detection
- Compares consecutive frames using absolute difference
- Applies binary threshold to identify changed regions
- Calculates motion value (number of changed pixels)
- Triggers event if motion exceeds threshold

### 3. Event Generation
Each event contains:
```json
{
  "event_id": 1,
  "timestamp": "2025-12-24T10:30:45.123456",
  "event_type": "motion_detected",
  "value": 15430,
  "metadata": {
    "source": "video_pipeline",
    "version": "1.0"
  }
}
```

### 4. Data Storage
- Events stored in `events.json` file
- Structured format for easy querying
- Persistent across application runs

### 5. Real-Time Communication
- **WebSocket**: Low-latency, bidirectional communication
- **REST API**: Standard HTTP POST for event submission

## 📈 Event Data Structure

### Stored Format (JSON)
```json
{
  "events": [
    {
      "event_id": 1,
      "timestamp": "2025-12-24T10:30:45.123456",
      "event_type": "motion_detected",
      "value": 15430,
      "metadata": {
        "source": "video_pipeline",
        "version": "1.0"
      }
    }
  ]
}
```

## 🧪 Testing

### Test Motion Detection
1. Run the application
2. Move in front of the camera
3. Check console for "Motion detected!" messages
4. Verify events in `events.json`

### Test WebSocket Communication
1. Start `websocket_server.py`
2. Run `main.py`
3. Check server console for received events

### Test REST API
1. Start `rest_api.py`
2. Access `http://localhost:5000/events` to view stored events
3. Use Postman or curl to test endpoints

## 🔍 API Endpoints (REST)

### POST /events
Submit a new event
```bash
curl -X POST http://localhost:5000/events \
  -H "Content-Type: application/json" \
  -d '{"event_type":"test","value":100,"timestamp":"2025-12-24T10:00:00"}'
```

### GET /events
Retrieve all events
```bash
curl http://localhost:5000/events
```

### GET /events/{event_type}
Get events by type
```bash
curl http://localhost:5000/events/motion_detected
```

## 💡 Design Decisions & Assumptions

### Assumptions
1. **Webcam access**: Assumes camera is available at index 0
2. **Motion threshold**: Default value works for typical indoor scenarios
3. **Storage**: JSON file sufficient for moderate event volumes
4. **Processing**: Single-threaded processing adequate for webcam resolution

### Design Choices
1. **Frame differencing**: Simple, fast motion detection algorithm
2. **JSON storage**: Human-readable, easy to parse, good for prototyping
3. **Modular design**: Separate modules for detection, storage, communication
4. **Graceful degradation**: Works without WebSocket/REST server running

### Technical Approach
- **OpenCV**: Industry-standard for computer vision tasks
- **Frame differencing**: Lightweight motion detection without ML models
- **Gaussian blur**: Reduces false positives from sensor noise
- **Binary threshold**: Clear motion/no-motion decision boundary

## 🚀 Possible Improvements

### Performance
- [ ] Multi-threading for frame capture and processing
- [ ] Async I/O for WebSocket and file operations
- [ ] Frame buffer for smoother processing
- [ ] GPU acceleration for image processing

### Features
- [ ] Object detection using YOLO or MobileNet
- [ ] Multi-zone motion detection
- [ ] Event filtering and aggregation
- [ ] Database integration (PostgreSQL, SQLite)
- [ ] Video recording on event trigger
- [ ] Email/SMS notifications
- [ ] Web dashboard for visualization

### Architecture
- [ ] Kafka integration for event streaming
- [ ] Docker containerization
- [ ] Configuration file support
- [ ] Logging framework
- [ ] Unit and integration tests
- [ ] CI/CD pipeline

### Computer Vision
- [ ] Background subtraction algorithms
- [ ] Optical flow for motion tracking
- [ ] People counting
- [ ] Face detection/recognition
- [ ] Activity recognition

## 🐛 Troubleshooting

### Camera not found
```
Error: Failed to open camera
Solution: Check camera index in config.py, try values 0, 1, 2
```

### Low FPS
```
Solution: Reduce frame resolution, optimize blur kernel size
```

### No motion detected
```
Solution: Lower MOTION_THRESHOLD in config.py
```

### WebSocket connection failed
```
Solution: Ensure websocket_server.py is running first
```

## 📦 Dependencies

- **opencv-python**: Video capture and image processing
- **numpy**: Numerical operations on frames
- **websockets**: WebSocket client/server
- **flask**: REST API (optional)
- **aiohttp**: Async HTTP client (optional)

## 📝 License

MIT License - Feel free to use for learning and projects

## 👤 Author

Created as an intern assignment demonstrating:
- Python fundamentals
- Computer vision concepts
- Real-time processing
- Backend integration
- Clean code practices

## 🙏 Acknowledgments

- OpenCV community for excellent documentation
- Python asyncio for WebSocket examples
- Flask team for simple REST API framework
