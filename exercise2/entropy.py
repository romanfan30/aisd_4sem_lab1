"""
расчет энтропии сообщения
задание 2, пункт 1.1
"""

import math
import matplotlib.pyplot as plt


def calculate_entropy(data, symbol_bytes=1):
    """
    расчет энтропии сообщения
    data: байтовая строка
    symbol_bytes: длина кода символа в байтах
    """
    if not data:
        return 0

    n = len(data)
    symbols = []
    for i in range(0, n, symbol_bytes):
        chunk = data[i:i + symbol_bytes]
        if len(chunk) < symbol_bytes:
            chunk = chunk + b'\x00' * (symbol_bytes - len(chunk))
        symbols.append(chunk)

    freq = {}
    for sym in symbols:
        if sym in freq:
            freq[sym] += 1
        else:
            freq[sym] = 1
    total = len(symbols)

    entropy = 0
    for count in freq.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy


def analyze_entropy_by_symbol_len(data, symbol_bytes_list):
    """анализ зависимости энтропии от длины символа"""
    results = {'symbol_bytes': symbol_bytes_list, 'entropy': []}

    for sb in symbol_bytes_list:
        entropy = calculate_entropy(data, sb)
        results['entropy'].append(entropy)
        print(f"длина символа: {sb} байт  энтропия: {entropy:.4f} бит/символ")

    return results


def plot_entropy_vs_symbol_len(results):
    """график зависимости энтропии от длины символа"""
    plt.figure(figsize=(10, 6))
    plt.plot(results['symbol_bytes'], results['entropy'], 'bo-', linewidth=2, markersize=8)
    plt.xlabel('длина символа (байт)', fontsize=12)
    plt.ylabel('энтропия (бит/символ)', fontsize=12)
    plt.title('зависимость энтропии от длины кода символа', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xticks(results['symbol_bytes'])

    for i, (x, y) in enumerate(zip(results['symbol_bytes'], results['entropy'])):
        plt.annotate(f'{y:.4f}', (x, y), textcoords="offset points",
                     xytext=(0, 10), ha='center', fontsize=10)

    plt.tight_layout()
    plt.show()


def test_entropy_for_english_text():
    """тест энтропии для английского текста"""
    english_text = """

When he was nearly thirteen, my brother Jem got his arm badly broken at the elbow. When it healed, and Jems fears of never being able to play football were assuaged,he was seldom self-conscious about his injury. His left arm was somewhat shorterthan his right; when he stood or walked, the back of his hand was at right angles to his body,his thumb parallel to his thigh. He couldnt have cared less, so long as he couldpass and punt.

When enough years had gone by to enable us to look back on them, we sometimes discussed the events leading to his accident. I maintain that the Ewells started itall, but Jem, who was four years my senior, said it started long before that. He saidit began the summer Dill came to us, when Dill first gave us the idea of making Boo Radleycome out.

I said if he wanted to take a broad view of the thing, it really began with Andrew Jackson.If General Jackson hadnt run the Creeks up the creek, Simon Finchw ouldnever have paddled up the Alabama, and where would we be if he hadnt? We were fartoo old to settle an argument with a fist-fight, so we consulted Atticus. Our father saidwe were both right.

Being Southerners, it was a source of shame to some members of the family that we had no recorded ancestors on either side of the Battle of Hastings. All we hadwas Simon Finch,a fur-trapping apothecary from Cornwall whose piety was exceeded onlyby his stinginess.In England, Simon was irritated by the persecution of those who calledthemselves Methodists at the hands of their more liberal brethren, and as Simoncalled himself a Methodist, he worked his way across the Atlantic to Philadelphia, thenceto Jamaica,thence to Mobile, and up the Saint Stephens. Mindful of John Wesleysstrictures on the use of many words in buying and selling, Simon made a pile practicingmedicine, but in this pursuit he was unhappy lest he be tempted into doing what he knewwas not for the glory of God, as the putting on of gold and costly apparel. So Simon,having forgotten his teachers dictum on the possession of human chattels, bought threeslaves and with their aid established a homestead on the banks of the Alabama River someforty miles above Saint Stephens. He returned to Saint Stephens only once, to finda wife, and with her established a line that ran high to daughters. Simon lived toa nimpressive age and died rich.
    """

    cleaned_text = ''.join([c for c in english_text if ord(c) < 128])
    data = cleaned_text.encode('ascii')

    print(f"английский текст из {len(cleaned_text)} символов")

    symbol_bytes_list = [1, 2, 3, 4]

    results = analyze_entropy_by_symbol_len(data, symbol_bytes_list)
    plot_entropy_vs_symbol_len(results)


if __name__ == "__main__":
    test_data = b"abracadabra"
    entropy = calculate_entropy(test_data, 1)
    print(f"энтропия 'abracadabra': {entropy:.4f}")
    print()

    test_entropy_for_english_text()
