from PIL import Image
import struct
import os

# ---------- PNG ----------
BLACK_AND_WHITE_PNG = r"C:\lab1\bw.png"
GREY_PNG = r"C:\lab1\grey.png"
COLORS_PNG = r"C:\lab1\colors.png"

RAW_BW_PNG = r"C:\lab1\bw.raw"
RAW_GREY_PNG = r"C:\lab1\grey.raw"
RAW_COLORS_PNG = r"C:\lab1\colors.raw"

# ---------- JPG ----------
BLACK_AND_WHITE_JPG = r"C:\lab1\bw.jpg"
GREY_JPG = r"C:\lab1\grey.jpg"
COLORS_JPG = r"C:\lab1\colors.jpg"

RAW_BW_JPG = r"C:\lab1\bw_jpg.raw"
RAW_GREY_JPG = r"C:\lab1\grey_jpg.raw"
RAW_COLORS_JPG = r"C:\lab1\colors_jpg.raw"

def image_to_raw(input_path, output_path, image_type):
    img = Image.open(input_path)
    width, height = img.size

    if image_type == "bw":
        img = img.convert("1")
        mode = 0
        bytes_per_pixel = 1

        data = bytearray()
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                data.append(0 if pixel == 0 else 1)

    elif image_type == "gray":
        img = img.convert("L")
        mode = 1
        bytes_per_pixel = 1
        data = img.tobytes()

    else:
        img = img.convert("RGB")
        mode = 2
        bytes_per_pixel = 3
        data = img.tobytes()

    with open(output_path, "wb") as f:
        f.write(struct.pack("B", mode))
        f.write(struct.pack(">I", width))
        f.write(struct.pack(">I", height))
        f.write(data)

    original_size = os.path.getsize(input_path)
    raw_size = os.path.getsize(output_path)

    print(f"\nИсходник: {input_path}")
    print(f"    Размер: {original_size} байт")
    print(f"RAW: {output_path}")
    print(f"    Размер: {raw_size} байт")
    print(f"    Тип: {image_type}")
    print(f"    Разрешение: {width} x {height}")
    print(f"    Без метаданных: {width * height * bytes_per_pixel} байт")

    if raw_size != 0:
        print(f"    RAW / исходник: {raw_size / original_size:.2f}")
        print(f"    Сжатие: {original_size / raw_size:.2f}x\n")


# ---------- PNG ----------
image_to_raw(BLACK_AND_WHITE_PNG, RAW_BW_PNG, 'bw')
image_to_raw(GREY_PNG, RAW_GREY_PNG, 'gray')
image_to_raw(COLORS_PNG, RAW_COLORS_PNG, 'rgb')

# ---------- JPG ----------
image_to_raw(BLACK_AND_WHITE_JPG, RAW_BW_JPG, 'bw')
image_to_raw(GREY_JPG, RAW_GREY_JPG, 'gray')
image_to_raw(COLORS_JPG, RAW_COLORS_JPG, 'rgb')
