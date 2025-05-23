from flask import Flask, render_template, jsonify
from kafka import KafkaConsumer
from collections import deque
import os
import json
import threading

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka-service:9092")
TOPIC_NAME = "anomaly-data"

# Flask setup
app = Flask(__name__)

# Circular buffer to store the latest messages
buffer = deque(maxlen=1000)

# Background Kafka consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='ui-service-group'
)

def consume_kafka():
    for message in consumer:
        buffer.append(message.value)

# Routes
@app.route("/")
def serve_map():
    return render_template("map.html")

@app.route("/data")
def get_data():
    return jsonify(list(buffer))

if __name__ == "__main__":
    threading.Thread(target=consume_kafka, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)