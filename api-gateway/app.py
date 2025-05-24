# from flask import Flask, request, jsonify
# from kafka import KafkaProducer
# import json
# import os

# # Configuration
# KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka-service:9092")
# TOPIC_NAME = "raw-data"

# app = Flask(__name__)

# # Initialize Kafka producer
# producer = KafkaProducer(
#     bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# @app.route('/ingest', methods=['POST'])
# def ingest():
#     if not request.is_json:
#         return jsonify({"error": "Expected JSON"}), 400

#     data = request.get_json()

#     required_fields = [
#         "timestamp", "latitude", "longitude", "temperature", "humidity",
#         "wind_speed", "wind_direction", "vegetation_density",
#         "air_quality_index", "source_name"
#     ]
#     missing = [f for f in required_fields if f not in data]
#     if missing:
#         return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

#     try:
#         producer.send(TOPIC_NAME, value=data)
#         producer.flush()
#         return jsonify({"status": "Data sent to Kafka", "topic": TOPIC_NAME}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/')
# def health():
#     return jsonify({"status": "API Gateway is running"}), 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)



from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
import os

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka-service:9092")
TOPIC_NAME = "raw-data"

app = Flask(__name__)

# Initialize Kafka producer with batching
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    linger_ms=5,         # buffer up to 5 ms
    batch_size=32768,    # larger batches for better throughput
    acks='1'             # wait for leader acknowledgment only
)

@app.route('/ingest', methods=['POST'])
def ingest():
    if not request.is_json:
        return jsonify({"error": "Expected JSON"}), 400

    data = request.get_json()

    required_fields = [
        "timestamp", "latitude", "longitude", "temperature", "humidity",
        "wind_speed", "wind_direction", "vegetation_density",
        "air_quality_index", "source_name"
    ]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        producer.send(TOPIC_NAME, value=data)
        # Removed synchronous flush for lower latency
        return jsonify({"status": "Data sent to Kafka", "topic": TOPIC_NAME}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def health():
    return jsonify({"status": "API Gateway is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)