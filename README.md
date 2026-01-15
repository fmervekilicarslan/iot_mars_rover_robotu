# 🤖 Mars Rover Konseptli Kestirimci Bakım Robotu (IoT & AI)

Bu proje, endüstriyel sahalarda ortam denetimi yapmak ve arızaları önceden tespit etmek (Kestirimci Bakım) amacıyla geliştirilmiş, **uzaktan kontrol edilebilen** ve **otonom özelliklere sahip** bir robot prototipidir.

## 👥 Proje Hakkında
Sınıf arkadaşlarımla bir **takım çalışması** olarak geliştirdiğimiz bu projede; Mars Rover araçlarından ilham alan bir robot tasarladık. Sistem, Raspberry Pi merkezli bir mimari ile çalışmakta olup, hem kendi kararlarını verebilmekte hem de bir operatör tarafından yönetilebilmektedir.

### ⚙️ Sistemin Temel Yetenekleri
* **Uzaktan Kontrol Paneli (Desktop Dashboard):** Geliştirdiğimiz masaüstü arayüzü sayesinde robotun hareketleri bilgisayar üzerinden manuel olarak kontrol edilebilir.
* **Canlı İzleme:** Üzerindeki **5+ farklı sensörden** gelen veriler (sıcaklık, gaz, titreşim vb.) anlık olarak kontrol paneline ve bulut sistemine aktarılır.
* **Otonom Müdahale:** Kritik durumlarda (örneğin gaz kaçağı veya aşırı ısınma) robot üzerindeki **3 farklı eyleyiciyi (actuator)** otomatik olarak devreye sokar.
* **Hibrit Sürüş:** Sistem hem otonom olarak ortamı tarayabilir hem de manuel modda spesifik noktalara yönlendirilebilir.

## 🧠 Benim Projedeki Rolüm: Yapay Zeka ve Karar Destek
Bu ekip çalışmasında ben, robotun "karar verme mekanizması" ve "veri analitiği" süreçlerine odaklandım:

* **Yapay Zeka Destekli Karar:** Sensörlerden gelen ham verilerin işlenmesi ve anomali tespiti algoritmalarının geliştirilmesi.
* **Veri Analizi:** Sistemin sadece belirlenen eşik değerlerine göre değil, verilerin akışına göre akıllı aksiyonlar almasını sağlayan Python kodlarının yazılması.
* **Backend Entegrasyonu:** Sensör verilerinin kontrol paneli ve bulut platformu ile haberleşmesinde ekip arkadaşlarımla birlikte aktif rol aldım.

## 🛠️ Kullanılan Teknolojiler
* **Donanım:** Raspberry Pi (Ana Sunucu), Sensör Seti, DC Motorlar
* **Yazılım:** Python (AI & Backend), Masaüstü Kontrol Arayüzü (GUI)
* **IoT:** Bulut Tabanlı İzleme Platformu (Cloud Monitoring)
* **Konsept:** Kestirimci Bakım (Predictive Maintenance) & Tele-Operasyon
