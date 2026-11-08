"""
Move-To-Front (MTF) преобразование
задание 2, пункт 1.3
"""


def mtf_encode(data):
    """MTF кодирование"""
    if not data:
        return []

    symbols = list(range(256))
    result = []

    for byte in data:
        pos = symbols.index(byte)
        result.append(pos)

        symbols.pop(pos)
        symbols.insert(0, byte)

    return result


def mtf_decode(indices):
    """MTF декодирование"""
    if not indices:
        return b''

    symbols = list(range(256))
    result = bytearray()

    for idx in indices:
        byte = symbols[idx]
        result.append(byte)

        symbols.pop(idx)
        symbols.insert(0, byte)

    return bytes(result)


def mtf_encode_utf8(text):
    """MTF кодирование для UTF-8 текста"""
    codepoints = [ord(ch) for ch in text]
    symbols = []
    result = []

    for code in codepoints:
        if code in symbols:
            pos = symbols.index(code)
        else:
            symbols.append(code)
            pos = len(symbols) - 1

        result.append(pos)
        symbols.pop(pos)
        symbols.insert(0, code)

    return result


if __name__ == "__main__":
    test_data = bytes([0x42, 0x41, 0x4E, 0x41, 0x4E, 0x41])  # BANANA
    encoded = mtf_encode(test_data)
    decoded = mtf_decode(encoded)
    print(f"вход: {test_data}")
    print(f"выход MTF: {encoded}")
    print(f"декодировано: {decoded}")

    print()
    test_data2 = bytes([0x41, 0x41, 0x41, 0x41, 0x41, 0x42, 0x42, 0x42, 0x42, 0x42])
    encoded2 = mtf_encode(test_data2)
    decoded2 = mtf_decode(encoded2)
    print(f"вход: {test_data2}")
    print(f"выход MTF: {encoded2}")
    print(f"декодировано: {decoded2}")
