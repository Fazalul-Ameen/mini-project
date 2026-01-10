from PIL import Image, ImageChops, ImageEnhance

def ela_image(path, quality=90):
    original = Image.open(path)
    temp_path = "temp.jpg"
    original.save(temp_path, "JPEG", quality=quality)
    compressed = Image.open(temp_path)
    ela = ImageChops.difference(original, compressed)
    enhancer = ImageEnhance.Brightness(ela)
    ela = enhancer.enhance(10)
    return ela
