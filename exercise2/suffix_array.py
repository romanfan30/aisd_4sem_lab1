"""
суффиксный массив для BWT
задание 3, пункт 1
"""


def build_suffix_array(data):
    """простое построение суффиксного массива"""
    n = len(data)
    suffixes = []

    for i in range(n):
        suffixes.append((data[i:], i))

    for i in range(n):
        for j in range(i + 1, n):
            if suffixes[i][0] > suffixes[j][0]:
                suffixes[i], suffixes[j] = suffixes[j], suffixes[i]

    suffix_array = [suffixes[i][1] for i in range(n)]
    return suffix_array


def suffix_array_to_bwt(suffix_array, original_data):
    """преобразование суффиксного массива в BWT"""
    if not suffix_array or not original_data:
        return b''

    n = len(original_data)
    result = bytearray()

    for i in range(n):
        pos = suffix_array[i]
        if pos == 0:
            result.append(original_data[n - 1])
        else:
            result.append(original_data[pos - 1])

    return bytes(result)


def build_suffix_array_manber_myers(data):
    """построение суффиксного массива алгоритмом манбера-майерса"""
    n = len(data)
    if n == 0:
        return []

    rank = [data[i] for i in range(n)]
    tmp = [0] * n
    sa = list(range(n))

    k = 1
    while True:
        sa.sort(key=lambda x: (rank[x], rank[x + k] if x + k < n else -1))

        tmp[sa[0]] = 0
        for i in range(1, n):
            prev = sa[i - 1]
            curr = sa[i]
            prev_val = rank[prev + k] if prev + k < n else -1
            curr_val = rank[curr + k] if curr + k < n else -1

            if rank[prev] == rank[curr] and prev_val == curr_val:
                tmp[curr] = tmp[prev]
            else:
                tmp[curr] = tmp[prev] + 1

        rank, tmp = tmp, rank

        if rank[sa[-1]] == n - 1:
            break
        k <<= 1

    return sa


def bwt_from_suffix_array(data, suffix_array):
    """BWT из суффиксного массива"""
    n = len(data)
    result = bytearray()

    for pos in suffix_array:
        if pos == 0:
            result.append(data[-1])
        else:
            result.append(data[pos - 1])

    return bytes(result)


def bwt_encode_effective(data):
    """эффективное BWT с использованием суффиксного массива"""
    if not data:
        return b'', 0

    suffix_array = build_suffix_array_manber_myers(data)
    bwt = bwt_from_suffix_array(data, suffix_array)

    for i, pos in enumerate(suffix_array):
        if pos == 0:
            index = i
            break

    return bwt, index


if __name__ == "__main__":
    data = bytes([0x62, 0x61, 0x6e, 0x61, 0x6e, 0x61])  # "banana"
    print(f"\nисходные данные: {' '.join(f'0x{b:02x}' for b in data)}")
    print(data.decode('ascii'))

    suffix_array = build_suffix_array(data)
    print(f"\nсуффиксный массив: {suffix_array}")

    bwt_result = suffix_array_to_bwt(suffix_array, data)
    print(f"BWT через суффиксный массив: {' '.join(f'0x{b:02x}' for b in bwt_result)}")
