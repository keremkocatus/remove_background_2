import os
from PIL import Image

def strip_meta_and_measure(input_path, output_path):
    # Orijinali oku ve meta atarak yeniden kaydet
    img = Image.open(input_path)
    w, h = img.size
    
    if w<=1024 and h<=1024:
        scale = 1
    elif w>=h:
        scale = 1024 / w
    else:
        scale = 1024 / h
    
    img_resized = img.resize((int(scale*w), int(scale*h)), Image.Resampling.LANCZOS)
    img_resized.save(output_path, format="JPEG", quality=80, optimize=True, progressive=True)

    # Boyutları ölç
    before = os.path.getsize(input_path)
    after = os.path.getsize(output_path)
    print(f"Önce: {before/1024:.1f} KB\nSonra: {after/1024:.1f} KB\nFark: {(before-after)/1024:.1f} KB")

strip_meta_and_measure("./images/test_outfit_ai.jpg","output.jpg")