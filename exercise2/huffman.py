"""
кодирование хаффмана
задание 2, пункт 1.4
"""


class HuffmanNode:
    def __init__(self, symbol=None, freq=0, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None


def build_huffman_tree(freqs):
    """построение дерева хаффмана"""
    nodes = []
    for symbol, freq in freqs.items():
        nodes.append(HuffmanNode(symbol=symbol, freq=freq))

    def sort_nodes(nodes):
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if nodes[i].freq > nodes[j].freq:
                    nodes[i], nodes[j] = nodes[j], nodes[i]
        return nodes

    while len(nodes) > 1:
        nodes = sort_nodes(nodes)
        left = nodes.pop(0)
        right = nodes.pop(0)
        parent = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        nodes.append(parent)

    return nodes[0] if nodes else None


def generate_codes(node, code="", codes=None):
    """генерация кодов хаффмана"""
    if codes is None:
        codes = {}

    if node.is_leaf():
        codes[node.symbol] = code
        return codes

    if node.left:
        generate_codes(node.left, code + "0", codes)
    if node.right:
        generate_codes(node.right, code + "1", codes)
    return codes


def huffman_encode(data):
    """кодирование хаффмана"""
    if not data:
        return b'', 0

    freqs = {}
    for byte in data:
        freqs[byte] = freqs.get(byte, 0) + 1

    tree = build_huffman_tree(freqs)
    codes = generate_codes(tree)

    bits = ""
    for byte in data:
        bits += codes[byte]

    padding = (8 - len(bits) % 8) % 8
    bits += "0" * padding

    encoded = bytearray()
    for i in range(0, len(bits), 8):
        byte_val = int(bits[i:i + 8], 2)
        encoded.append(byte_val)

    return bytes(encoded), padding


def huffman_decode(encoded_data, tree, padding):
    """декодирование хаффмана"""
    if not encoded_data:
        return b''

    bits = ""
    for byte in encoded_data:
        bits += format(byte, '08b')

    if padding > 0:
        bits = bits[:-padding]

    result = bytearray()
    node = tree

    for bit in bits:
        if bit == '0':
            node = node.left
        else:
            node = node.right

        if node.is_leaf():
            result.append(node.symbol)
            node = tree

    return bytes(result)


def arithmetic_encode(data):
    """арифметическое кодирование"""
    if not data:
        return 0.0, 0.0, 0, {}

    freqs = {}
    for b in data:
        freqs[b] = freqs.get(b, 0) + 1

    total = len(data)

    cum_probs = {}
    cum = 0.0
    for sym in sorted(freqs.keys()):
        prob = freqs[sym] / total
        cum_probs[sym] = (cum, cum + prob)
        cum += prob

    low = 0.0
    high = 1.0

    for b in data:
        range_width = high - low
        low_b, high_b = cum_probs[b]
        low = low + range_width * low_b
        high = low + range_width * (high_b - low_b)

    code = (low + high) / 2

    return code, low, high, len(data), cum_probs


def arithmetic_decode(code, low, high, data_len, cum_probs):
    """арифметическое декодирование"""
    result = bytearray()
    current_low = 0.0
    current_high = 1.0
    symbols = sorted(cum_probs.keys())

    for _ in range(data_len):
        range_width = current_high - current_low
        value = (low + high) / 2

        for sym in symbols:
            low_b, high_b = cum_probs[sym]
            sym_low = current_low + range_width * low_b
            sym_high = current_low + range_width * high_b

            if sym_low <= value < sym_high:
                result.append(sym)
                current_low = sym_low
                current_high = sym_high
                break

    return bytes(result)


if __name__ == "__main__":
    test_data = bytes([0x42, 0x41, 0x4E, 0x41, 0x4E, 0x41])
    encoded, padding = huffman_encode(test_data)
    freqs = {}
    for b in test_data:
        freqs[b] = freqs.get(b, 0) + 1
    tree = build_huffman_tree(freqs)
    decoded = huffman_decode(encoded, tree, padding)
    print(f"BANANA: вход={test_data}\nдекодировано={decoded}")
    print()

    print("арифметическое кодирование")
    test_arith = bytes([0x42, 0x41, 0x4E, 0x41, 0x4E, 0x41])
    code, low, high, data_len, cum_probs = arithmetic_encode(test_arith)
    print(f"code = {code:.20f}")
    print(f"low = {low:.20f}")
    print(f"high = {high:.20f}")

    decoded_arith = arithmetic_decode(code, low, high, data_len, cum_probs)
    print(f"декодировано: {decoded_arith}")
