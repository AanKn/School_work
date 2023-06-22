c = 100
w = [12, 9, 56, 78, 55, 23]

# 按重量从小到大排序
w.sort()

# 贪心选择策略：每次选择最轻的集装箱装上船
count = 0
for i in range(len(w)):
    if c >= w[i]:
        c -= w[i]
        count += 1
    else:
        break

print(count)