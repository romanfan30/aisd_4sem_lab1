"""
LZ78 и LZW алгоритмы
задание 3, пункт 2.3-2.4
"""


def lz78_encode(data, max_dict_size=4096):
    """LZ78 кодирование"""
    if not data:
        return b'', 0

    dictionary = {}
    dict_size = 1
    result = bytearray()
    i = 0
    n = len(data)

    while i < n:
        current = b''
        idx = 0
        j = i

        while j < n:
            candidate = current + bytes([data[j]])
            if candidate in dictionary:
                current = candidate
                idx = dictionary[current]
                j += 1
            else:
                break

        if current:
            if j >= n:
                result.append((idx >> 8) & 0xFF)
                result.append(idx & 0xFF)
                result.append(0)
                i = j
            else:
                next_char = data[j]
                result.append((idx >> 8) & 0xFF)
                result.append(idx & 0xFF)
                result.append(next_char)

                new_phrase = current + bytes([next_char])
                if dict_size < max_dict_size and new_phrase not in dictionary:
                    dictionary[new_phrase] = dict_size
                    dict_size += 1

                i = j + 1
        else:
            result.append(0)
            result.append(0)
            result.append(data[i])

            if dict_size < max_dict_size and bytes([data[i]]) not in dictionary:
                dictionary[bytes([data[i]])] = dict_size
                dict_size += 1

            i += 1

    return bytes(result), len(data)


def lz78_decode(data, orig_len, max_dict_size=4096):
    """LZ78 декодирование"""
    if not data:
        return b''

    dictionary = {}
    dict_size = 1
    result = bytearray()
    i = 0
    n = len(data)

    while i + 2 < n and len(result) < orig_len:
        idx = (data[i] << 8) | data[i + 1]
        next_char = data[i + 2]
        i += 3

        if idx == 0:
            if next_char == 0:
                continue
            phrase = bytes([next_char])
        else:
            if idx in dictionary:
                phrase = dictionary[idx] + bytes([next_char]) if next_char != 0 else dictionary[idx]
            else:
                phrase = bytes([next_char]) if next_char != 0 else b''

        if len(phrase) == 0:
            continue

        if len(result) + len(phrase) > orig_len:
            phrase = phrase[:orig_len - len(result)]

        result.extend(phrase)

        if dict_size < max_dict_size and idx != 0:
            dictionary[dict_size] = phrase
            dict_size += 1
        elif dict_size < max_dict_size and idx == 0 and next_char != 0:
            if bytes([next_char]) not in dictionary.values():
                dictionary[dict_size] = bytes([next_char])
                dict_size += 1

    return bytes(result)


def lzw_encode(data, max_dict_size=4096):
    """LZW кодирование"""
    if not data:
        return b'', 0

    dictionary = {}
    for i in range(256):
        dictionary[bytes([i])] = i

    dict_size = 256
    result = bytearray()
    current = b''

    for byte in data:
        current_byte = bytes([byte])
        new_phrase = current + current_byte

        if new_phrase in dictionary:
            current = new_phrase
        else:
            code = dictionary[current]
            result.append((code >> 8) & 0xFF)
            result.append(code & 0xFF)

            if dict_size < max_dict_size:
                dictionary[new_phrase] = dict_size
                dict_size += 1

            current = current_byte

    if current:
        code = dictionary[current]
        result.append((code >> 8) & 0xFF)
        result.append(code & 0xFF)

    return bytes(result), len(data)


def lzw_decode(data, max_dict_size=4096):
    """LZW декодирование"""
    if not data:
        return b''

    dictionary = {}
    for i in range(256):
        dictionary[i] = bytes([i])

    dict_size = 256
    result = bytearray()

    i = 0
    n = len(data)

    if i + 1 >= n:
        return b''
    code = (data[i] << 8) | data[i + 1]
    i += 2

    if code not in dictionary:
        return b''

    current = dictionary[code]
    result.extend(current)

    while i + 1 < n:
        code = (data[i] << 8) | data[i + 1]
        i += 2

        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            entry = current + bytes([current[0]])
        else:
            break

        result.extend(entry)

        if dict_size < max_dict_size:
            dictionary[dict_size] = current + bytes([entry[0]])
            dict_size += 1

        current = entry

    return bytes(result)


if __name__ == "__main__":
    print("LZ78")
    test_data = b"abracadabra"
    encoded, orig_len = lz78_encode(test_data)
    decoded = lz78_decode(encoded, orig_len)
    print(f"исходные: {test_data.decode()}")
    print(f"закодировано: {len(encoded)} байт")
    print(f"декодировано: {decoded.decode()}")
