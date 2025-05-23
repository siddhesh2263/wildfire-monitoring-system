import os
import json
from kafka import KafkaConsumer, KafkaProducer

# Kafka config
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka-service:9092")
RAW_TOPIC = "raw-data"
ANOMALY_TOPIC = "anomaly-data"

# Kafka setup
consumer = KafkaConsumer(
    RAW_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="anomaly-detector-group"
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Anomaly Detection Service is running...")

def classify_intensity(data):
    temp = data.get("temperature", 0)
    humidity = data.get("humidity", 100)
    wind_speed = data.get("wind_speed", 0)
    vegetation = data.get("vegetation_density", 0)
    aqi = data.get("air_quality_index", 0)

    if (
        temp > 40 or
        humidity < 20 or
        wind_speed > 20 or
        vegetation > 0.7 or
        aqi > 150
    ):
        return "high", 0.95
    elif (
        temp > 35 or
        humidity < 30 or
        wind_speed > 15 or
        vegetation > 0.5 or
        aqi > 100
    ):
        return "medium", 0.75
    else:
        return "low", 0.45

for message in consumer:
    data = message.value
    try:
        intensity, score = classify_intensity(data)
        data["intensity"] = intensity
        data["confidence_score"] = round(score, 2)

        producer.send(ANOMALY_TOPIC, value=data)
        producer.flush()

        print(f"Classified {intensity.upper()} | Lat: {data['latitude']} Lon: {data['longitude']}")
    except Exception as e:
        print(f"Error: {e}")