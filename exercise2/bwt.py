"""
преобразование барроуза-уиллера (BWT)
задание 2, пункт 2
"""


def bwt_encode_block(data):
    """BWT кодирование с построением матрицы"""
    if not data:
        return b'', 0

    n = len(data)
    matrix = []
    for i in range(n):
        row = data[i:] + data[:i]
        matrix.append(row)

    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i] > matrix[j]:
                matrix[i], matrix[j] = matrix[j], matrix[i]

    last = bytearray()
    for row in matrix:
        last.append(row[-1])

    for i, row in enumerate(matrix):
        if row == data:
            idx = i
            break

    print(matrix)
    return bytes(last), idx


def bwt_decode_matrix(last, idx):
    """BWT декодирование через построение матрицы"""
    n = len(last)
    matrix = [bytearray() for _ in range(n)]

    for _ in range(n):
        for i in range(n):
            matrix[i].insert(0, last[i])
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i] > matrix[j]:
                    matrix[i], matrix[j] = matrix[j], matrix[i]

    return bytes(matrix[idx])


def bwt_decode_fast(last, idx):
    """BWT декодирование с использованием перестановки"""
    n = len(last)

    first = sorted(last)

    positions = [[] for _ in range(256)]
    for i, ch in enumerate(last):
        positions[ch].append(i)

    next_arr = [0] * n
    counts = [0] * 256
    for i, ch in enumerate(first):
        next_arr[i] = positions[ch][counts[ch]]
        counts[ch] += 1

    res = bytearray()
    curr = idx
    for _ in range(n):
        res.append(first[curr])
        curr = next_arr[curr]

    return bytes(res)


def compress_file(data, block_size=1024):
    """BWT + RLE с блочной обработкой"""
    from exercise1.rle import rle_encode

    if not data:
        return b''

    res = bytearray()
    n = len(data)

    res.append((block_size >> 0) & 0xFF)
    res.append((block_size >> 8) & 0xFF)
    res.append((block_size >> 16) & 0xFF)
    res.append((block_size >> 24) & 0xFF)

    i = 0
    while i < n:
        block = data[i:i + block_size]

        bwt_block, idx = bwt_encode_block(block)
        rle_block = rle_encode(bwt_block)

        res.append((idx >> 0) & 0xFF)
        res.append((idx >> 8) & 0xFF)
        res.append((idx >> 16) & 0xFF)
        res.append((idx >> 24) & 0xFF)

        rle_len = len(rle_block)
        res.append((rle_len >> 0) & 0xFF)
        res.append((rle_len >> 8) & 0xFF)
        res.append((rle_len >> 16) & 0xFF)
        res.append((rle_len >> 24) & 0xFF)

        res.extend(rle_block)

        i += block_size

    return bytes(res)


def decompress_file(data):
    """декодирование BWT + RLE"""
    from exercise1.rle import rle_decode

    if not data:
        return b''

    res = bytearray()
    i = 0

    block_size = (data[i] | (data[i + 1] << 8) | (data[i + 2] << 16) | (data[i + 3] << 24))
    i += 4

    while i < len(data):
        idx = (data[i] | (data[i + 1] << 8) | (data[i + 2] << 16) | (data[i + 3] << 24))
        i += 4

        rle_len = (data[i] | (data[i + 1] << 8) | (data[i + 2] << 16) | (data[i + 3] << 24))
        i += 4

        rle_block = data[i:i + rle_len]
        i += rle_len

        bwt_block = rle_decode(rle_block)
        block = bwt_decode_fast(bwt_block, idx)

        res.extend(block)

    return bytes(res)


def rle_encode_block(data):
    """RLE кодирование блока"""
    if not data:
        return b''

    res = bytearray()
    i = 0
    n = len(data)

    while i < n:
        j = i + 1
        while j < n and data[j] == data[i] and (j - i) < 127:
            j += 1

        run_len = j - i

        if run_len >= 3:
            res.append(run_len)
            res.append(data[i])
            i = j
        else:
            start = i
            while i < n and (i - start) < 127:
                k = i
                while k + 1 < n and data[k + 1] == data[k]:
                    k += 1
                if k - i + 1 >= 3:
                    break
                i += 1

            unique_len = i - start
            if unique_len > 0:
                res.append(0x80 | unique_len)
                res.extend(data[start:i])

    return bytes(res)


def rle_decode_block(data):
    """RLE декодирование блока"""
    if not data:
        return b''

    res = bytearray()
    i = 0
    n = len(data)

    while i < n:
        ctrl = data[i]
        i += 1
        length = ctrl & 0x7F

        if (ctrl & 0x80) == 0:
            if i >= n:
                break
            sym = data[i]
            i += 1
            res.extend([sym] * length)
        else:
            if i + length > n:
                break
            res.extend(data[i:i + length])
            i += length

    return bytes(res)


if __name__ == "__main__":
    test_data = bytes([0x62, 0x61, 0x6e, 0x61, 0x6e, 0x61])
    print(f"вход: {test_data.hex().upper()} ({test_data.decode()})")

    bwt_data, idx = bwt_encode_block(test_data)
    print(f"BWT: {bwt_data.hex().upper()} (индекс {idx})")

    decoded_matrix = bwt_decode_matrix(bwt_data, idx)
    print(f"обратное BWT (матрица): {decoded_matrix.hex().upper()}")

    decoded_fast = bwt_decode_fast(bwt_data, idx)
    print(f"обратное BWT (быстрое): {decoded_fast.hex().upper()}")
