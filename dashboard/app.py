from flask import Flask, render_template, jsonify, request, redirect, url_for
from kafka import KafkaConsumer
import threading
import json
import time
from datetime import datetime
import logging
from collections import deque
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app with static folder configuration
app = Flask(__name__, 
    static_url_path='/static',
    static_folder='static',
    template_folder='templates'
)

# Use a deque for better performance with a fixed size collection
events = deque(maxlen=100)
sensor_data = {}
alerts = deque(maxlen=20)

# Status flags
kafka_connected = False
last_event_time = None

def consume_events():
    """Consume events from Kafka and store them in memory"""
    global kafka_connected, last_event_time
    
    # Retry connection if Kafka isn't immediately available
    retry_count = 0
    max_retries = 5
    
    while retry_count < max_retries:
        try:
            logger.info("Attempting to connect to Kafka...")
            consumer = KafkaConsumer(
                'smart-home-events',
                bootstrap_servers='kafka:9092',
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest',
                consumer_timeout_ms=5000,
                group_id='dashboard-consumer-group'
            )
            kafka_connected = True
            logger.info("Successfully connected to Kafka")
            break
        except Exception as e:
            retry_count += 1
            wait_time = retry_count * 5
            logger.error(f"Failed to connect to Kafka: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    if not kafka_connected:
        logger.error("Failed to connect to Kafka after multiple attempts")
        return
    
    # Process messages from Kafka
    try:
        for msg in consumer:
            data = msg.value
            process_event(data)
            last_event_time = datetime.now()
    except Exception as e:
        logger.error(f"Error consuming Kafka messages: {e}")
        kafka_connected = False

def process_event(data):
    """Process and categorize incoming event data"""
    events.appendleft(data)
    
    # Store latest data by sensor ID for quick access
    if 'sensor_id' in data:
        sensor_id = data['sensor_id']
        
        # Format the timestamp for display
        if 'timestamp' in data:
            data['formatted_time'] = datetime.fromtimestamp(data['timestamp']).strftime('%H:%M:%S %d-%m-%Y')
        
        # Store the updated sensor data
        sensor_data[sensor_id] = data
        
        # Check for anomalies
        check_anomalies(data)

def check_anomalies(data):
    """Check for anomalies in the data and create alerts"""
    sensor_id = data.get('sensor_id', 'unknown')
    
    # Temperature anomalies
    if 'temperature' in data:
        temp = data['temperature']
        if temp > 30:
            create_alert(f"High temperature alert: {temp}°C in {sensor_id}")
        elif temp < 10:
            create_alert(f"Low temperature alert: {temp}°C in {sensor_id}")
    
    # Humidity anomalies
    if 'humidity' in data:
        humidity = data['humidity']
        if humidity > 80:
            create_alert(f"High humidity alert: {humidity}% in {sensor_id}")
        elif humidity < 20:
            create_alert(f"Low humidity alert: {humidity}% in {sensor_id}")
    
    # Motion detection during armed state
    if data.get('motion', False) and data.get('armed', False):
        create_alert(f"Motion detected while system armed in {sensor_id}")
    
    # Door left open during night
    if data.get('door') == "open" and data.get('night', False):
        create_alert(f"Door left open during night in {sensor_id}")

def create_alert(message):
    """Create a new alert with timestamp"""
    alert = {
        'message': message,
        'timestamp': datetime.now().strftime('%H:%M:%S %d-%m-%Y'),
        'id': int(time.time() * 1000)
    }
    alerts.appendleft(alert)
    logger.warning(f"Alert created: {message}")

@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template('index.html', 
                          kafka_connected=kafka_connected,
                          last_update=last_event_time)

@app.route('/events')
def get_events():
    """Return recent events as JSON"""
    limit = request.args.get('limit', default=20, type=int)
    return jsonify(list(events)[:limit])

@app.route('/sensors')
def get_sensors():
    """Return current sensor states"""
    return jsonify(sensor_data)

@app.route('/alerts')
def get_alerts():
    """Return recent alerts"""
    return jsonify(list(alerts))

@app.route('/health')
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'ok' if kafka_connected else 'degraded',
        'kafka_connected': kafka_connected,
        'last_event_time': last_event_time.isoformat() if last_event_time else None,
        'event_count': len(events),
        'sensor_count': len(sensor_data),
        'alert_count': len(alerts)
    }
    return jsonify(status)

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    logger.error(f"Server error: {e}")
    return render_template('500.html'), 500

def start_background_threads():
    """Start all background threads"""
    # Kafka consumer thread
    kafka_thread = threading.Thread(target=consume_events, daemon=True)
    kafka_thread.start()
    logger.info("Background thread started for Kafka consumer")

if __name__ == '__main__':
    # Start background processes
    start_background_threads()
    
    # Determine if in development or production
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    # Start the Flask application
    logger.info(f"Starting Flask application on port 5000 (debug={debug_mode})")
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
