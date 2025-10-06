import time
from typing import List, Tuple

import matplotlib.pyplot as plt

from recursion import factorial, fibonacci_naive, fast_power
from memoization import fibonacci_memo, compare_fibonacci_performance
from recursion_tasks import binary_search_recursive, hanoi_towers
from recursion_tasks import file_system_traversal


def performance_experiment() -> None:
    """
    Эксперимент по сравнению производительности рекурсивных алгоритмов.

    Проводит замеры времени выполнения и строит сравнительные графики.
    """
    print('\n=== ЭКСПЕРИМЕНТАЛЬНОЕ ИССЛЕДОВАНИЕ ===\n')

    compare_fibonacci_performance(35)

    print('\n--- Построение графика времени выполнения ---')
    n_values, naive_times, memo_times = measure_fibonacci_times()
    plot_performance_comparison(n_values, naive_times, memo_times)

    print_complexity_analysis()

    demonstrate_filesystem_traversal()


def measure_fibonacci_times() -> Tuple[List[int], List[float], List[float]]:
    """
    Измеряет время выполнения наивной и мемоизированной версий Фибоначчи.

    Returns:
        Tuple с n_values, naive_times, memo_times
    """
    n_values_list = list(range(1, 25))
    naive_times_list = []
    memo_times_list = []

    for current_n in n_values_list:
        start_time = time.perf_counter()
        fibonacci_naive(current_n)
        naive_time = time.perf_counter() - start_time
        naive_times_list.append(naive_time)

        start_time = time.perf_counter()
        fibonacci_memo(current_n)
        memo_time = time.perf_counter() - start_time

        if memo_time < 0.0001:
            iterations_count = 1000
            start_time = time.perf_counter()
            for _ in range(iterations_count):
                fibonacci_memo(current_n)
            memo_time = (time.perf_counter() - start_time) / iterations_count

        memo_times_list.append(memo_time)

    return n_values_list, naive_times_list, memo_times_list


def plot_performance_comparison(
    n_values: List[int],
    naive_times: List[float],
    memo_times: List[float]
) -> None:
    """
    Строит графики сравнения производительности.

    Args:
        n_values: Значения n для оси X
        naive_times: Времена наивной реализации
        memo_times: Времена мемоизированной реализации
    """
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(n_values, naive_times, label='Наивная рекурсия',
             marker='o', color='red')
    plt.plot(n_values, memo_times, label='С мемоизацией',
             marker='s', color='green')
    plt.xlabel('n')
    plt.ylabel('Время (секунды)')
    plt.title('Сравнение времени вычисления чисел Фибоначчи')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(n_values, naive_times, label='Наивная рекурсия',
             marker='o', color='red')
    plt.plot(n_values, memo_times, label='С мемоизацией',
             marker='s', color='green')
    plt.xlabel('n')
    plt.ylabel('Время (секунды)')
    plt.title('Логарифмическая шкала времени')
    plt.legend()
    plt.grid(True)
    plt.yscale('log')

    plt.tight_layout()
    plt.savefig('fibonacci_performance.png', dpi=300, bbox_inches='tight')
    plt.show()
    print('График сохранен как fibonacci_performance.png')


def print_complexity_analysis() -> None:
    """Выводит анализ временной сложности алгоритмов."""
    print('\n--- Анализ сложности алгоритмов ---')
    print('Наивная рекурсия Фибоначчи: O(2^n) - экспоненциальная сложность')
    print('Фибоначчи с мемоизацией: O(n) - линейная сложность')
    print('Быстрое возведение в степень: O(log n) - логарифмическая сложность')
    print('Факториал: O(n) - линейная сложность')
    print('Бинарный поиск: O(log n) - логарифмическая сложность')


def demonstrate_filesystem_traversal() -> None:
    """Демонстрирует рекурсивный обход файловой системы."""
    print('\n--- Обход файловой системы ---')
    test_depth = 3
    print(f'Обход с максимальной глубиной {test_depth}:')
    file_system_traversal('.', max_depth=test_depth)


def demo_all_functions() -> None:
    """Демонстрация всех реализованных рекурсивных функций."""
    print('=== ДЕМОНСТРАЦИЯ ВСЕХ ФУНКЦИЙ ===\n')

    print('1. Факториал 5:', factorial(5))

    print('2. 10-е число Фибоначчи:')
    print('   Наивный метод:', fibonacci_naive(10))
    print('   С мемоизацией:', fibonacci_memo(10))

    print('3. Быстрое возведение в степень:')
    print('   2^10 =', fast_power(2, 10))
    print('   3^5 =', fast_power(3, 5))

    search_array = [1, 3, 5, 7, 9, 11, 13]
    search_target_value = 7
    result_index = binary_search_recursive(search_array, search_target_value)
    print(f'4. Бинарный поиск {search_target_value} в {search_array}: '
          f'индекс {result_index}')

    print('5. Ханойские башни для 3 дисков:')
    hanoi_towers(3)

    print('6. Обход файловой системы (текущая директория, глубина 1):')
    file_system_traversal('.', max_depth=1)


def system_info() -> None:
    """Вывод информации о системе для воспроизводимости экспериментов."""
    pc_info = """
ХАРАКТЕРИСТИКИ ПК ДЛЯ ТЕСТИРОВАНИЯ:
- Процессор: Intel Core i5-13420H (2.10 GHz)
- Оперативная память: 16 GB DDR5
- ОС: Windows 11
- Python: 3.11
"""
    print(pc_info)


if __name__ == '__main__':
    system_info()
    demo_all_functions()
    performance_experiment()
