import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

# ==========================================
# AYARLAR: HASSASİYET PARAMETRELERİ
# ==========================================
DEFAULT_SIGMA = 4    # Diğer sensörler için Standart Sapma Çarpanı
TEMP_SIGMA = 15      # Sıcaklık sensörü için Genişletilmiş Çarpan

# Modelin anomali hassasiyeti (%5)
CONTAMINATION_RATE = 0.05 

print("[BİLGİ] Veri seti yükleniyor ve ön işleme yapılıyor...")

try:
    df_raw = pd.read_csv('sensor_data.csv', header=None, na_values=['\\N'])
    df_real = df_raw[[2, 3, 4, 5, 6, 7, 8]].copy()
    df_real.columns = ['voltage', 'current', 'sound', 'gas', 'temp', 'hum', 'heading']
    df_real = df_real.apply(pd.to_numeric, errors='coerce')
    df_real.dropna(inplace=True)
    
    print(f"✅ Gerçek Veri Seti Hazır: {len(df_real)} örnek.")

except FileNotFoundError:
    print("❌ HATA: 'sensor_data.csv' dosyası bulunamadı.")
    exit()

# ==========================================
# 2. ADIM: SENTETİK ANOMALİ ÜRETİMİ
# ==========================================
print("[BİLGİ] Model eğitimi için sentetik anomali verileri üretiliyor...")

anomali_listesi = []

for col in df_real.columns:
    mu = df_real[col].mean()
    sigma = df_real[col].std()
    
    if sigma == 0: sigma = mu * 0.1 if mu != 0 else 1
    
    # Sensör tipine göre tolerans katsayısı belirleme
    if col == 'temp':
        katsayi = TEMP_SIGMA
    else:
        katsayi = DEFAULT_SIGMA
    
    limit_ust = mu + (katsayi * sigma)
    limit_alt = mu - (katsayi * sigma)
    
    # Anomali Örneklem Sayısı (Düşük tutularak modelin bunları aykırı görmesi sağlanır)
    SAMPLE_SIZE = 5 
    
    # 1. Üst Limit Sapması
    high_anomali = df_real.sample(SAMPLE_SIZE).copy()
    high_anomali[col] = np.random.uniform(limit_ust, limit_ust * 1.5, SAMPLE_SIZE)
    anomali_listesi.append(high_anomali)
    
    # 2. Alt Limit Sapması
    low_anomali = df_real.sample(SAMPLE_SIZE).copy()
    val_min = limit_alt * 1.5 if col == 'temp' else max(0, limit_alt * 0.5)
    low_anomali[col] = np.random.uniform(val_min, limit_alt, SAMPLE_SIZE)
    anomali_listesi.append(low_anomali)

# Veri setlerini birleştirme
df_anomali = pd.concat(anomali_listesi, ignore_index=True)
df_final = pd.concat([df_real, df_anomali], ignore_index=True)
df_final = df_final.sample(frac=1).reset_index(drop=True)

print(f"[BİLGİ] Eğitim Seti: {len(df_real)} Normal + {len(df_anomali)} Anomali Verisi")

# ==========================================
# 3. ADIM: MODEL EĞİTİMİ
# ==========================================
print("[BİLGİ] Isolation Forest algoritması eğitiliyor...")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_final)

# Modelin oluşturulması ve eğitilmesi
model = IsolationForest(n_estimators=100, contamination=CONTAMINATION_RATE, random_state=42)
model.fit(X_scaled)

# ==========================================
# 4. ADIM: SONUÇLARIN KAYDEDİLMESİ
# ==========================================
df_final['tahmin'] = model.predict(X_scaled)
df_final['durum'] = df_final['tahmin'].apply(lambda x: 'ANOMALI' if x == -1 else 'NORMAL')
df_final.to_csv('tugba_icin_veri.csv', index=False)

joblib.dump(model, 'model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("-" * 50)
print("✅ MODEL EĞİTİMİ BAŞARIYLA TAMAMLANDI.")
print("📁 Oluşturulan Dosyalar:")
print("   - model.pkl (Eğitilmiş Model)")
print("   - scaler.pkl (Ölçekleyici)")
print("   - tugba_icin_veri.csv (Analiz Verisi)")
print("-" * 50)