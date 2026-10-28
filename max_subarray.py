"""实验二第二版：求最大子数组和，并输出子数组位置与内容。

最大子数组必须连续且非空。并列时，先选起点较小的子数组；
起点也相同时，再选终点较小的子数组。
"""

from dataclasses import dataclass
import sys


@dataclass(frozen=True)
class SubarrayResult:
    """计算结果。left 和 right 为从 0 开始、两端都包含的下标。"""

    total: int
    left: int
    right: int


def max_subarray(numbers: list[int]) -> SubarrayResult:
    """Kadane 算法：时间 O(n)，辅助空间 O(1)，不修改输入数组。"""
    if not numbers:
        raise ValueError("数组不能为空")

    current_sum = best_sum = numbers[0]
    current_left = best_left = best_right = 0

    for index in range(1, len(numbers)):
        number = numbers[index]
        # 前一段和为 0 时继续延长，以保留更早的起点。
        if current_sum < 0:
            current_sum = number
            current_left = index
        else:
            current_sum += number

        # 按右端点递增扫描；和、起点都相同的情况保留已有结果。
        if current_sum > best_sum or (
            current_sum == best_sum and current_left < best_left
        ):
            best_sum = current_sum
            best_left = current_left
            best_right = index

    return SubarrayResult(best_sum, best_left, best_right)


def max_subarray_sum(numbers: list[int]) -> int:
    """保留第一版的函数接口，只返回最大和。"""
    return max_subarray(numbers).total


def parse_count(text: str) -> int:
    """解析第一行的数组长度。"""
    try:
        count = int(text.strip())
    except ValueError:
        raise ValueError("数组长度必须是整数") from None
    if count <= 0:
        raise ValueError("数组长度必须大于 0")
    return count


def parse_numbers(text: str, count: int) -> list[int]:
    """解析第二行，要求恰好包含 count 个整数。"""
    tokens = text.split()
    if len(tokens) != count:
        raise ValueError(f"需要 {count} 个整数，实际输入 {len(tokens)} 个")
    try:
        return [int(token) for token in tokens]
    except ValueError:
        raise ValueError("数组元素必须全部为整数") from None


def main() -> int:
    print("请输入数组长度 n：", flush=True)
    try:
        count = parse_count(sys.stdin.readline())
        print(f"请输入 {count} 个整数（同一行，以空格分隔）：", flush=True)
        numbers = parse_numbers(sys.stdin.readline(), count)
        result = max_subarray(numbers)
        print(f"最大子数组和：{result.total}")
        print(f"起始位置：{result.left + 1}（从 1 开始）")
        print(f"结束位置：{result.right + 1}（从 1 开始）")
        content = " ".join(str(numbers[i]) for i in range(result.left, result.right + 1))
        print(f"最大子数组：{content}")
        return 0
    except ValueError as error:
        print(f"输入错误：{error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
