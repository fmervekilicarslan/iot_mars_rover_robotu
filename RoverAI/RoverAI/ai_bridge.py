import time
import requests
from tahmin_motoru import model_yukle, anomali_kontrol

# =============================
# API ENDPOINTLERİ
# =============================
SENSOR_API = "http://localhost:8080/api/sensor-data"
RESULT_API = "http://localhost:8080/api/ai-result"

POLL_INTERVAL = 2  # saniye

# =============================
# MODEL YÜKLE
# =============================
print("AI Köprü Servisi Başlatılıyor...")
model, scaler = model_yukle()
if not model:
    raise RuntimeError("Model yüklenemedi!")

print("Sistem hazır, sensör verisi bekleniyor...")

# =============================
# ANA DÖNGÜ
# =============================
while True:
    try:
        #Sensör verisini çek
        response = requests.get(SENSOR_API, timeout=5)
        response.raise_for_status()
        data = response.json()

        #last_received kontrolü
        sensor_data = data.get("last_received")

        if sensor_data is None:
            print(" Henüz sensör verisi gelmedi...")
            time.sleep(POLL_INTERVAL)
            continue

        # Modele gönder
        sonuc = anomali_kontrol(
            model,
            scaler,
            sensor_data["voltage"],
            sensor_data["current"],
            sensor_data["sound"],
            sensor_data["gas"],
            sensor_data["temp"],
            sensor_data["hum"],
            sensor_data["heading"]
        )

        # Sonucu hedef endpoint'e yolla
        payload = {
            "durum": sonuc["durum"],
            "mesaj": sonuc["mesaj"],
            "sensorData": sensor_data,
            "serverTime": data.get("server_time")
        }

        post_resp = requests.post(RESULT_API, json=payload, timeout=5)
        post_resp.raise_for_status()

        print(f"📤 AI Sonuç Gönderildi → {sonuc['durum']}")

    except requests.exceptions.RequestException as e:
        print(f"API Hatası: {e}")

    except KeyError as e:
        print(f"Eksik sensör alanı: {e}")

    except Exception as e:
        print(f"Beklenmeyen hata: {e}")

    time.sleep(POLL_INTERVAL)
