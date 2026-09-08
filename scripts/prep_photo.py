import cv2
import numpy as np
from rembg import remove
from PIL import Image
import io
import sys

if len(sys.argv) < 2:
    print("Hata: Kaynak resim belirtilmedi.")
    sys.exit(1)

input_path = sys.argv[1]
output_path = 'source-prepped.png'

# Arka planı sil
with open(input_path, 'rb') as i:
    input_bg_removed = remove(i.read())

img = Image.open(io.BytesIO(input_bg_removed)).convert("RGBA")

# Saydam arka planı beyaz yap (kontrast için)
background = Image.new("RGBA", img.size, (255, 255, 255, 255))
alpha_composite = Image.alpha_composite(background, img)
alpha_composite_3 = alpha_composite.convert("RGB")

# CLAHE ile yerel kontrastı artır
cv_img = np.array(alpha_composite_3)
cv_img = cv_img[:, :, ::-1].copy() 
gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(gray)

cv2.imwrite(output_path, cl1)
print(f"İşlenmiş fotoğraf kaydedildi: {output_path}")