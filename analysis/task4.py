import time
import os
from exercise1.rle import rle_encode, rle_decode, rle_encode_with_len
from exercise2.bwt import bwt_encode_block, bwt_decode_fast
from exercise2.mtf import mtf_encode, mtf_decode
from exercise2.huffman import huffman_encode, huffman_decode, build_huffman_tree
from exercise3.lzss import lzss_encode, lzss_decode
from exercise3.lz78_lzw import lzw_encode, lzw_decode

from exercise2.entropy import calculate_entropy


def compressor_huffman(data):
    encoded, tree = huffman_encode(data)  # распаковываем кортеж
    return encoded

def compressor_rle(data):
    return rle_encode(data)
    # return rle_encode_with_len(data)
    #


def compressor_bwt_rle(data, block_size=4096):
    """BWT + RLE с правильной обработкой блоков"""
    if not data:
        return b''

    result = bytearray()
    n = len(data)

    # заголовок: исходный размер и размер блока
    result.extend(n.to_bytes(4, 'little'))
    result.extend(block_size.to_bytes(4, 'little'))

    i = 0
    while i < n:
        # берем блок (последний может быть меньше)
        block = data[i:i + block_size]
        block_len = len(block)

        # BWT
        bwt_block, idx = bwt_encode_block(block)

        # RLE
        rle_block = rle_encode(bwt_block)

        # сохраняем: [BWT индекс (4)] [размер блока (4)] [размер RLE (4)] [RLE данные]
        result.extend(idx.to_bytes(4, 'little'))
        result.extend(block_len.to_bytes(4, 'little'))
        result.extend(len(rle_block).to_bytes(4, 'little'))
        result.extend(rle_block)

        i += block_size

    return bytes(result)


def compressor_bwt_mtf_huffman(data, block_size=4096):
    result = bytearray()
    i = 0
    n = len(data)

    while i < n:
        block = data[i:i + block_size]
        if len(block) < block_size:
            block = block + b'\x00' * (block_size - len(block))
        bwt_block, idx = bwt_encode_block(block)
        # сохраняем индекс (4 байта)
        result.extend(idx.to_bytes(4, 'little'))
        mtf_indices = mtf_encode(bwt_block)
        mtf_bytes = bytes(mtf_indices)

        # исправлено: распаковываем результат
        huff_encoded, tree = huffman_encode(mtf_bytes)
        result.extend(huff_encoded)
        i += block_size

    return bytes(result)


def compressor_bwt_mtf(data, block_size=4096):
    result = bytearray()
    i = 0
    n = len(data)

    while i < n:
        block = data[i:i + block_size]
        if len(block) < block_size:
            block = block + b'\x00' * (block_size - len(block))
        bwt_block, idx = bwt_encode_block(block)
        # cохр индекс (4 байта)
        result.extend(idx.to_bytes(4, 'little'))
        mtf_indices = mtf_encode(bwt_block)
        mtf_bytes = bytes(mtf_indices)
        huff_encoded = huffman_encode(mtf_bytes)
        result.extend(huff_encoded)
        i += block_size

    return bytes(result)


def compressor_bwt_mtf_rle_huffman(data, block_size=4096):
    result = bytearray()
    i = 0
    n = len(data)

    while i < n:
        block = data[i:i + block_size]
        if len(block) < block_size:
            block = block + b'\x00' * (block_size - len(block))
        bwt_block, idx = bwt_encode_block(block)
        result.extend(idx.to_bytes(4, 'little'))
        mtf_indices = mtf_encode(bwt_block)
        mtf_bytes = bytes(mtf_indices)
        rle_block = rle_encode(mtf_bytes)

        # исправлено: распаковываем результат
        huff_encoded, tree = huffman_encode(rle_block)
        result.extend(huff_encoded)
        i += block_size

    return bytes(result)

def compressor_lzss(data, window_size=4096):
    encoded = lzss_encode(data, window_size)
    return encoded



def compressor_lzss_huffman(data, window_size=4096):
    lzss_compressed = lzss_encode(data, window_size)
    # исправлено: распаковываем результат
    huff_compressed, tree = huffman_encode(lzss_compressed)
    return huff_compressed


def compressor_lzw(data, dict_size=4096):
    encoded, _ = lzw_encode(data, dict_size)
    return encoded


def compressor_lzw_huffman(data, dict_size=4096):
    lzw_compressed, _ = lzw_encode(data, dict_size)
    # исправлено: распаковываем результат
    huff_compressed, tree = huffman_encode(lzw_compressed)
    return huff_compressed


def get_file_size_mb(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def test_all_compressors(data, filename, description):
    print(f"файл: {filename}")
    print(f"описание: {description}")
    print(f"исходный размер: {get_file_size_mb(len(data))} ({len(data)} байт)")
    print(f"{'=' * 90}")

    compressors = [
        ("HA", compressor_huffman),
        ("RLE", compressor_rle),
        ("BWT + RLE", compressor_bwt_rle),

        ("BWT + MTF + HA", compressor_bwt_mtf_huffman),
        # ("BWT + MTF + HA", compressor_bwt_mtf),

        # ("BWT + MTF + HA", compressor_bwt_mtf_huffman),



        ("BWT + MTF + RLE + HA", compressor_bwt_mtf_rle_huffman),
        ("LZSS", compressor_lzss),
        ("LZSS + HA", compressor_lzss_huffman),
        ("LZW", compressor_lzw),
        ("LZW + HA", compressor_lzw_huffman),
    ]

    results = []
    entropy = calculate_entropy(data, 1)
    size = len(data)

    # if size < 1024:

    print(f"{filename:<25} {size:<15} {entropy:<12.4f}")
    print()

    print(f"\n{'компрессор':<25} {'сжатый размер':<18} {'коэффициент':<12} {'время(с)':<10}")
    print("-" * 75)

    for name, comp_func in compressors:
        start_time = time.time()
        compressed = comp_func(data)
        elapsed_time = time.time() - start_time

        compressed_size = len(compressed)
        ratio = compressed_size / len(data) if compressed_size > 0 else 0

        results.append({
            'name': name,
            'compressed_size': compressed_size,
            'ratio': ratio,
            'time': elapsed_time
        })

        size_str = get_file_size_mb(compressed_size)
        print(f"{name:<25} {size_str:<18} {ratio:<12.3f} {elapsed_time:<10.3f}")

    return results


def main():
    test_files = [

        #("bw.raw", "черно-белое изображение, 1200x800"),
        #("grey.raw", "изображение в оттенках серого, 1200x800"),
        ("color.raw", "цветное изображение, 800x600"),
        #(r"C:\Users\roman\PycharmProjects\algo_lab1\analysis\Haksli_200kb.txt", " текст"),
        #(r"C:\Users\roman\PycharmProjects\algo_lab1\analysis\part_1_1mb.exe", " файл .exe"),
        #("enwik7", "текстовый файл "),
    ]

    all_results = {}

    for filename, description in test_files:
        if not os.path.exists(filename):
            print(f"\nфайл {filename} не найден, пропуск")
            continue

        with open(filename, 'rb') as f:
            data = f.read()

        results = test_all_compressors(data, filename, description)
        all_results[filename] = results


if __name__ == "__main__":
    main()
