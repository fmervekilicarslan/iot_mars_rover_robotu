import joblib
import pandas as pd
from tahmin_motoru import model_yukle, anomali_kontrol

print("--- ROBOT TEŞHİS SİSTEMİ BAŞLATILIYOR ---")
model, scaler = model_yukle()

if not model: exit()

while True:
    print("\n" + "="*50)
    print("📝 YENİ SENSÖR VERİSİ GİRİŞİ")
    print("="*50)
    try:
        v_volt = float(input("Voltage (V)   [Normal: 5.0] : ") or 5.0)
        v_curr = float(input("Current (A)   [Normal: 13.5]: ") or 13.5)
        v_sound= float(input("Sound         [Normal: 1020]: ") or 1020)
        v_gas  = float(input("Gas           [Normal: 1023]: ") or 1023)
        v_temp = float(input("Temp (°C)     [Normal: 23.0]: ") or 23.0)
        v_hum  = float(input("Hum (%)       [Normal: 57]  : ") or 57)
        v_head = float(input("Heading (°)   [Normal: 230] : ") or 230)
        
        sonuc = anomali_kontrol(model, scaler, v_volt, v_curr, v_sound, v_gas, v_temp, v_hum, v_head)
        
        print("\n" + "-"*50)
        if sonuc["durum"] == "NORMAL":
            print(f"✅ SONUÇ: {sonuc['durum']}")
            print(f"ℹ️  Bilgi: {sonuc['mesaj']}")
        else:
            print(f"❌ SONUÇ: {sonuc['durum']} TESPİT EDİLDİ!")
            print("🚨 DETAYLI ARIZA RAPORU:")
            print(sonuc['mesaj'])  # Alt alta buraya basacak
        print("-"*50)
            
    except ValueError:
        print("Lütfen sayı girin!")
    except KeyboardInterrupt:
        break