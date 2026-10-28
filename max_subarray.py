"""实验二第一版：求非空连续子数组的最大和。"""

import sys


def max_subarray_sum(numbers: list[int]) -> int:
    """使用 Kadane 算法，时间 O(n)，辅助空间 O(1)。"""
    if not numbers:
        raise ValueError("数组不能为空")

    current_sum = best_sum = numbers[0]
    for index in range(1, len(numbers)):
        number = numbers[index]
        current_sum = max(number, current_sum + number)
        best_sum = max(best_sum, current_sum)
    return best_sum


def main() -> int:
    print("请输入数组长度 n：", flush=True)
    try:
        count = int(sys.stdin.readline())
        if count <= 0:
            raise ValueError("数组长度必须大于 0")
        print(f"请输入 {count} 个整数（同一行，以空格分隔）：", flush=True)
        numbers = [int(value) for value in sys.stdin.readline().split()]
        if len(numbers) != count:
            raise ValueError("实际输入个数与数组长度不一致")
        print(f"最大子数组和：{max_subarray_sum(numbers)}")
        return 0
    except ValueError as error:
        print(f"输入错误：{error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
