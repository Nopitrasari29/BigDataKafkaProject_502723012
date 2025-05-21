# kafka_producers/suhu_producer.py
import time
import json
import random
from kafka import KafkaProducer

# Konfigurasi Kafka
KAFKA_BROKER = 'localhost:9092'
TOPIC_SUHU = 'sensor-suhu-gudang'
GUDANG_IDS = ['G1', 'G2', 'G3', 'G4'] # Minimal 3 gudang

# Inisialisasi Kafka Producer
# Pastikan value_serializer mengubah dict menjadi bytes JSON
try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print(f"Memulai Suhu Producer untuk topik: {TOPIC_SUHU} ke broker: {KAFKA_BROKER}...")
except Exception as e:
    print(f"Error initializing Kafka Producer: {e}")
    exit()


try:
    while True:
        gudang_id = random.choice(GUDANG_IDS)
        # Suhu antara 70-95 untuk memungkinkan kondisi > 80
        suhu = round(random.uniform(70.0, 95.0), 1) 
        
        message = {
            "gudang_id": gudang_id,
            "suhu": suhu
        }
        
        # Mengirim pesan ke topik Kafka
        producer.send(TOPIC_SUHU, value=message)
        print(f"Sent Suhu: {message}")
        
        # Kirim data setiap detik (atau interval acak kecil)
        time.sleep(random.uniform(0.8, 1.2)) 
except KeyboardInterrupt:
    print("Suhu Producer dihentikan.")
except Exception as e:
    print(f"Error during producing: {e}")
finally:
    if 'producer' in locals() and producer:
        producer.flush() # Pastikan semua pesan terkirim
        producer.close()
        print("Suhu Producer ditutup.")