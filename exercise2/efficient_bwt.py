"""
эффективное преобразование барроузауиллера (BWT)
на основе суффиксного массива.
"""

def build_suffix_array(data):
    n = len(data)

    # начальная сортировка по одному символу
    sa = list(range(n))
    rank = list(data)
    tmp = [0] * n

    k = 1

    while k < n:

        # сортировка по паре:
        # (rank[i], rank[i + k])
        sa.sort(
            key=lambda i: (
                rank[i],
                rank[i + k] if i + k < n else -1
            )
        )

        # пересчет классов эквивалентности
        tmp[sa[0]] = 0

        for i in range(1, n):

            prev = sa[i - 1]
            curr = sa[i]

            prev_rank = (
                rank[prev],
                rank[prev + k] if prev + k < n else -1
            )

            curr_rank = (
                rank[curr],
                rank[curr + k] if curr + k < n else -1
            )

            tmp[curr] = tmp[prev] + (prev_rank != curr_rank)

        rank[:] = tmp[:]

        # все ранги уникальны
        if rank[sa[-1]] == n - 1:
            break

        k *= 2

    return sa


def bwt_encode_suffix_array(data):
    if not data:
        return b'', 0

    n = len(data)

    # строим суффиксный массив
    sa = build_suffix_array(data)

    last_column = bytearray()
    primary_idx = 0

    for i, suffix_pos in enumerate(sa):

        # символ перед суффиксом
        last_column.append(data[suffix_pos - 1])

        # исходная строка соответствует суффиксу с позиции 0
        if suffix_pos == 0:
            primary_idx = i

    return bytes(last_column), primary_idx


if __name__ == "__main__":

    test_data = b"banana"

    print("исходные данные:", test_data)

    bwt_data, idx = bwt_encode_suffix_array(test_data)

    print("BWT:", bwt_data)
    print("индекс:", idx)
