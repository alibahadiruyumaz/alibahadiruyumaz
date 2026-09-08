import json
import os

try:
    with open("data/contributions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("Hata: Veri bulunamadı. Önce fetch_contributions.py çalıştırılmalı.")
    exit(1)

# GitHub Heatmap renk paleti
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

box_size = 12
gap = 4
svg_width = 860
svg_height = 200

# SVG Başlangıcı ve CSS Animasyonları
svg_content = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
<style>
    .box {{ opacity: 0; animation: slideIn 0.8s forwards; rx: 2px; }}
    @keyframes slideIn {{
        0% {{ opacity: 0; transform: translateY(-10px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}
    .bg {{ fill: #0d1117; rx: 10px; }}
</style>
<rect width="100%" height="100%" class="bg"/>
<g transform="translate(20, 20)">
'''

# Kutucukların Çizilmesi ve Çapraz Animasyon Staggering'i
for i, day in enumerate(data):
    week = i // 7
    day_of_week = i % 7
    
    x = week * (box_size + gap)
    y = day_of_week * (box_size + gap)
    
    level = int(day.get("level", 0))
    color = PALETTE[level] if level < len(PALETTE) else PALETTE[-1]
    
    # Animasyon gecikmesi: Sol üstten sağ alta doğru akış
    delay = (week * 0.02) + (day_of_week * 0.02)
    
    svg_content += f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" class="box" style="animation-delay: {delay}s;" />\n'

svg_content += '''</g>\n</svg>'''

with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("contrib-heatmap.svg başarıyla oluşturuldu.")