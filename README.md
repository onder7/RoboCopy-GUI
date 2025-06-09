# RoboCopy Benzeri GUI Dosya Kopyalama Uygulaması

Aşağıda Python'da tkinter kullanarak oluşturulmuş, RoboCopy benzeri bir GUI dosya kopyalama uygulaması bulunmaktadır. Bu uygulama temel RoboCopy parametrelerini destekler ve kullanıcı dostu bir arayüz sunar.

v1

![image](https://github.com/user-attachments/assets/608d07ca-99ef-4b59-94ca-68c100584490)

v2

![image](https://github.com/user-attachments/assets/df35bc0d-1ad7-4090-bd42-d32ca28ab4f8)


## Özellikler

1. **Temel RoboCopy Parametreleri**:
   - Alt dizinleri kopyalama (/S)
   - Boş dizinleri kopyalama (/E)
   - Varolan dosyaların üzerine yazma (/IS)
   - Aynalama modu (/MIR)
   - Dosya taşıma (/MOV)
   - Dosya filtresi (*.txt gibi)

2. **GUI Özellikleri**:
   - Kaynak ve hedef dizin seçimi için gözat butonları
   - İşlem ilerleme çubuğu
   - Detaylı günlük ekranı
   - Kopyalama işlemini durdurma butonu

3. **Diğer Özellikler**:
   - Uzun süren işlemler için thread kullanımı
   - Hata yönetimi
   - Kullanıcı dostu mesajlar

## Kurulum ve Kullanım

1. Python'un yüklü olduğundan emin olun (3.x versiyonu önerilir)
2. Kodu bir `.py` dosyasına kaydedin
3. Komut satırından `python dosya_adi.py` komutuyla çalıştırın
4. Arayüzde kaynak ve hedef dizinleri seçin, istediğiniz parametreleri ayarlayın ve "Kopyalamayı Başlat" butonuna tıklayın

Python Uygulamasını EXE Dosyasına Dönüştürme

pyinstaller --onefile --windowed --name="RoboCopy GUI" mainv2.py

Bu uygulama temel RoboCopy işlevlerini sağlar, ancak daha fazla özellik eklemek için genişletilebilir.


## V3 Eklenen Yeni Özellikler
![image](https://github.com/user-attachments/assets/1dfbc3df-8311-484d-9719-f39301deb7b3)

Değişiklik Algılama ve Otomatik Kopyalama:

Kaynak dizindeki dosyaları belirli aralıklarla kontrol eder

Değişen veya yeni dosyaları otomatik olarak kopyalar

Dosya hash'leri ve zaman damgaları karşılaştırılır

Zamanlanmış Kopyalama:

Belirli bir saatte otomatik kopyalama yapabilme

Günlük veya tek seferlik zamanlama desteği

HH:MM formatında zaman girilebilir

İşlem Sonrası Bilgisayarı Kapatma:

Kopyalama tamamlandığında bilgisayarı otomatik kapatma

60 saniye geri sayım ile iptal şansı

Ek Önerilen Özellikler:

Email bildirimi (işlem tamamlandığında)

Dosya sıkıştırma seçeneği

Daha gelişmiş hata yönetimi

İzleme modu için ayrı buton ve arayüz

Kullanım
Değişiklik İzleme:

"İzlemeyi Başlat" butonuna basın

Kontrol aralığını dakika cinsinden ayarlayın

Kırmızı buton izlemenin aktif olduğunu gösterir

Zamanlanmış Kopyalama:

"Yeni Özellikler" sekmesinden zamanı ayarlayın

HH:MM formatında zaman girin (örn: 23:30)

Zamanlanmış kopyalama etkinleştirin

Bilgisayarı Kapatma:

Aynı sekmedeki seçeneği işaretleyin

Kopyalama tamamlandığında bilgisayar kapanacaktır
