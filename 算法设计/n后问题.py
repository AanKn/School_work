def solve_n_queens(n):
    board = [["O" for _ in range(n)] for _ in range(n)]
    result = []

    def backtrack(row, col, diag, anti_diag):
        if row == n:
            result.append(["".join(r) for r in board])
            return
        for j in range(n):
            if j not in col and row+j not in diag and row-j not in anti_diag:
                board[row][j] = "Q"
                col.add(j)
                diag.add(row+j)
                anti_diag.add(row-j)
                backtrack(row+1, col, diag, anti_diag)
                col.remove(j)
                diag.remove(row+j)
                anti_diag.remove(row-j)
                board[row][j] = "O"

    backtrack(0, set(), set(), set())
    return result

n = 4
solutions = solve_n_queens(n)
print(f"Found {len(solutions)} solutions for {n}-Queens problem:")
for solution in solutions:
    for row in solution:
        print(row)
    print()