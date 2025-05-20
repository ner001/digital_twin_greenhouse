from flask import Flask, render_template, jsonify
from kafka import KafkaConsumer
import threading
import json

app = Flask(__name__)
events = []
def consume_events():
    consumer = KafkaConsumer(
        'smart-home-events',
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    for msg in consumer:
        events.append(msg.value)
        if len(events) > 100:
            events.pop(0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def get_events():
    return jsonify(events[::-1])

if __name__ == '__main__':
    t = threading.Thread(target=consume_events, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000)
