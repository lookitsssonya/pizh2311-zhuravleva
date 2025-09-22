## **Дисциплина**: Анализ сложности алгоритмов
## Тема 01: Введение в алгоритмы. Сложность. Поиск.
### Выполнила студентка группы ПИЖ-б-о-23-1(1) Журавлева Софья Витальевна 
**Репозиторий Git:** https://github.com/lookitsssonya/pizh2311_zhuravleva  <br></br>
**Цель работы:**   
Освоить понятие вычислительной сложности алгоритма. Получить практические навыки
реализации и анализа линейного и бинарного поиска. Научиться экспериментально подтверждать
теоретические оценки сложности O(n) и O(log n).  

**Теория (кратко):**   
**Сложность алгоритма:** Характеризует количество ресурсов (времени и памяти), необходимых
алгоритму для обработки входных данных объема n.   
**Асимптотический анализ:** Анализ поведения алгоритма при стремлении n к бесконечности.
Позволяет абстрагироваться от констант и аппаратных особенностей.   
**O-нотация («О-большое»):** Верхняя асимптотическая оценка роста функции. Определяет
наихудший сценарий работы алгоритма.   
**Линейный поиск (Linear Search):** Последовательный перебор всех элементов массива.
Сложность: O(n).   
**Бинарный поиск (Binary Search):** Поиск в отсортированном массиве путем многократного
деления интервала поиска пополам. Сложность: O(log n). Требует предварительной сортировки
(O(n log n)).   

**Задание:**

 1. Реализовать функцию линейного поиска элемента в массиве.
 2. Реализовать функцию бинарного поиска элемента в отсортированном массиве.
 3. Провести теоретический анализ сложности обоих алгоритмов.
 4. Экспериментально сравнить время выполнения алгоритмов на массивах разного размера.
 5. Визуализировать результаты, подтвердив асимптотику O(n) и O(log n).  

*search_comparison.py:*
```python
"""
Модуль для сравнения производительности линейного и бинарного поиска.
Содержит реализации алгоритмов и функции для тестирования.
"""

import random
import timeit
from typing import Dict, List, Optional, Callable

import matplotlib.pyplot as plt


def linear_search(arr: List[int], target: int) -> Optional[int]:
    """
    Линейный поиск элемента в массиве.

    Args:
        arr: Массив целых чисел для поиска
        target: Искомый элемент

    Returns:
        Индекс элемента или None, если элемент не найден
    """
    # O(n) - перебор всех элементов массива
    for i in range(len(arr)):  # O(n) - цикл по n элементам
        if arr[i] == target:  # O(1) - сравнение элементов
            return i  # O(1) - возврат результата
    return None  # O(1) - возврат None, если элемент не найден

    # Общая сложность: O(n)


def binary_search(arr: List[int], target: int) -> Optional[int]:
    """
    Бинарный поиск элемента в отсортированном массиве.

    Args:
        arr: Отсортированный массив целых чисел
        target: Искомый элемент

    Returns:
        Индекс элемента или None, если элемент не найден
    """
    left = 0  # O(1) - инициализация переменной
    right = len(arr) - 1  # O(1) - получение правой границы массива

    # O(log n) - цикл выполняется log2(n) раз
    while left <= right:  # O(1) - сравнение
        mid = (left + right) // 2  # O(1) - вычисление среднего индекса

        if arr[mid] == target:  # O(1) - сравнение элементов
            return mid  # O(1) - возврат результата
        elif arr[mid] < target:  # O(1) - сравнение
            left = mid + 1  # O(1) - обновление границы
        else:
            right = mid - 1  # O(1) - обновление границы

    return None  # O(1) - возврат None, если элемент не найден

    # Общая сложность: O(log n)


def generate_sorted_array(size: int) -> List[int]:
    """
    Генерация отсортированного массива уникальных целых чисел.

    Args:
        size: Размер массива

    Returns:
        Отсортированный массив уникальных целых чисел
    """
    # O(n log n) - создание отсортированного массива уникальных чисел
    return sorted(random.sample(range(size * 3), size))


def measure_search_time(search_func: Callable, arr: List[int], target: int,
                        repetitions: int = 1000) -> float:
    """
    Измерение среднего времени выполнения функции поиска.

    Args:
        search_func: Функция поиска (linear_search или binary_search)
        arr: Массив для поиска
        target: Искомый элемент
        repetitions: Количество повторений для усреднения

    Returns:
        Среднее время выполнения в секундах
    """
    # Более точный замер времени с помощью timeit
    def inner():
        return search_func(arr, target)

    total_time = timeit.timeit(inner, number=repetitions)
    return total_time / repetitions


def print_results_table(alg_name: str, results: Dict[int, Dict[str, float]],
                        sizes: List[int]) -> None:
    """
    Вывод таблицы результатов для указанного алгоритма.

    Args:
        alg_name: Название алгоритма
        results: Результаты измерений
        sizes: Размеры массивов
    """
    print(f"\n{'='*80}")
    print(f"ТАБЛИЦА РЕЗУЛЬТАТОВ ДЛЯ {alg_name}")
    print(f"{'='*80}")

    # Заголовок таблицы
    header = "Размер ".ljust(12) + " | " + \
             "Первый".ljust(12) + " | " + \
             "Средний".ljust(12) + " | " + \
             "Последний".ljust(12) + " | " + \
             "Отсутств.".ljust(12)
    print(header)
    print("-" * len(header))

    # Данные таблицы
    for size in sizes:
        row = f"{size}".ljust(12) + " | "
        row += f"{results[size]['first']:.8f}".ljust(12) + " | "
        row += f"{results[size]['middle']:.8f}".ljust(12) + " | "
        row += f"{results[size]['last']:.8f}".ljust(12) + " | "
        row += f"{results[size]['missing']:.8f}".ljust(12)
        print(row)

    print("-" * len(header))


def print_comparison_table(results_linear: Dict[int, Dict[str, float]],
                           results_binary: Dict[int, Dict[str, float]],
                           sizes: List[int]) -> float:
    """
    Вывод таблицы сравнения производительности алгоритмов.

    Args:
        results_linear: Результаты линейного поиска
        results_binary: Результаты бинарного поиска
        sizes: Размеры массивов

    Returns:
        Максимальное ускорение бинарного поиска
    """
    print(f"\n{'='*60}")
    print("ТАБЛИЦА СРАВНЕНИЯ ПРОИЗВОДИТЕЛЬНОСТИ (последний элемент)")
    print(f"{'='*60}")

    header = "Размер ".ljust(12) + " | " + \
             "Linear (с)".ljust(15) + " | " + \
             "Binary (с)".ljust(15) + " | " + \
             "Ускорение".ljust(15)
    print(header)
    print("-" * len(header))

    max_speedup = 0.0
    for size in sizes:
        linear_time = results_linear[size]['last']
        binary_time = results_binary[size]['last']
        speedup = linear_time / binary_time
        max_speedup = max(max_speedup, speedup)

        row = f"{size}".ljust(12) + " | "
        row += f"{linear_time:.8f}".ljust(15) + " | "
        row += f"{binary_time:.8f}".ljust(15) + " | "
        row += f"{speedup:.1f} раз".ljust(15)
        print(row)

    print("-" * len(header))
    return max_speedup


def run_experiment() -> None:
    """
    Проведение эксперимента по сравнению производительности поиска.
    Генерация данных, замер времени и построение графиков.
    """
    # Константы для эксперимента
    sizes = [1000, 2000, 5000, 10000, 20000, 50000, 100000]
    target_types = ['first', 'middle', 'last', 'missing']

    # Результаты измерений
    results_linear: Dict[int, Dict[str, float]] = {}
    results_binary: Dict[int, Dict[str, float]] = {}
    linear_times_avg: List[float] = []
    binary_times_avg: List[float] = []

    for size in sizes:
        # Генерация отсортированного массива
        arr = generate_sorted_array(size)

        # Выбор целевых элементов для тестирования
        targets = {
            'first': arr[0],
            'middle': arr[size // 2],
            'last': arr[-1],
            'missing': -1
        }

        # Результаты для текущего размера
        results_linear[size] = {}
        results_binary[size] = {}

        linear_time_sum = 0.0
        binary_time_sum = 0.0

        for target_type in target_types:
            target = targets[target_type]

            # Измерение времени линейного поиска
            linear_time = measure_search_time(linear_search, arr, target, 100)
            results_linear[size][target_type] = linear_time
            linear_time_sum += linear_time

            # Измерение времени бинарного поиска
            binary_time = measure_search_time(
                binary_search, arr, target, 10000
            )
            results_binary[size][target_type] = binary_time
            binary_time_sum += binary_time

        # Усреднение результатов
        avg_linear = linear_time_sum / len(target_types)
        avg_binary = binary_time_sum / len(target_types)
        linear_times_avg.append(avg_linear)
        binary_times_avg.append(avg_binary)

    # Вывод таблиц результатов
    print_results_table("linear_search", results_linear, sizes)
    print_results_table("binary_search", results_binary, sizes)
    max_speedup = print_comparison_table(
        results_linear, results_binary, sizes
    )

    # Построение графиков
    plot_results(sizes, linear_times_avg, binary_times_avg)

    # Анализ результатов
    print_analysis(max_speedup)


def plot_results(sizes: List[int], linear_times: List[float],
                 binary_times: List[float]) -> None:
    """
    Построение графиков результатов эксперимента.

    Args:
        sizes: Размеры массивов
        linear_times: Время выполнения линейного поиска
        binary_times: Время выполнения бинарного поиска
    """
    # Создание области для графиков
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # График в линейном масштабе
    ax1.plot(sizes, linear_times, 'o-',
             label='Линейный поиск O(n)', linewidth=2)
    ax1.plot(sizes, binary_times, 's-',
             label='Бинарный поиск O(log n)', linewidth=2)
    ax1.set_xlabel('Размер массива', fontsize=12)
    ax1.set_ylabel('Время выполнения (секунды)', fontsize=12)
    ax1.set_title('Сравнение времени поиска', fontsize=14)
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)

    # График в логарифмическом масштабе по оси Y
    ax2.semilogy(sizes, linear_times, 'o-',
                 label='Линейный поиск O(n)', linewidth=2)
    ax2.semilogy(sizes, binary_times, 's-',
                 label='Бинарный поиск O(log n)', linewidth=2)
    ax2.set_xlabel('Размер массива', fontsize=12)
    ax2.set_ylabel('Время выполнения (log scale)', fontsize=12)
    ax2.set_title('Логарифмическая шкала времени', fontsize=14)
    ax2.legend(fontsize=12)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('search_performance.png', dpi=300, bbox_inches='tight')
    plt.show()


def print_analysis(max_speedup: float) -> None:
    """
    Анализ результатов эксперимента.

    Args:
        max_speedup: Максимальное ускорение бинарного поиска
    """
    print("\n" + "="*60)
    print("АНАЛИЗ РЕЗУЛЬТАТОВ")
    print("="*60)

    print("Алгоритм линейного поиска: теоретическая оценка O(n)")
    print("На практике: минимальное время для первого элемента массива,")
    print("максимальное - для конечного и отсутствующего элементов.")
    print("График демонстрирует прямолинейную зависимость от размера.")
    print("Поиск последнего элемента требует n операций сравнения.")

    print("\nАлгоритм бинарного поиска: теоретическая оценка O(log n)")
    print("На практике: время выполнения слабо зависит от позиции искомого")
    print("элемента, график имеет логарифмический характер роста.")
    print("Для нахождения конечного элемента необходимо log(n) операций.")

    print(f"\nНаибольшее ускорение: {max_speedup:.1f} раз")
    print("Бинарный поиск существенно эффективнее на больших объемах данных.")


if __name__ == '__main__':
    """
    Основная точка входа в программу.
    """
    # Характеристики ПК для тестирования
    pc_info = """
ХАРАКТЕРИСТИКИ ПК ДЛЯ ТЕСТИРОВАНИЯ:
- Процессор: Intel Core i5-13420H (2.10 GHz)
- Оперативная память: 16 GB DDR5
- ОС: Windows 11
- Python: 3.11
"""
    print(pc_info)

    # Запуск эксперимента
    run_experiment()

```
*Пример вывода:*  
<img src="./lab_01/out.png">   
<img src="./lab_01/out2.png">   
<img src="./lab_01/out3.png">   
<img src="./lab_01/search_performance.png">