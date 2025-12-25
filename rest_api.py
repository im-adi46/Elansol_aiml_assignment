from flask import Flask, request, jsonify
from datetime import datetime
import json
from data_storage import DataStorage

storage = DataStorage("events.json")


app = Flask(__name__)

# Store events in memory
events_storage = []

@app.route('/events', methods=['POST'])
def receive_event():
    try:
        event = request.get_json()
        event['server_received_at'] = datetime.now().isoformat()
        events_storage.append(event)
        storage.save_event(event)  # <-- save to file
        print(f"\n=== Event Received via REST ===")
        print(f"Type: {event['event_type']}")
        print(f"Value: {event['value']}")
        print(f"Time: {event['timestamp']}")
        print("==============================\n")
        return jsonify({
            "status": "success",
            "message": "Event received",
            "event_id": event.get('event_id')
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


@app.route('/events', methods=['GET'])
def get_events():
    """Endpoint to retrieve all events"""
    return jsonify({
        "total_events": len(events_storage),
        "events": events_storage
    }), 200

@app.route('/events/<event_type>', methods=['GET'])
def get_events_by_type(event_type):
    """Endpoint to retrieve events by type"""
    filtered = [e for e in events_storage if e['event_type'] == event_type]
    
    return jsonify({
        "event_type": event_type,
        "count": len(filtered),
        "events": filtered
    }), 200

if __name__ == '__main__':
    print("Starting REST API server on http://localhost:5000")
    app.run(debug=True, port=5000)