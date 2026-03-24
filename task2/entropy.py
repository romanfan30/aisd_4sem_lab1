import math
from collections import Counter
import matplotlib.pyplot as plt


# -------------------------------
# 1. Энтропия при фиксированной длине символа
# -------------------------------
def entropy_by_symbol_size(data: bytes, ms: int) -> float:
    """
    data — байтовая строка
    ms — размер символа в байтах (1–4)
    """

    # разбиение на "символы" фиксированной длины
    symbols = [
        data[i:i + ms]
        for i in range(0, len(data), ms)
    ]

    # если последний кусок короче — убираем
    symbols = [s for s in symbols if len(s) == ms]

    total = len(symbols)
    if total == 0:
        return 0.0

    freq = Counter(symbols)

    H = 0.0
    for count in freq.values():
        p = count / total
        H -= p * math.log2(p)

    return H


# -------------------------------
# 2. Фильтрация ASCII (убираем Unicode > 127)
# -------------------------------
def filter_ascii(data: bytes) -> bytes:
    return bytes(b for b in data if b < 128)


# -------------------------------
# 3. Загрузка текста
# -------------------------------
def load_text(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


# -------------------------------
# 4. Основной эксперимент
# -------------------------------
def run_experiment(text_path: str):
    data = load_text(text_path)

    # фильтрация Unicode > 127
    data = filter_ascii(data)

    print(f"Размер после фильтрации: {len(data)} байт")

    ms_values = [1, 2, 3, 4]
    entropies = []

    for ms in ms_values:
        h = entropy_by_symbol_size(data, ms)
        entropies.append(h)
        print(f"ms={ms} байт -> H={h:.4f} бит/символ")

    # -------------------------------
    # 5. График
    # -------------------------------
    plt.figure(figsize=(8, 5))
    plt.plot(ms_values, entropies, marker='o')

    plt.title("Зависимость энтропии от длины символа")
    plt.xlabel("Длина символа (байт)")
    plt.ylabel("Энтропия (бит/символ)")
    plt.xticks(ms_values)
    plt.grid(True, alpha=0.3)

    plt.show()


# -------------------------------
# 6. Запуск
# -------------------------------
if __name__ == "__main__":
    # любой английский текстовый файл
    run_experiment("english_text.txt")