"""
Модуль с оптимизированными рекурсивными функциями с использованием мемоизации.
"""
import timeit
from typing import Dict

from recursion import fibonacci_naive


def fibonacci_memo(
    fib_n: int,
    memo_dict: Dict[int, int] = None
) -> int:
    """
    Вычисление n-го числа Фибоначчи с мемоизацией.

    Args:
        fib_n: Порядковый номер числа Фибоначчи
        memo_dict: Словарь для хранения вычисленных значений

    Returns:
        n-е число Фибоначчи
    """
    if memo_dict is None:
        memo_dict = {}

    if fib_n in memo_dict:
        return memo_dict[fib_n]

    if fib_n == 0:
        return 0
    if fib_n == 1:
        return 1

    memo_dict[fib_n] = (
        fibonacci_memo(fib_n - 1, memo_dict) +
        fibonacci_memo(fib_n - 2, memo_dict)
    )
    return memo_dict[fib_n]


# Временная сложность: O(n).  Глубина рекурсии: O(n).


def compare_fibonacci_performance(fib_number: int = 35) -> None:
    """
    Сравнение производительности наивной и мемоизированной версий.

    Args:
        fib_number: Номер числа Фибоначчи для тестирования
    """
    naive_time = timeit.timeit(lambda: fibonacci_naive(fib_number), number=1)
    memo_time = timeit.timeit(lambda: fibonacci_memo(fib_number), number=1)

    naive_result = fibonacci_naive(fib_number)
    memo_result = fibonacci_memo(fib_number)

    print(f'Результат для n={fib_number}:')
    print(f'Наивная версия: {naive_result}, время: {naive_time:.6f} сек')
    print(f'Мемоизированная версия: {memo_result}, время: {memo_time:.6f} сек')

    if memo_time > 0:
        speedup = naive_time / memo_time
        print(f'Ускорение: {speedup:.2f} раз')
    else:
        print('Ускорение: > 1000 раз')


def measure_multiple_n() -> None:
    """Измерение времени для разных значений n."""
    test_values = [10, 20, 30, 35]

    print('\nСравнение времени выполнения для разных n:')
    print('n\tНаивная (сек)\tМемоизированная (сек)\tУскорение')
    print('-' * 60)

    for current_n in test_values:
        naive_time = timeit.timeit(
            lambda: fibonacci_naive(current_n), number=1
        )
        memo_time = timeit.timeit(lambda: fibonacci_memo(current_n), number=1)

        if memo_time > 0:
            speedup = naive_time / memo_time
        else:
            speedup = float('inf')

        if naive_time > 1:
            time_str = f'{naive_time:.3f}'
        else:
            time_str = f'{naive_time:.6f}'

        print(
            f'{current_n}\t{time_str}\t\t{memo_time:.6f}\t\t\t{speedup:.0f}x'
        )


if __name__ == '__main__':
    compare_fibonacci_performance(35)
    measure_multiple_n()
