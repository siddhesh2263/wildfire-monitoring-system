from locust import HttpUser, task, between
import random
import datetime

class APIGatewayUser(HttpUser):
    wait_time = between(0.01, 0.1)  # 10–100ms between requests

    @task
    def send_data(self):
        payload = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "latitude": round(random.uniform(31.0, 32.0), 6),
            "longitude": round(random.uniform(-111.0, -110.0), 6),
            "temperature": round(random.uniform(25, 45), 2),
            "humidity": random.randint(10, 90),
            "wind_speed": round(random.uniform(5, 30), 1),
            "wind_direction": random.choice([0, 90, 180, 270]),
            "vegetation_density": round(random.uniform(0.1, 1.0), 2),
            "air_quality_index": random.randint(20, 200),
            "source_name": "locust-simulator"
        }

        self.client.post("/ingest", json=payload)