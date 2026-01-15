# 🛠️ IoT ve Yapay Zeka Tabanlı Kestirimci Bakım Sistemi (Predictive Maintenance)

Bu proje, sistemlerin sağlık durumunu anlık olarak izlemek, olası arızaları önceden tespit etmek ve bulut üzerinden yönetmek amacıyla geliştirilmiş kapsamlı bir **IoT (Nesnelerin İnterneti)** uygulamasıdır.

## 👥 Proje Hakkında
Sınıf arkadaşlarımla birlikte **takım çalışması** olarak geliştirdiğimiz bu projede; endüstriyel bir senaryoyu simüle eden bir yapı kurduk. Sistemimiz, ortamdan ve cihaz üzerinden topladığı verileri analiz ederek bir sorun oluşmadan önce müdahale edilmesine olanak sağlar.

Projemiz şu temel gereksinimleri karşılayacak şekilde tasarlanmıştır:
* **Merkezi Kontrol:** Raspberry Pi kullanılarak sistemin yönetilmesi.
* **Veri Toplama:** En az **5 farklı sensör** ile ortam ve cihaz verilerinin (sıcaklık, titreşim, akım vb.) toplanması.
* **Aksiyon:** Gelen verilere göre **3 farklı Actuator** (Motor, Fan, Alarm vb.) tetiklenerek sisteme müdahale edilmesi.
* **Bulut Entegrasyonu:** Tüm verilerin **Bulut Tabanlı bir IoT Platformuna** aktarılarak uzaktan monitörize edilmesi.

## 🧠 Benim Projedeki Rolüm: Yapay Zeka ve Karar Destek
Bu ekip çalışmasında ben, toplanan verilerin anlamlandırılması ve sistemin "akıllı" kararlar vermesini sağlayan **Yapay Zeka** tarafına odaklandım.

Sensörlerden akan ham verileri alıp işleyerek şunları gerçekleştirdim:
* **Karar Destek Algoritmaları:** Sistemin sadece belirlenen eşik değerlerine göre değil, verilerin gidişatına göre akıllı kararlar vermesini sağlayan algoritmaların geliştirilmesi.
* **Anomali Tespiti:** Sistem normal çalışırken oluşan en ufak sapmaların yapay zeka algoritmalarıyla tespit edilmesi ve kestirimci bakım uyarısı verilmesi.
* **Veri Analizi:** Raspberry Pi üzerinde çalışan Python kodları ile verilerin analiz edilip aksiyon mekanizmasının (Actuator'ların) doğru zamanda tetiklenmesinin sağlanması.

## 🛠️ Kullanılan Teknolojiler
* **Donanım:** Raspberry Pi (Ana Sunucu), Sensör Seti (5+ Adet), Actuatorler (3 Adet)
* **Yazılım:** Python (Yapay Zeka ve Backend Kodları)
* **IoT:** Bulut Tabanlı İzleme Platformu (Cloud Monitoring)
* **Yöntem:** Kestirimci Bakım (Predictive Maintenance) Prensipleri
