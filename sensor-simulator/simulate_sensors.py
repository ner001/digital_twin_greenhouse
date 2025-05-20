import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

ROOMS = ['living_room', 'bedroom', 'kitchen', 'garage']
ARMED = True  # Simulate home security system armed

def is_night():
    hour = datetime.now().hour
    return hour < 6 or hour > 22

while True:
    room = random.choice(ROOMS)
    data = {
        "sensor_id": room,
        "temperature": round(random.uniform(16, 32), 2),
        "humidity": round(random.uniform(25, 80), 2),
        "motion": random.choices([True, False], weights=[0.2, 0.8])[0],
        "door": random.choices([True, False], weights=[0.1, 0.9])[0] if room == "garage" else None,
        "armed": ARMED,
        "night": is_night(),
        "timestamp": int(time.time())
    }
    producer.send('smart-home-sensors', data)
    print(f"Sent: {data}")
    time.sleep(random.uniform(1, 3))
