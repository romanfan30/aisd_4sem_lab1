"""
LZ77 и LZSS алгоритмы
задание 3, пункт 2.1-2.2
"""


def lz77_encode(data, buffer_size=4096):
    """LZ77 кодирование"""
    if not data:
        return b''

    result = bytearray()
    i = 0
    n = len(data)

    while i < n:
        best_offset = 0
        best_len = 0

        start = max(0, i - buffer_size)

        for offset in range(1, i - start + 1):
            length = 0
            while (i + length < n and
                   length < 255 and
                   data[i + length] == data[i - offset + length]):
                length += 1

            if length > best_len:
                best_len = length
                best_offset = offset

        if i + best_len < n:
            next_char = data[i + best_len]
        else:
            next_char = 0

        result.append((best_offset >> 8) & 0xFF)
        result.append(best_offset & 0xFF)
        result.append(best_len)
        result.append(next_char)

        i += best_len + 1

    return bytes(result)


def lz77_decode(data):
    """LZ77 декодирование"""
    if not data:
        return b''

    result = bytearray()
    i = 0
    n = len(data)

    while i + 3 < n:
        offset = (data[i] << 8) | data[i + 1]
        length = data[i + 2]
        next_char = data[i + 3]
        i += 4

        if length > 0:
            start = len(result) - offset
            for j in range(length):
                result.append(result[start + j])

        if next_char != 0:
            result.append(next_char)

    return bytes(result)



if __name__ == "__main__":
    test_data = b"abracadabra"
    print(f"\nисходные данные: {test_data.decode()}")
    print(f"размер: {len(test_data)} байт")

    encoded = lz77_encode(test_data, 256)
    print(f"\nLZ77 закодировано: {len(encoded)} байт")
    print(f"коэффициент сжатия: {len(test_data) / len(encoded):.2f}")

    decoded = lz77_decode(encoded)
    print(f"декодировано: {decoded.decode()}")
