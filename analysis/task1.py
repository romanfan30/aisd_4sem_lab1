"""
задание 1: зависимость энтропии от размера блока (BWT + MTF)
"""

import time
import matplotlib.pyplot as plt
import sys
sys.path.append('..')

from exercise2.bwt import bwt_encode_block
from exercise2.mtf import mtf_encode
from exercise2.entropy import calculate_entropy


def bwt_mtf_block(data, block_size):
    """применение BWT + MTF с блочной обработкой"""
    result = bytearray()
    n = len(data)
    i = 0

    while i < n:
        block = data[i:i + block_size]
        bwt_block, _ = bwt_encode_block(block)
        mtf_indices = mtf_encode(bwt_block)
        result.extend(mtf_indices)
        i += block_size
    return bytes(result)


def analyze_bwt_mtf_entropy(data, block_sizes):
    """анализ энтропии после BWT + MTF"""
    results = {'block_sizes': [], 'entropy': []}

    print(f"\n{'размер блока':<15} {'энтропия':<12}")
    print("-" * 30)

    for block_size in block_sizes:
        transformed_data = bwt_mtf_block(data, block_size)
        entropy_after = calculate_entropy(transformed_data, 1)

        results['block_sizes'].append(block_size)
        results['entropy'].append(entropy_after)

        print(f"{block_size:<15} {entropy_after:<12.4f}")

    return results


def plot_entropy_vs_block_size(results, original_entropy):
    """график зависимости энтропии от размера блока"""
    plt.figure(figsize=(10, 6))

    plt.plot(results['block_sizes'], results['entropy'], 'b-o', linewidth=2, markersize=6)
    plt.axhline(y=original_entropy, color='r', linestyle='--', label=f'исходная энтропия:{original_entropy:.4f}')

    plt.xlabel('размер блока (байт)', fontsize=12)
    plt.ylabel('энтропия (бит/символ)', fontsize=12)
    plt.title('зависимость энтропии от размера блока (BWT + MTF)', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('entropy_vs_block_size.png', dpi=150)
    plt.show()


def test_on_file(filepath, max_bytes=None):
    """тестирование на файле"""
    print(f"файл: {filepath}")

    with open(filepath, 'rb') as f:
        if max_bytes:
            data = f.read(max_bytes)
        else:
            data = f.read()

    print(f"загружено {len(data)} байт")

    block_sizes = [64, 128, 256, 512, 1024, 2048, 4096, 8192]
    print("\nзадание 1: зависимость энтропии от размера блока (BWT + MTF)")

    original_entropy = calculate_entropy(data, 1)
    print(f"исходная энтропия: {original_entropy:.4f}")

    results = analyze_bwt_mtf_entropy(data, block_sizes)
    plot_entropy_vs_block_size(results, original_entropy)

    return results


if __name__ == "__main__":
    file_path = "enwik7"
    results = test_on_file(file_path, max_bytes=100 * 1024)
