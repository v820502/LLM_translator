from PIL import Image, ImageDraw

# 創建一個 64x64 的圖像
img = Image.new('RGBA', (64, 64), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# 繪製一個簡單的翻譯圖標
draw.rectangle([10, 10, 54, 54], fill='#4a90e2', outline='#2171c7', width=2)
draw.text((20, 20), "T", fill='white', font=None, font_size=24)

# 保存圖標
img.save('icon.png') 