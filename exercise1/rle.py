"""
RLE (Run-Length Encoding) - кодирование длин серий
задание 1, пункт 2
"""

def rle_encode(data):
    """базовое RLE кодирование с 8-битными кодами"""
    if not data:
        return b''

    result = bytearray()
    i = 0
    n = len(data)

    while i < n:
        run_len = 1
        while (i + run_len < n) and (data[i + run_len] == data[i]) and (run_len < 127):
            run_len += 1

        if run_len >= 3:
            result.append(run_len)
            result.append(data[i])
            i += run_len
        else:
            start = i
            while i < n:
                test_len = 1
                while (i + test_len < n) and (data[i + test_len] == data[i]) and (test_len <127):
                    test_len += 1

                if test_len >= 3:
                    break
                i += 1

            unique_len = i - start
            if unique_len > 0:
                if unique_len > 127:
                    unique_len = 127
                ctrl = 0x80 | unique_len
                result.append(ctrl)
                result.extend(data[start:i])

    return bytes(result)


def rle_decode(data):
    """базовое RLE декодирование"""
    if not data:
        return b''

    result = bytearray()
    i = 0
    n = len(data)

    while i < n:
        ctrl = data[i]
        i += 1
        length = ctrl & 0x7F

        if (ctrl & 0x80) == 0:
            if i >= n:
                break
            symbol = data[i]
            i += 1
            result.extend([symbol] * length)
        else:
            if i + length > n:
                break
            result.extend(data[i:i + length])
            i += length

    return bytes(result)


def rle_encode_with_len(data, ms=8, mc=8):
    """
    RLE кодирование с настраиваемой длиной символа и управляющего кода
    ms - длина кода символа в битах
    mc - длина управляющего символа в битах
    """
    if not data:
        return b''

    def bytes_to_symbols(data_bytes, ms_val):
        symbol_bytes = ms_val // 8
        symbols = []
        for idx in range(0, len(data_bytes), symbol_bytes):
            chunk = data_bytes[idx:idx + symbol_bytes]
            if len(chunk) < symbol_bytes:
                chunk = chunk + b'\x00' * (symbol_bytes - len(chunk))
            value = 0
            for j, b in enumerate(chunk):
                value |= (b << (8 * j))
            symbols.append(value)
        return symbols

    def symbols_to_bytes(symbols_list, ms_val):
        symbol_bytes = ms_val // 8
        result = bytearray()
        for sym in symbols_list:
            for i in range(symbol_bytes):
                result.append((sym >> (8 * i)) & 0xFF)
        return bytes(result)

    symbols = bytes_to_symbols(data, ms)
    result = bytearray()
    i = 0
    n = len(symbols)
    max_count = (1 << (mc - 1)) - 1

    while i < n:
        run_len = 1
        while (i + run_len < n) and (symbols[i + run_len] == symbols[i]) and (run_len <max_count):
            run_len += 1

        if run_len >= 2:
            result.append(run_len)
            sym_bytes = symbols_to_bytes([symbols[i]], ms)
            result.extend(sym_bytes)
            i += run_len
        else:
            start = i
            while i < n:
                test_len = 1
                while (i + test_len < n) and (symbols[i + test_len] == symbols[i]) and (test_len < max_count):
                    test_len += 1
                if test_len >= 3:
                    break
                i += 1

            unique_len = i - start
            if unique_len > 0:
                result.append(0x80 | unique_len)
                for k in range(start, i):
                    sym_bytes = symbols_to_bytes([symbols[k]], ms)
                    result.extend(sym_bytes)

    return bytes(result)


def rle_decode_with_len(data, ms=8, mc=8):
    """RLE декодирование с настраиваемой длиной символа"""
    if not data:
        return b''

    def symbols_to_bytes(symbols_list, ms_val):
        symbol_bytes = ms_val // 8
        result = bytearray()
        for sym in symbols_list:
            for i in range(symbol_bytes):
                result.append((sym >> (8 * i)) & 0xFF)
        return bytes(result)

    result_symbols = []
    i = 0
    n = len(data)
    symbol_bytes = ms // 8

    while i < n:
        ctrl = data[i]
        i += 1
        length = ctrl & 0x7F

        if (ctrl & 0x80) == 0:
            if i + symbol_bytes > n:
                break
            sym_bytes = data[i:i + symbol_bytes]
            i += symbol_bytes
            symbol = 0
            for j, b in enumerate(sym_bytes):
                symbol |= (b << (8 * j))
            result_symbols.extend([symbol] * length)
        else:
            for _ in range(length):
                if i + symbol_bytes > n:
                    break
                sym_bytes = data[i:i + symbol_bytes]
                i += symbol_bytes
                symbol = 0
                for j, b in enumerate(sym_bytes):
                    symbol |= (b << (8 * j))
                result_symbols.append(symbol)

    return symbols_to_bytes(result_symbols, ms)


if __name__ == "__main__":
    print("RLE с Ms и Mc")
    print("Ms=16")
    test_ms16 = bytes([0xCF, 0xCE, 0xCF, 0xCE, 0xCF, 0xCE])
    enc_ms16 = rle_encode_with_len(test_ms16, ms=16, mc=8)
    print(f"0x{' 0x'.join(f'{b:02X}' for b in test_ms16)} -> 0x{' 0x'.join(f'{b:02X}' for b in enc_ms16)}")
    dec_ms16 = rle_decode_with_len(enc_ms16, ms=16, mc=8)
    print(f"0x{' 0x'.join(f'{b:02X}' for b in enc_ms16)} -> 0x{' 0x'.join(f'{b:02X}' for b in dec_ms16)}")

    print("\nMs=24")
    test_ms24 = bytes([0xCF, 0xCE, 0xCF, 0xCF, 0xCE, 0xCF])
    enc_ms24 = rle_encode_with_len(test_ms24, ms=24, mc=8)
    print(f"0x{' 0x'.join(f'{b:02X}' for b in test_ms24)} -> 0x{' 0x'.join(f'{b:02X}' for b in enc_ms24)}")
    dec_ms24 = rle_decode_with_len(enc_ms24, ms=24, mc=8)
    print(f"0x{' 0x'.join(f'{b:02X}' for b in enc_ms24)} -> 0x{' 0x'.join(f'{b:02X}' for b in dec_ms24)}")
