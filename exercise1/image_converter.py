"""
конвертация изображений в RAW формат
задание 1, пункт 1
"""

import numpy as np
from PIL import Image
import struct


def convert_jpeg_to_raw(input_path, output_path):
    """конвертация JPEG в RAW формат с метаданными"""
    img = Image.open(input_path)

    if img.mode == '1' or img.mode == 'P':
        img = img.convert('1')
        img_type = 1  # черно-белое
    elif img.mode == 'L':
        img_type = 2  # оттенки серого
    else:
        img = img.convert('RGB')
        img_type = 3  # цветное

    width, height = img.size
    raw_data = np.array(img)

    # заголовок: тип (1 байт), ширина (4), высота (4)
    with open(output_path, 'wb') as f:
        f.write(struct.pack('B', img_type))
        f.write(struct.pack('I', width))
        f.write(struct.pack('I', height))
        raw_data.tofile(f)

    print(f"сохранено: {output_path}")
    print(f"тип: {img_type}, размер: {width}x{height}")

if __name__ == "__main__":
    convert_jpeg_to_raw('colors.png', '../analysis/color.raw')
