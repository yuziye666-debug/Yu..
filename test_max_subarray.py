"""功能、边界、穷举对照和命令行输入测试。运行：python -m unittest -v"""

import itertools
import os
from pathlib import Path
import random
import subprocess
import sys
import unittest

from max_subarray import (
    SubarrayResult,
    max_subarray,
    max_subarray_sum,
    parse_count,
    parse_numbers,
)


def brute_force(numbers: list[int]) -> SubarrayResult:
    """独立枚举全部区间，按和、起点、终点选择最优结果。"""
    intervals = (
        SubarrayResult(sum(numbers[left : right + 1]), left, right)
        for left in range(len(numbers))
        for right in range(left, len(numbers))
    )
    return max(intervals, key=lambda result: (result.total, -result.left, -result.right))


class AlgorithmTests(unittest.TestCase):
    def test_typical_array(self):
        numbers = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
        self.assertEqual(max_subarray(numbers), SubarrayResult(6, 3, 6))
        self.assertEqual(max_subarray_sum(numbers), 6)

    def test_all_negative(self):
        self.assertEqual(max_subarray([-8, -3, -6, -2, -5]), SubarrayResult(-2, 3, 3))

    def test_all_positive(self):
        self.assertEqual(max_subarray([1, 2, 3, 4]), SubarrayResult(10, 0, 3))

    def test_single_element(self):
        for number in (-7, 0, 9):
            with self.subTest(number=number):
                self.assertEqual(max_subarray([number]), SubarrayResult(number, 0, 0))

    def test_ties_keep_earliest_start_then_end(self):
        for numbers, expected in (
            ([0, 0, 0], SubarrayResult(0, 0, 0)),
            ([0, 1], SubarrayResult(1, 0, 1)),
            ([1, -1, 1], SubarrayResult(1, 0, 0)),
            ([-2, -2], SubarrayResult(-2, 0, 0)),
        ):
            with self.subTest(numbers=numbers):
                self.assertEqual(max_subarray(numbers), expected)

    def test_empty_array_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "数组不能为空"):
            max_subarray([])

    def test_large_integers(self):
        number = 10**100
        self.assertEqual(max_subarray([number, number, -1]), SubarrayResult(2 * number, 0, 1))

    def test_input_is_not_modified(self):
        numbers = [3, -1, 4]
        before = numbers.copy()
        max_subarray(numbers)
        self.assertEqual(numbers, before)

    def test_exhaustive_small_arrays_against_brute_force(self):
        # 长度 1～6，元素取 -2、0、2，共 1092 个数组。
        for length in range(1, 7):
            for values in itertools.product((-2, 0, 2), repeat=length):
                numbers = list(values)
                self.assertEqual(max_subarray(numbers), brute_force(numbers), numbers)

    def test_seeded_random_arrays_against_brute_force(self):
        generator = random.Random(20261028)
        for _ in range(500):
            numbers = [generator.randint(-100, 100) for _ in range(generator.randint(1, 30))]
            self.assertEqual(max_subarray(numbers), brute_force(numbers), numbers)


class InputTests(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(parse_count(" 3\n"), 3)
        self.assertEqual(parse_numbers("1\t-2  +3\n", 3), [1, -2, 3])

    def test_invalid_count(self):
        for text in ("", "abc", "2.5", "0", "-2"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_count(text)

    def test_missing_or_extra_elements(self):
        for text in ("", "1 2", "1 2 3 4"):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, "实际输入"):
                parse_numbers(text, 3)

    def test_non_integer_element(self):
        for text in ("1 x 3", "1 2.5 3"):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, "必须全部为整数"):
                parse_numbers(text, 3)


class CommandLineTests(unittest.TestCase):
    def run_program(self, text):
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(Path(__file__).with_name("max_subarray.py"))],
            input=text,
            capture_output=True,
            encoding="utf-8",
            env=dict(os.environ, PYTHONUTF8="1"),
            check=False,
            timeout=10,
        )

    def test_successful_output(self):
        result = self.run_program("9\n-2 1 -3 4 -1 2 1 -5 4\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        for expected in ("最大子数组和：6", "起始位置：4", "结束位置：7", "最大子数组：4 -1 2 1"):
            self.assertIn(expected, result.stdout)

    def test_bad_input_exits_with_error(self):
        for text in ("0\n", "abc\n", "3\n1 2\n", "3\n1 x 3\n", "", "3\n"):
            with self.subTest(text=text):
                result = self.run_program(text)
                self.assertEqual(result.returncode, 1)
                self.assertIn("输入错误：", result.stderr)
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
