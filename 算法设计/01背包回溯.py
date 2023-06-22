def knapsack_01(values, weights, capacity):
    n = len(values)
    max_value = -1

    def backtrack(i, curr_weight, curr_value):
        nonlocal max_value
        if curr_weight > capacity:
            return
        if i == n:
            max_value = max(max_value, curr_value)
            return
        # 不选择第i个物品
        backtrack(i + 1, curr_weight, curr_value)
        # 选择第i个物品
        backtrack(i + 1, curr_weight + weights[i], curr_value + values[i])

    backtrack(0, 0, 0)
    return max_value
values = [60, 100, 120]
weights = [10, 20, 30]
capacity = 50
max_value = knapsack_01(values, weights, capacity)
print(f"The maximum value in knapsack is {max_value}")