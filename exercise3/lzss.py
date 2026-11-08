def lzss_encode(data, window_size=4096):
    """LZSS кодирование"""
    if not data:
        return b'', 0

    output_bits = []
    output_bytes = []
    i = 0
    n = len(data)

    while i < n:
        search_start = max(0, i - window_size)
        best_len = 0
        best_pos = 0

        for pos in range(search_start, i):
            length = 0
            while (i + length < n and
                   length < 255 and
                   data[pos + length] == data[i + length]):
                length += 1

            if length > best_len:
                best_len = length
                best_pos = i - pos

        if best_len >= 3:
            output_bits.append(1)
            output_bytes.append((best_pos >> 8) & 0xFF)
            output_bytes.append(best_pos & 0xFF)
            output_bytes.append(best_len)
            i += best_len
        else:
            output_bits.append(0)
            output_bytes.append(data[i])
            i += 1

    packed_flags = bytearray()
    for j in range(0, len(output_bits), 8):
        byte = 0
        for k in range(8):
            if j + k < len(output_bits) and output_bits[j + k]:
                byte |= (1 << (7 - k))
        packed_flags.append(byte)

    result = bytearray()
    result.append((len(packed_flags) >> 8) & 0xFF)
    result.append(len(packed_flags) & 0xFF)
    result.extend(packed_flags)
    result.extend(output_bytes)

    return bytes(result), len(data)


def lzss_decode(data, orig_len, window_size=4096):
    """LZSS декодирование"""
    if not data:
        return b''

    flags_len = (data[0] << 8) | data[1]
    flags_data = data[2:2 + flags_len]
    bytes_data = data[2 + flags_len:]

    flags = []
    for byte in flags_data:
        for i in range(8):
            flags.append((byte >> (7 - i)) & 1)

    result = bytearray()
    byte_pos = 0

    for flag in flags:
        if len(result) >= orig_len:
            break

        if flag == 0:
            if byte_pos >= len(bytes_data):
                break
            result.append(bytes_data[byte_pos])
            byte_pos += 1
        else:
            if byte_pos + 2 >= len(bytes_data):
                break
            offset = (bytes_data[byte_pos] << 8) | bytes_data[byte_pos + 1]
            length = bytes_data[byte_pos + 2]
            byte_pos += 3

            start = len(result) - offset
            if start < 0:
                start = 0

            for j in range(length):
                if len(result) >= orig_len:
                    break
                result.append(result[start + j])

    return bytes(result)


if __name__ == "__main__":
    test1 = b"abracadabra"
    print(f"Test1: {test1.decode()}")

    enc1, orig1 = lzss_encode(test1)
    dec1 = lzss_decode(enc1, orig1)

    print(f"размер: исходный={len(test1)}, сжатый={len(enc1)}, коэфф={len(test1)/len(enc1):.2f}")
    print(f"декодировано верно: {test1 == dec1}")

    test2 = b"aaaaabbbbbcccccaaaaabbbbb"
    print(f"\nTest2: {test2.decode()}")

    enc2, orig2 = lzss_encode(test2)
    dec2 = lzss_decode(enc2, orig2)

    print(f"размер: исходный={len(test2)}, сжатый={len(enc2)}, коэфф={len(test2)/len(enc2):.2f}")
    print(f"декодировано верно: {test2 == dec2}")

    print()

    test3 = bytes([0]) * 1000
    enc3, orig3 = lzss_encode(test3)
    dec3 = lzss_decode(enc3, orig3)

    print(f"1000 нулей: сжатый размер={len(enc3)}, коэфф={len(test3)/len(enc3):.2f}")
    print(f"декодировано верно: {test3 == dec3}")
