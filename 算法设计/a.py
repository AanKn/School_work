
import heapq
# 定义生成哈夫曼编码的函数
def generate_huffman_codes(freq):
    heap = [[weight, [symbol, '']] for symbol, weight in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        low = heapq.heappop(heap)
        high = heapq.heappop(heap)
        for pair in low[1:]:
            pair[1] = '0' + pair[1]
        for pair in high[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [low[0] + high[0]] + low[1:] + high[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

# 定义生成斐波那契数列的函数
def generate_fibonacci_sequence(n):
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    return sequence

# 定义生成频率字典的函数
def generate_frequency_dict(n):
    freq = {}
    fibonacci_sequence = generate_fibonacci_sequence(n)
    for i in range(n):
        freq[chr(ord('a') + i)] = fibonacci_sequence[i]
    return freq

# 生成前8个字符的频率字典
freq = generate_frequency_dict(8)

# 生成前8个字符的哈夫曼编码
huffman_codes = generate_huffman_codes(freq)

# 打印前8个字符的哈夫曼编码
for symbol, code in huffman_codes:
    print(f"{symbol}: {code}")

# 生成前n个字符的频率字典
n = 10
freq = generate_frequency_dict(n)

# 生成前n个字符的哈夫曼编码
huffman_codes = generate_huffman_codes(freq)

# 打印前n个字符的哈夫曼编码
for symbol, code in huffman_codes:
    print(f"{symbol}: {code}")
