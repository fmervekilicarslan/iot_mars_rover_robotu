import joblib
import pandas as pd

# ==========================================
# GÜVENLİ ARALIKLAR (MARS STANDARDI)
# ==========================================
LIMITLER = {
    'voltage': {'min': 3.0,  'max': 7.0,  'msg_low': '⚠️ GÜÇ KESİNTİSİ / PİL BİTİK -> Pili Şarj Et!', 'msg_high': '⚠️ AŞIRI VOLTAJ -> Devre Yanabilir!'},
    'current': {'min': 8.1,  'max': 18.9, 'msg_low': '⚠️ KABLO KOPUK / AÇIK DEVRE -> Bağlantıları Kontrol Et.', 'msg_high': '⚠️ MOTOR SIKIŞMASI -> Tekerlekleri Kontrol Et!'},
    'sound':   {'min': 978,  'max': 1056, 'msg_low': '⚠️ SENSÖR HATASI -> Mikrofonu Kontrol Et.', 'msg_high': '⚠️ MEKANİK GÜRÜLTÜ / PATLAMA -> Motorları Durdur!'},
    'gas':     {'min': 614,  'max': 1432, 'msg_low': '⚠️ SENSÖR HATASI -> Gaz Sensörü Bozuk.', 'msg_high': '⚠️ GAZ KAÇAĞI / DUMAN -> Ortamı Havalandır!'},
    'temp':    {'min': 13.1, 'max': 33.0, 'msg_low': '⚠️ DONMA RİSKİ -> Isıtıcıları Aç.', 'msg_high': '⚠️ AŞIRI ISINMA -> Soğutma Sistemini Devreye Sok!'},
    'hum':     {'min': 43,   'max': 70,   'msg_low': '⚠️ AŞIRI KURU HAVA -> Statik Elektrik Riski.', 'msg_high': '⚠️ SU TEMASI / AŞIRI NEM -> Kurutma Modunu Aç!'},
    'heading': {'min': 158,  'max': 316,  'msg_low': '⚠️ ROTA SAPMASI (SOL) -> Yörüngeyi Düzelt.', 'msg_high': '⚠️ ROTA SAPMASI (SAĞ) -> Yörüngeyi Düzelt.'}
}

def model_yukle():
    print("🧠 Akıllı Teşhis Modülü yükleniyor...")
    try:
        model = joblib.load('model.pkl')
        scaler = joblib.load('scaler.pkl')
        print("✅ Hazır!")
        return model, scaler
    except Exception as e:
        print(f"❌ HATA: {e}")
        return None, None

def detayli_analiz(veri):
    rapor = []

    if float(veri["voltage"]) < 3.0:
        rapor.append({
            "tip": "DÜŞÜK VOLTAGE",
            "deger": float(veri["voltage"]),
            "limit": 3.0,
            "aciklama": "GÜÇ KESİNTİSİ / PİL BİTİK",
            "oneri": "Pili şarj et"
        })

    if float(veri["current"]) < 8.1:
        rapor.append({
            "tip": "DÜŞÜK CURRENT",
            "deger": float(veri["current"]),
            "limit": 8.1,
            "aciklama": "KABLO KOPUK / AÇIK DEVRE",
            "oneri": "Bağlantıları kontrol et"
        })

    if float(veri["sound"]) < 978:
        rapor.append({
            "tip": "DÜŞÜK SOUND",
            "deger": float(veri["sound"]),
            "limit": 978,
            "aciklama": "SENSÖR HATASI",
            "oneri": "Mikrofonu kontrol et"
        })

    if float(veri["gas"]) < 614:
        rapor.append({
            "tip": "DÜŞÜK GAS",
            "deger": float(veri["gas"]),
            "limit": 614,
            "aciklama": "SENSÖR HATASI",
            "oneri": "Gaz sensörünü kontrol et"
        })

    return rapor


def anomali_kontrol(model, scaler, voltage, current, sound, gas, temp, hum, heading):
    """
    Hem AI tahmini yapar hem de detaylı açıklama döndürür.
    Girdi olarak gelen string/float verileri güvenli şekilde float'a çevirir.
    """

    def to_float(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return None

    cols = ['voltage', 'current', 'sound', 'gas', 'temp', 'hum', 'heading']

    raw_values = [voltage, current, sound, gas, temp, hum, heading]
    clean_values = [to_float(v) for v in raw_values]

    # Eğer herhangi bir sensör değeri float'a çevrilemediyse
    if any(v is None for v in clean_values):
        return {
            "durum": "HATA",
            "mesaj": "Geçersiz sensör verisi (float'a çevrilemeyen değer var)"
        }

    veri_dict = dict(zip(cols, clean_values))

    # DataFrame oluşturma
    yeni_veri = pd.DataFrame([clean_values], columns=cols)

    # Ölçekleme + AI tahmini
    veri_scaled = scaler.transform(yeni_veri)
    ai_sonuc = model.predict(veri_scaled)[0]

    if ai_sonuc == 1:
        return {"durum": "NORMAL", "mesaj": "Sistem Stabil."}
    else:
        aciklama = detayli_analiz(veri_dict)
        return {"durum": "ANOMALİ", "mesaj": aciklama}
