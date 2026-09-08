from PIL import Image
import numpy as np

# Açık renkten koyu renge doğru karakter rampası
RAMP = " .`:-=+*cs#%@"

try:
    img = Image.open("source-prepped.png").convert("L")
except FileNotFoundError:
    print("Hata: source-prepped.png bulunamadı.")
    exit(1)

# Terminal formatı için 100x53 yeniden boyutlandırma
width, height = 100, 53
img = img.resize((width, height), Image.Resampling.LANCZOS)
pixels = np.array(img)

svg_out = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width*6} {height*12}" width="{width*6}" height="{height*12}">\n'
svg_out += '<style>\n.text { font-family: monospace; font-size: 10px; fill: #8b949e; white-space: pre; }\n</style>\n'
svg_out += '<rect width="100%" height="100%" fill="#0d1117"/>\n'

for y in range(height):
    line = ""
    for x in range(width):
        pixel_val = pixels[y, x]
        idx = int((pixel_val / 255.0) * (len(RAMP) - 1))
        # Koyu alanlara yoğun karakter, açık alanlara boşluk
        line += RAMP[-(idx+1)]
    
    # Satır satır animasyon gecikmesi
    delay = y * 0.05
    y_pos = (y + 1) * 12
    escaped_line = line.replace("&", "&amp;").replace("<", "&lt;")
    
    svg_out += f'<g><clipPath id="c{y}"><rect x="0" y="{y_pos-10}" width="0" height="12"><animate attributeName="width" from="0" to="{width*6}" dur="1s" begin="{delay}s" fill="freeze" /></rect></clipPath>\n'
    svg_out += f'<text x="0" y="{y_pos}" class="text" clip-path="url(#c{y})">{escaped_line}</text></g>\n'

svg_out += '</svg>'

with open("avi-ascii.svg", "w", encoding="utf-8") as f:
    f.write(svg_out)