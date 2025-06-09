# RoboCopy Benzeri GUI Dosya Kopyalama Uygulaması

Aşağıda Python'da tkinter kullanarak oluşturulmuş, RoboCopy benzeri bir GUI dosya kopyalama uygulaması bulunmaktadır. Bu uygulama temel RoboCopy parametrelerini destekler ve kullanıcı dostu bir arayüz sunar.

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

Bu uygulama temel RoboCopy işlevlerini sağlar, ancak daha fazla özellik eklemek için genişletilebilir.
