from random import sample
count = 0

def mao_pao(num_list):
    global count
    num_len = len(num_list)
    for j in range(num_len):
        for i in range(num_len - 1 - j):
            count += 1
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]


if __name__ == '__main__':
    a = sample([i for i in range(-1000, 1000)], 100)
    print("长度为100的数组为：", a)
    mao_pao(a)
    print("最大值为：%d" % a[0])
    print("最小值为：%d" % a[-1])
    print("比较次数为：%d" % count)