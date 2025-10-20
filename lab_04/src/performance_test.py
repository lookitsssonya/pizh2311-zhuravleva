"""Модуль для тестирования производительности алгоритмов сортировки."""

import timeit
from typing import List, Dict, Any, Callable
from sorts import SORTING_ALGORITHMS, is_sorted
from generate_data import generate_test_datasets


def system_info() -> None:
    """Вывод информации о системе."""
    pc_info = """
ХАРАКТЕРИСТИКИ ПК ДЛЯ ТЕСТИРОВАНИЯ:
- Процессор: Intel Core i5-13420H (2.10 GHz)
- Оперативная память: 16 GB DDR5
- ОС: Windows 11
- Python: 3.11
"""
    print(pc_info)


def measure_sorting_time(
    sort_func: Callable[[List[int]], List[int]],
    data: List[int]
) -> float:
    """Измеряет время выполнения сортировки."""
    data_copy = data.copy()

    def sort_wrapper():
        return sort_func(data_copy)

    timer = timeit.timeit(sort_wrapper, number=1)
    return timer


def run_performance_tests(
    sizes: List[int] = None
) -> Dict[str, Any]:
    """Запускает тесты производительности."""
    if sizes is None:
        sizes = [100, 1000, 5000, 10000]

    system_info()

    datasets = generate_test_datasets(sizes)

    results_data = {}

    print(f"Запуск тестов для размеров: {sizes}")

    for algo_name, sort_func in SORTING_ALGORITHMS.items():
        results_data[algo_name] = {}
        print(f"\nТестирование {algo_name}...")

        for data_type, size_data in datasets.items():
            results_data[algo_name][data_type] = {}

            for size, data in size_data.items():
                sorted_data = sort_func(data)
                if not is_sorted(sorted_data):
                    print(f"Ошибка: {algo_name} не отсортировал {data_type}")
                    continue

                time_taken = measure_sorting_time(sort_func, data)
                results_data[algo_name][data_type][size] = time_taken

                print(f"{data_type}, размер {size}: {time_taken:.6f} сек")

    return results_data


def main() -> None:
    """Основная функция."""
    run_performance_tests()


if __name__ == '__main__':
    main()
