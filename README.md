<div align="center">
  <img src="video.gif" alt="Video Demo" width="320">
</div>

# Market Ürün Tanıma ve Stok Takibi 

Bu proje, **market ürünlerini kamera üzerinden gerçek zamanlı tanıyıp stok bilgisini otomatik güncelleyen** bir sistemdir.  
**YOLOv4 Tiny** nesne tanıma modeli kullanılarak ürünler tespit edilir, ekranda kutucuk içine alınarak adları ve doğruluk oranları gösterilir.  
Tespit edilen ürünlerin stok miktarları **Excel tablosunda otomatik güncellenir** ve tüm işlem geçmişi ayrı bir log dosyasına kaydedilir.  

---

## Özellikler  

- **Gerçek zamanlı ürün tanıma** – YOLOv4 Tiny ile hızlı ve doğru nesne tespiti  
- **Görsel gösterim** – OpenCV ile ürünlerin kutucuk ve güven skoru ile ekranda işaretlenmesi  
- **Stok takibi** – Pandas ile `stok.xlsx` dosyasındaki stokların otomatik güncellenmesi  
-  **Log kaydı** – Her tespit için `log.xlsx` dosyasına zaman, ürün, güven skoru, fiyat ve stok durumu kaydedilmesi  
- **Dinamik fiyatlandırma** – Ürün kategorilerine göre fiyat eşleştirme desteği  

---

## Çalışma Mantığı  

1. Kamera açılır ve görüntü alınır.  
2. YOLOv4 Tiny modeli ile ürünler algılanır.  
3. Algılanan ürün adı ve doğruluk oranı ekranda gösterilir.  
4. Excel üzerinde ilgili ürünün stoğu **1 azaltılır**.  
5. Güncel stok durumu (**VAR / TÜKENDİ**) kaydedilir.  
6. Her işlem, `log.xlsx` dosyasına zaman damgası ile yazılır.  

---

## Proje Dizini  

 -obj/                 # Etiketli veri seti (11 sınıf için resimler ve YOLO formatında txt dosyaları). 
 
 -output/              # Eğitim test çıktıları
 
 -test/                # Test için resimler ve kod (image_test.py)
 
 -training/            # YOLOv4-tiny ağırlık dosyası (yolov4-tiny.weights) burada bulunur.
 
 -class.txt            # Sınıf isimleri listesi
 
 -log.xlsx             # Tespit loglarının tutulduğu Excel dosyası (script otomatik oluşturur)
 
 -obj.data             # YOLO eğitim parametrelerini tanımlar. Bu dosyada sınıf sayısı, eğitim/test veri listelerinin yolları, sınıf isim dosyası ve eğitim sırasında elde edilen ağırlıkların kaydedileceği dizin belirtilmiştir.
 
 -stok.xlsx            # Ürün stok bilgileri (script otomatik oluşturur, ilk değerler burada)
 
 -realtime_detect.py   # Canlı kamera için ana script (mevcut dosya adı)
 
 -yolov4-tiny.cfg      # YOLOv4-tiny konfigürasyon dosyası

---

## Çalışma Detayları:

Kameradan gerçek zamanlı algılama yapmak için `yolov4-tiny.weights` ağırlık dosyası ile birlikte `realtime_detect.py` dosyasını çalıştırmanız gerekir. Bu işlem kamerayı açacak, ürünleri tespit edecek ve her tespit sonrası ilgili ürünün stok miktarını otomatik olarak azaltacaktır. Ancak model yalnızca sınırlı ve belirli ürünler için eğitildiğinden, elinizde bu ürünler bulunmayabilir. Bu durumda, test amaçlı olarak `test/` klasöründe yer alan örnek görüntüleri kullanabilir ve `image_test.py` dosyasını çalıştırarak sistemin nasıl çalıştığını deneyimleyebilirsiniz. Yapılan tüm tespitler `log.xlsx` dosyasına kaydedilir; burada her bir ürün için doğruluk oranı, tarih ve saat bilgileri tutulur. Stokların güncel durumu ise `stok.xlsx` dosyasında izlenebilir. Bu dosya, başlangıçta ürünlerin stok sayılarını içerir ve tespitler sonrasında stok miktarlarını güncelleyerek stok kontrolünü kolaylaştırır.

NOT: Weights dosyası training/ dosyası içindedir. Etiketli veri seti için : https://drive.google.com/file/d/1TGlgg0kY7Z6TIKr8IhCjATZ-SmF3YWbw/view?usp=sharing indirebilirsiniz.
