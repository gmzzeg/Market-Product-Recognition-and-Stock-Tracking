import cv2 as cv
import os

# YOLO için güven eşikleri
CONF_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4

# Sınıf adları (modelden gelen detaylı etiketler)
class_names = ["doritos hot cips", "eti karam cikolata", "yumos sakura yumusatici",
               "elidor sampuan", "asya su", "demlik suzen poset siyah cay",
               "kurukahveci mehmet efendi turk kahvesi", "pinar suzme peynir",
               "makarna", "billur tuz"]

# Model dosyaları
weights_path = "yolov4-tiny.weights"
cfg_path = "yolov4-tiny.cfg"

# Modeli yükle
net = cv.dnn.readNet(weights_path, cfg_path)
model = cv.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

# Test edilecek resim yolu
test_image_path = "test_image.jpg"  #

# Resmi yükle
if not os.path.exists(test_image_path):
    raise FileNotFoundError(f"Resim bulunamadı: {test_image_path}")

image = cv.imread(test_image_path)
height, width = image.shape[:2]

# Nesneleri tespit et
classes, scores, boxes = model.detect(image, CONF_THRESHOLD, NMS_THRESHOLD)

# Tespit edilen nesneleri ekrana çiz
if len(classes) > 0:
    for classid, score, box in zip(classes.flatten(), scores.flatten(), boxes):
        color = (0, 255, 0)  # Yeşil kutu
        label = f"{class_names[classid]}: {score:.2f}"
        cv.rectangle(image, box, color, 2)
        cv.putText(image, label, (box[0], box[1] - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
else:
    print("Resimde nesne bulunamadı.")

# Sonucu göster
cv.imshow("Detection Result", image)
cv.waitKey(0)
cv.destroyAllWindows()
