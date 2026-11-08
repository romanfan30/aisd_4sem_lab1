"""
канонические коды хаффмана
задание 4, пункт 2
"""


def build_huffman_freqs(data):
    """построение частот символов"""
    freqs = {}
    for byte in data:
        freqs[byte] = freqs.get(byte, 0) + 1
    return freqs


def build_huffman_tree(freqs):
    """построение дерева хаффмана"""
    nodes = []
    for symbol, freq in freqs.items():
        nodes.append([freq, symbol, None, None])

    while len(nodes) > 1:
        nodes.sort(key=lambda x: x[0])
        left = nodes.pop(0)
        right = nodes.pop(0)
        parent = [left[0] + right[0], None, left, right]
        nodes.append(parent)

    return nodes[0] if nodes else None


def get_code_lengths(node, depth=0, lengths=None):
    """получение длин кодов хаффмана"""
    if lengths is None:
        lengths = {}

    if node[1] is not None:
        lengths[node[1]] = depth
    else:
        if node[2]:
            get_code_lengths(node[2], depth + 1, lengths)
        if node[3]:
            get_code_lengths(node[3], depth + 1, lengths)

    return lengths


def build_can_codes(code_lengths):
    """построение канонических кодов по длинам"""
    symbols = sorted(code_lengths.items(), key=lambda x: (x[1], x[0]))

    codes = {}
    current_code = 0
    current_len = symbols[0][1]

    for symbol, length in symbols:
        if length > current_len:
            current_code <<= (length - current_len)
            current_len = length

        code_bits = bin(current_code)[2:].zfill(length)
        codes[symbol] = code_bits
        current_code += 1

    return codes


def can_huffman_encode(data):
    """кодирование каноническими кодами хаффмана"""
    if not data:
        return b'', {}, 0

    freqs = build_huffman_freqs(data)
    tree = build_huffman_tree(freqs)
    code_lengths = get_code_lengths(tree)
    codes = build_can_codes(code_lengths)

    bits = ""
    for byte in data:
        bits += codes[byte]

    padding = (8 - len(bits) % 8) % 8
    bits += "0" * padding

    encoded = bytearray()
    for i in range(0, len(bits), 8):
        encoded.append(int(bits[i:i + 8], 2))

    return bytes(encoded), code_lengths, padding


def can_huffman_decode(encoded_data, code_lengths, padding, data_len):
    """декодирование канонических кодов хаффмана"""
    if not encoded_data:
        return b''

    codes = build_can_codes(code_lengths)
    reverse_codes = {v: k for k, v in codes.items()}

    bits = ""
    for byte in encoded_data:
        bits += format(byte, '08b')

    if padding > 0:
        bits = bits[:-padding]

    result = bytearray()
    current_code = ""

    for bit in bits:
        current_code += bit
        if current_code in reverse_codes:
            result.append(reverse_codes[current_code])
            current_code = ""

    return bytes(result)


def save_canonical_huffman(data, output_path):
    """сохранение канонически закодированных данных"""
    if not data:
        return 0, 0

    encoded, code_lengths, padding = can_huffman_encode(data)

    with open(output_path, 'wb') as f:
        f.write(len(code_lengths).to_bytes(4, 'little'))
        for symbol, length in sorted(code_lengths.items()):
            f.write(symbol.to_bytes(1, 'little'))
            f.write(length.to_bytes(1, 'little'))
        f.write(padding.to_bytes(1, 'little'))
        f.write(len(data).to_bytes(4, 'little'))
        f.write(encoded)

    return len(data), len(encoded) + 4 + 2 * len(code_lengths) + 1 + 4


def load_canonical_huffman(input_path):
    """загрузка канонически закодированных данных"""
    with open(input_path, 'rb') as f:
        num_symbols = int.from_bytes(f.read(4), 'little')
        code_lengths = {}
        for _ in range(num_symbols):
            symbol = f.read(1)[0]
            length = f.read(1)[0]
            code_lengths[symbol] = length
        padding = f.read(1)[0]
        data_len = int.from_bytes(f.read(4), 'little')
        encoded = f.read()

    return can_huffman_decode(encoded, code_lengths, padding, data_len)


if __name__ == "__main__":
    test1 = b"abracadabra"
    print(test1.decode())
    print(f"размер: {len(test1)} байт")
    encoded1, lengths1, padding1 = can_huffman_encode(test1)
    print(f"сжатый размер: {len(encoded1)} байт")
    print(f"коэффициент: {len(test1) / len(encoded1):.2f}")
    print(f"метаданные (длины кодов): {dict(sorted(lengths1.items()))}")
    decoded1 = can_huffman_decode(encoded1, lengths1, padding1, len(test1))
    print(f"верно: {test1 == decoded1}")
