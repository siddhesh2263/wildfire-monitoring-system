import os
import json
import psycopg2
from kafka import KafkaConsumer
from psycopg2.extras import execute_values

# Read DB creds from env (Kubernetes secret)
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka-service:9092")
TOPIC_NAME = "raw-data"

# PostgreSQL connection
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Kafka Consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="db-writer-group"
)

print("DB Writer started, consuming from Kafka...")

for message in consumer:
    data = message.value
    try:
        cursor.execute("""
            INSERT INTO raw_data (
                timestamp, latitude, longitude, temperature, humidity,
                wind_speed, wind_direction, vegetation_density,
                air_quality_index, source_name
            ) VALUES (
                %(timestamp)s, %(latitude)s, %(longitude)s, %(temperature)s, %(humidity)s,
                %(wind_speed)s, %(wind_direction)s, %(vegetation_density)s,
                %(air_quality_index)s, %(source_name)s
            );
        """, data)
        conn.commit()
        print(f"Inserted: {data}")
    except Exception as e:
        conn.rollback()
        print(f"Insert error: {e}")