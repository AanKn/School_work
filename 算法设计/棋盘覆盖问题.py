def chess(tr, tc, pr, pc, size):
    global mark
    global table
    if size == 1:
        return
    mark += 1
    count = mark
    half = size // 2
    if (pr < tr + half) and (pc < tc + half):
        chess(tr, tc, pr, pc, half)
    else:
        table[tr + half - 1][tc + half - 1] = count
        chess(tr, tc, tr + half - 1, tc + half - 1, half)
    if (pr < tr + half) and (pc >= tc + half):
        chess(tr, tc + half, pr, pc, half)
    else:
        table[tr + half - 1][tc + half] = count
        chess(tr, tc + half, tr + half - 1, tc + half, half)
    if (pr >= tr + half) and (pc < tc + half):
        chess(tr + half, tc, pr, pc, half)
    else:
        table[tr + half][tc + half - 1] = count
        chess(tr + half, tc, tr + half, tc + half - 1, half)
    if (pr >= tr + half) and (pc >= tc + half):
        chess(tr + half, tc + half, pr, pc, half)
    else:
        table[tr + half][tc + half] = count
        chess(tr + half, tc + half, tr + half, tc + half, half)


def show(table):
    n = len(table)
    for i in range(n):
        for j in range(n):
            print(table[i][j], end='	')
        print('')


mark = 0
n = 8
table = [[-1 for x in range(n)] for y in range(n)]
chess(0, 0, 2, 2, n)
show(table)

