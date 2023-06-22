from random import sample


def binarySearch(arr, target):
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (right + left) // 2
        if arr[mid] == target:
            x = []
            while arr[mid] == target:
                x.append(mid)
                mid += 1
            return x
        elif target > arr[mid]:
            left = mid + 1
        else:
            right = mid - 1
    return [right, left]


a = sorted([-56, -55, -22, -15, -9, -5, -4, 0, 0, 0, 5, 6, 8, 15, 56, 108])
print(a)
print(binarySearch(a, 0))

