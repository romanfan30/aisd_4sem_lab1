"""
задание 3: зависимость коэффициента сжатия от размера словаря (LZW)
"""

import matplotlib.pyplot as plt
import sys
sys.path.append('..')

from exercise3.lz78_lzw import lzw_encode


def analyze_lzw_dict_size(data, dict_sizes):
    """анализ зависимости коэффициента сжатия от размера словаря"""
    results = {'dict_sizes': [], 'compression_ratio': []}

    print(f"\n{'размер словаря':<15} {'коэффициент':<20}")
    print("-" * 40)

    for dict_size in dict_sizes:
        encoded, orig_len = lzw_encode(data, max_dict_size=dict_size)

        compressed_size = len(encoded)
        ratio = len(data) / compressed_size if compressed_size > 0 else 0

        results['dict_sizes'].append(dict_size)
        results['compression_ratio'].append(ratio)

        print(f"{dict_size:<15} {ratio:<20.3f}")

    return results


def plot_ratio_vs_dict_size(results):
    """график зависимости коэффициента сжатия от размера словаря"""
    plt.figure(figsize=(10, 6))

    plt.plot(results['dict_sizes'], results['compression_ratio'], 'orange', marker='o',linewidth=2, markersize=6)

    plt.xlabel('размер словаря', fontsize=12)
    plt.ylabel('коэффициент сжатия', fontsize=12)
    plt.title('зависимость коэффициента сжатия LZW от размера словаря', fontsize=14)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('lzw_dict_vs_ratio.png', dpi=150)
    plt.show()


def test_lzw_on_file(filepath, max_bytes=None):
    """тестирование на файле"""
    print(f"файл: {filepath}")

    with open(filepath, 'rb') as f:
        if max_bytes:
            data = f.read(max_bytes)
        else:
            data = f.read()

    print(f"загружено {len(data)} байт")

    dict_sizes = [256, 512, 1024, 2048, 4096, 8192, 16384]
    print("\nзадание 3: зависимость коэффициента сжатия от размера словаря (LZW)")

    results = analyze_lzw_dict_size(data, dict_sizes)
    plot_ratio_vs_dict_size(results)

    return results


if __name__ == "__main__":
    file_path = "enwik7"
    results = test_lzw_on_file(file_path, max_bytes=100 * 1024)
