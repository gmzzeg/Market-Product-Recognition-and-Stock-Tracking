import cv2 as cv
import time
import pandas as pd
from datetime import datetime
import os

# YOLO için güven eşikleri
Conf_threshold = 0.70
NMS_threshold = 0.30

# Sınıf adları (modelden gelen detaylı etiketler)
class_name = ["doritos hot cips", "eti karam cikolata", "yumos sakura yumusatici", "elidor sampuan",
              " asya su", "demlik suzen poset siyah cay", "kurukahveci mehmet efendi turk kahvesi",
              "pinar suzme peynir", "makarna", "billur tuz","petek toz seker"]

# Temizle (baş/son boşlukları kaldır)
class_name = [name.strip() for name in class_name]

# Ürün fiyatlarını temsil eden sözlük (kategori bazlı)
product_prices = {
    "cips": 20,
    "cikolata": 15,
    "deterjan": 50,
    "sampuan": 30,
    "su": 5,
    "yag": 60,
    "kahve": 40,
    "peynir": 70,
    "makarna": 12,
    "tuz": 8,
    "seker": 25
}

# Detaylı etiketleri kategoriye eşleyecek anahtar kelime listesi
keyword_map = {
    "cips": ["cips", "doritos", "lays"],
    "cikolata": ["cikolata", "çikolata", "eti", "ülker"],
    "deterjan": ["deterjan", "yumusatici", "yumos", "soft", "detergent"],
    "sampuan": ["sampuan", "şampuan", "elidor"],
    "su": ["su", "pinar", "asya"],
    "yag": ["yag", "yağ"],
    "kahve": ["kahve", "kurukahveci"],
    "peynir": ["peynir"],
    "makarna": ["makarna"],
    "tuz": ["tuz"],
    "seker": ["seker", "şeker"]
}

def map_to_category(detailed_name):
    s = detailed_name.lower()
    for cat, keywords in keyword_map.items():
        for kw in keywords:
            if kw in s:
                return cat
    # fallback: son kelimeyi deney
    last = s.split()[-1]
    if last in product_prices:
        return last
    # bulunamazsa None döndür
    return None

# YOLOv4-tiny modelini yükler
net = cv.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
model = cv.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

# Log dosyası oluşturulmazsa sıfırdan oluştur
log_file = "log.xlsx"
if not os.path.exists(log_file):
    df = pd.DataFrame(columns=["Time", "Class", "Confidence", "Price", "StockStatus"])
    df.to_excel(log_file, index=False)

# Stok takibi için stok dosyası oluşturulmazsa sıfırdan oluştur
stok_file = "stok.xlsx"
if not os.path.exists(stok_file):
    fiyat_list = []
    for name in class_name:
        cat = map_to_category(name)
        if cat is None:
            print(f"UYARI: '{name}' için kategori bulunamadı. Fiyat 0 olarak ayarlandı.")
            fiyat_list.append(0)
        else:
            fiyat_list.append(product_prices[cat])

    stok_df = pd.DataFrame({
        "ClassID": list(range(len(class_name))),
        "ClassName": class_name,
        "Stock": [10] * len(class_name),
        "Durum": ["VAR"] * len(class_name),
        "Fiyat": fiyat_list
    })
    stok_df.to_excel(stok_file, index=False)

# Kamerayı başlat
cap = cv.VideoCapture(0)

last_logged_class = None
last_log_time = 0
log_interval = 2

fps_frame_count = 0
fps_start_time = time.time()
effective_fps = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    result = model.detect(frame, Conf_threshold, NMS_threshold)

    if len(result) == 3:
        classes, scores, boxes = result
    else:
        classes, scores, boxes = [], [], []

    if len(classes) > 0:
        for classid, score, box in zip(classes.flatten(), scores.flatten(), boxes):
            color = (0, 255, 255)
            label = f"{class_name[classid]} : {score:.2f}"
            cv.rectangle(frame, box, color, 2)
            cv.putText(frame, label, (box[0], box[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            detected_class = class_name[classid]
            current_time = time.time()

            if detected_class != last_logged_class or (current_time - last_log_time) > log_interval:
                stok_df = pd.read_excel(stok_file)

                if "Fiyat" not in stok_df.columns:
                    print("HATA: 'Fiyat' sütunu stok.xlsx dosyasında bulunamadı!")
                    print("Mevcut sütunlar:", stok_df.columns.tolist())
                    break

                row_index = stok_df.index[stok_df["ClassID"] == classid][0]
                current_stock = stok_df.at[row_index, "Stock"]
                product_price = stok_df.at[row_index, "Fiyat"]

                if current_stock > 0:
                    stok_df.at[row_index, "Stock"] = current_stock - 1
                    stok_df.at[row_index, "Durum"] = "VAR" if current_stock - 1 > 0 else "TÜKENDİ"
                    print(f"Ürün: {detected_class} | Fiyat: {product_price} TL | Stok: {current_stock - 1} adet")
                else:
                    stok_df.at[row_index, "Durum"] = "TÜKENDİ"
                    print(f"UYARI: {detected_class} stoğu TÜKENDİ! | Fiyat: {product_price} TL")

                stok_df.to_excel(stok_file, index=False)

                log_df = pd.read_excel(log_file)
                new_log = {
                    "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Class": detected_class,
                    "Confidence": float(score),
                    "Price": product_price,
                    "StockStatus": stok_df.at[row_index, "Durum"]
                }
                log_df = pd.concat([log_df, pd.DataFrame([new_log])], ignore_index=True)
                log_df.to_excel(log_file, index=False)

                last_logged_class = detected_class
                last_log_time = current_time

    fps_frame_count += 1
    if time.time() - fps_start_time >= 1:
        effective_fps = fps_frame_count / (time.time() - fps_start_time)
        fps_frame_count = 0
        fps_start_time = time.time()

    cv.putText(frame, f"FPS: {effective_fps:.2f}", (20, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv.imshow("Frame", frame)
    if cv.waitKey(1) == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
