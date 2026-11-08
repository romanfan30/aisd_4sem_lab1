"""
задание 2: зависимость коэффициента сжатия от размера буфера (LZSS)
"""

import time
import matplotlib.pyplot as plt
import sys
sys.path.append('..')

from exercise3.lzss import lzss_encode


def analyze_lzss_buffer_size(data, buffer_sizes):
    """анализ зависимости коэффициента сжатия от размера буфера"""
    results = {'buffer_sizes': [], 'compression_ratio': [], 'time': []}

    print(f"\n{'размер буфера':<15} {'коэффициент':<15} {'время (с)':<10}")
    print("-" * 45)

    for buffer_size in buffer_sizes:
        start_time = time.time()
        encoded, _ = lzss_encode(data, window_size=buffer_size)
        elapsed_time = time.time() - start_time

        compressed_size = len(encoded)
        ratio = len(data) / compressed_size if compressed_size > 0 else 0

        results['buffer_sizes'].append(buffer_size)
        results['compression_ratio'].append(ratio)
        results['time'].append(elapsed_time)

        print(f"{buffer_size:<15} {ratio:<15.3f} {elapsed_time:<10.4f}")

    return results


def plot_lzss_buffer(results):
    """график зависимости коэффициента сжатия от размера буфера"""
    plt.figure(figsize=(10, 6))

    plt.plot(results['buffer_sizes'], results['compression_ratio'], 'b-o', linewidth=2,markersize=6)

    plt.xlabel('размер буфера (байт)', fontsize=12)
    plt.ylabel('коэффициент сжатия', fontsize=12)
    plt.title('зависимость коэффициента сжатия LZSS от размера буфера', fontsize=14)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('lzss_buffer_vs_ratio.png', dpi=150)
    plt.show()


def test_lzss_on_file(filepath, max_bytes=None):
    """тестирование на файле"""
    print(f"файл: {filepath}")

    with open(filepath, 'rb') as f:
        if max_bytes:
            data = f.read(max_bytes)
        else:
            data = f.read()

    print(f"загружено {len(data)} байт")

    buffer_sizes = [256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
    print("\nзадание 2: зависимость коэффициента сжатия от размера буфера (LZSS)")

    results = analyze_lzss_buffer_size(data, buffer_sizes)
    plot_lzss_buffer(results)

    return results


if __name__ == "__main__":
    file_path = "enwik7"
    results = test_lzss_on_file(file_path, max_bytes=100 * 1024)
