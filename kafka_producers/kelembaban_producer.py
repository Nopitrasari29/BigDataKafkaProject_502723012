# kafka_producers/kelembaban_producer.py
import time
import json
import random
from kafka import KafkaProducer

# Konfigurasi Kafka
KAFKA_BROKER = 'localhost:9092'
TOPIC_KELEMBABAN = 'sensor-kelembaban-gudang'
GUDANG_IDS = ['G1', 'G2', 'G3', 'G4'] # Minimal 3 gudang

# Inisialisasi Kafka Producer
try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print(f"Memulai Kelembaban Producer untuk topik: {TOPIC_KELEMBABAN} ke broker: {KAFKA_BROKER}...")
except Exception as e:
    print(f"Error initializing Kafka Producer: {e}")
    exit()

try:
    while True:
        gudang_id = random.choice(GUDANG_IDS)
        # Kelembaban antara 60-85 untuk memungkinkan kondisi > 70
        kelembaban = round(random.uniform(60.0, 85.0), 1) 
        
        message = {
            "gudang_id": gudang_id,
            "kelembaban": kelembaban
        }
        
        producer.send(TOPIC_KELEMBABAN, value=message)
        print(f"Sent Kelembaban: {message}")
        
        time.sleep(random.uniform(0.8, 1.2)) 
except KeyboardInterrupt:
    print("Kelembaban Producer dihentikan.")
except Exception as e:
    print(f"Error during producing: {e}")
finally:
    if 'producer' in locals() and producer:
        producer.flush()
        producer.close()
        print("Kelembaban Producer ditutup.")