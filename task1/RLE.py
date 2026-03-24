import struct
import os


def rle_encode(data: bytes, Ms=1, Mc=1) -> bytes:
    if not data:
        return b''
    result = bytearray()
    symbols = [data[i:i+Ms] for i in range(0, len(data), Ms)]
    i, n = 0, len(symbols)
    flag_bit = 1 << (8 * Mc - 1)
    max_count = flag_bit - 1

    while i < n:
        if i + 1 < n and symbols[i] == symbols[i + 1]:
            value = symbols[i]
            count = 1
            while i + count < n and symbols[i + count] == value and count < max_count:
                count += 1
            result.extend(count.to_bytes(Mc, 'big'))
            result.extend(value)
            i += count
        else:
            start = i
            while i < n:
                if i + 1 < n and symbols[i] == symbols[i + 1]:
                    break
                i += 1
                if i - start == max_count:
                    break
            result.extend((flag_bit | (i - start)).to_bytes(Mc, 'big'))
            for s in symbols[start:i]:
                result.extend(s)
    return bytes(result)


def rle_decode(data: bytes, Ms=1, Mc=1) -> bytes:
    result = bytearray()
    i = 0
    flag_bit = 1 << (8 * Mc - 1)
    while i < len(data):
        control = int.from_bytes(data[i:i+Mc], 'big')
        i += Mc
        if control & flag_bit:
            length = control & (flag_bit - 1)
            result.extend(data[i:i + length * Ms])
            i += length * Ms
        else:
            symbol = data[i:i + Ms]
            i += Ms
            result.extend(symbol * control)
    return bytes(result)


# === Файловый ввод/вывод с метаданными [Ms, Mc] ===

def write_rle_file(filename, encoded_data, Ms, Mc):
    with open(filename, 'wb') as f:
        f.write(struct.pack('BB', Ms, Mc))
        f.write(encoded_data)


def read_rle_file(filename):
    with open(filename, 'rb') as f:
        Ms, Mc = struct.unpack('BB', f.read(2))
        return f.read(), Ms, Mc


# === UTF-8: паддинг до фиксированной ширины ===

def utf8_to_fixed(data: bytes, width=4) -> bytes:
    result = bytearray()
    i = 0
    while i < len(data):
        b = data[i]
        clen = 1 if b < 0x80 else 2 if b < 0xE0 else 3 if b < 0xF0 else 4
        result.extend(data[i:i+clen] + b'\x00' * (width - clen))
        i += clen
    return bytes(result)


def fixed_to_utf8(data: bytes, width=4) -> bytes:
    result = bytearray()
    for i in range(0, len(data), width):
        b = data[i]
        clen = 1 if b < 0x80 else 2 if b < 0xE0 else 3 if b < 0xF0 else 4
        result.extend(data[i:i+clen])
    return bytes(result)


# === Оценка коэффициента сжатия (без записи в файл) ===

def estimate_ratio(data: bytes, Ms=1, Mc=1) -> float:
    if not data:
        return 1.0
    encoded = rle_encode(data, Ms, Mc)
    return len(data) / len(encoded)


# === Полный цикл: файл → RLE → файл → декод → файл ===

def full_roundtrip(input_path, Ms, Mc, label=""):
    with open(input_path, 'rb') as f:
        original = f.read()

    est = estimate_ratio(original, Ms, Mc)
    encoded = rle_encode(original, Ms, Mc)

    rle_path = input_path + ".rle"
    write_rle_file(rle_path, encoded, Ms, Mc)

    enc_from_file, Ms_r, Mc_r = read_rle_file(rle_path)
    decoded = rle_decode(enc_from_file, Ms_r, Mc_r)

    out_path = input_path + ".decoded"
    with open(out_path, 'wb') as f:
        f.write(decoded)

    orig_size = len(original)
    enc_size = os.path.getsize(rle_path)
    real_ratio = orig_size / enc_size if enc_size else 0
    ok = decoded == original

    print(f"  [{label}]")
    print(f"    Файл: {input_path}")
    print(f"    Оригинал: {orig_size} байт")
    print(f"    Сжатый:   {enc_size} байт (с метаданными)")
    print(f"    Оценка сжатия:  {est:.4f}")
    print(f"    Реальное сжатие: {real_ratio:.4f}")
    print(f"    Совпадение: {'✓' if ok else '✗ ОШИБКА!'}")
    print()

    return ok

def full_roundtrip_utf8(input_path, label=""):
    with open(input_path, 'rb') as f:
        original = f.read()

    padded = utf8_to_fixed(original, width=4)
    Ms, Mc = 4, 1

    encoded = rle_encode(padded, Ms, Mc)

    # Оценку тоже считаем от оригинала, чтобы было честно
    est = len(original) / len(encoded) if encoded else 0
    encoded = rle_encode(padded, Ms, Mc)

    rle_path = input_path + ".rle"
    write_rle_file(rle_path, encoded, Ms, Mc)

    enc_from_file, Ms_r, Mc_r = read_rle_file(rle_path)
    decoded_padded = rle_decode(enc_from_file, Ms_r, Mc_r)
    decoded = fixed_to_utf8(decoded_padded, width=4)

    out_path = input_path + ".decoded"
    with open(out_path, 'wb') as f:
        f.write(decoded)

    orig_size = len(original)
    enc_size = os.path.getsize(rle_path)
    real_ratio = orig_size / enc_size if enc_size else 0
    ok = decoded == original

    print(f"  [{label}]")
    print(f"    Файл: {input_path}")
    print(f"    Оригинал: {orig_size} байт")
    print(f"    После паддинга: {len(padded)} байт")
    print(f"    Сжатый:   {enc_size} байт (с метаданными)")
    print(f"    Оценка сжатия:  {est:.4f}")
    print(f"    Реальное сжатие: {real_ratio:.4f}")
    print(f"    Совпадение: {'✓' if ok else '✗ ОШИБКА!'}")
    print()

    return ok


# =============================================
# ТЕСТОВЫЕ ФАЙЛЫ
# =============================================

RAW_BW_PNG   = r"C:\lab1\bw.raw"
RAW_GREY_PNG = r"C:\lab1\grey.raw"
RAW_COLORS_PNG = r"C:\lab1\colors.raw"

RU_TXT   = r"C:\lab1\not_pic\haksli_-_o_divnyy_novyy_mir.txt"
ENVIK7   = r"C:\lab1\not_pic\enwik7"
BIN_FILE = r"C:\lab1\not_pic\tsetup-x64.6.6.2.exe"


if __name__ == '__main__':
    print("=" * 60)
    print("RAW ИЗОБРАЖЕНИЯ")
    print("=" * 60)
    full_roundtrip(RAW_BW_PNG,     Ms=1, Mc=1, label="BW raw (Ms=1)")
    full_roundtrip(RAW_GREY_PNG,   Ms=1, Mc=1, label="Grey raw (Ms=1)")
    full_roundtrip(RAW_COLORS_PNG, Ms=3, Mc=1, label="Color raw RGB (Ms=3)")

    print("=" * 60)
    print("ТЕКСТОВЫЕ ФАЙЛЫ")
    print("=" * 60)
    # Побайтовый RLE для сравнения
    full_roundtrip(RU_TXT, Ms=1, Mc=1, label="RU текст (Ms=1, побайтово)")
    # UTF-8 с паддингом
    full_roundtrip_utf8(RU_TXT, label="RU текст (UTF-8 паддинг, Ms=4)")

    print("=" * 60)
    print("БИНАРНЫЕ / ПРОЧИЕ ФАЙЛЫ")
    print("=" * 60)
    full_roundtrip(ENVIK7,   Ms=1, Mc=1, label="ENVIK7 (Ms=1)")
    full_roundtrip(BIN_FILE, Ms=1, Mc=1, label="EXE (Ms=1)")