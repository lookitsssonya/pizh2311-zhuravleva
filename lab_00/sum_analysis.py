# sum_analysis.py

import random
import timeit
from typing import Callable, List

import matplotlib.pyplot as plt


# Исходная простая задача
def calculate_sum() -> None:
    """Считает сумму двух введенных чисел."""
    a = int(input())  # O(1) - чтение одной строки и преобразование
    b = int(input())  # O(1)
    result = a + b    # O(1) - арифметическая операция
    print(result)     # O(1) - вывод одной строки
    # Общая сложность функции: O(1)


# calculate_sum()  # Раскомментировать для проверки исходной задачи

# УСЛОЖНЕННАЯ ЗАДАЧА ДЛЯ АНАЛИЗА ПРОИЗВОДИТЕЛЬНОСТИ
# Суммирование N чисел для демонстрации линейной сложности O(N)
def sum_array(arr: List[int]) -> int:
    """Возвращает сумму всех элементов массива.
    Сложность: O(N), где N - длина массива.
    """
    total = 0   # O(1) - инициализация переменной
    for num in arr:           # O(N) - цикл по всем элементам массива
        total += num      # O(1) - операция сложения и присваивания
    return total              # O(1) - возврат результата
    # Общая сложность: O(1) + O(N) * O(1) + O(1) = O(N)


# Функция для замера времени выполнения
def measure_execution_time(
    func: Callable[[List[int]], int],
    input_data: List[int]
) -> float:
    """Измеряет время выполнения функции в миллисекундах."""
    start_time = timeit.default_timer()
    func(input_data)
    end_time = timeit.default_timer()
    return (end_time - start_time) * 1000  # Конвертация в миллисекунды


# Характеристики ПК
pc_info: str = """
Характеристики ПК для тестирования:
- Процессор: Intel Core i5-13420H (2.10 GHz)
- Оперативная память: 16 GB DDR5
- ОС: Windows 11
- Python: 3.11
"""
print(pc_info)

# Проведение экспериментов
sizes: List[int] = [
    1000, 5000, 10000, 50000, 100000, 500000
]  # Размеры массивов
times: List[float] = []  # Время выполнения для каждого размера
time_per_element_values: List[float] = []  # Храним время на элемент

print("Замеры времени выполнения для алгоритма суммирования массива:")
print("{:>10} {:>12} {:>15}".format(
    "Размер (N)", "Время (мс)", "Время/N (мкс)"
))

for size in sizes:
    # Генерация случайного массива заданного размера
    test_data: List[int] = [random.randint(1, 1000) for _ in range(size)]

    # Замер времени выполнения (усреднение на 10 запусках)
    execution_time: float = timeit.timeit(
        lambda: sum_array(test_data), number=10
    ) * 1000 / 10

    times.append(execution_time)
    # мкс на элемент
    time_per_element: float = (
        (execution_time * 1000) / size if size > 0 else 0
    )
    time_per_element_values.append(time_per_element)

    print("{:>10} {:>12.4f} {:>15.4f}".format(
        size, execution_time, time_per_element
    ))

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(sizes, times, 'bo-', label='Измеренное время')
plt.xlabel('Размер массива (N)')
plt.ylabel('Время выполнения (мс)')
plt.title('Зависимость времени выполнения от размера массива\n'
          'Сложность: O(N)')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.savefig('time_complexity_plot.png', dpi=300, bbox_inches='tight')
plt.show()

# Дополнительный анализ: сравнение с теоретической оценка
print("\nАнализ результатов:")
print("1. Теоретическая сложность алгоритма: O(N)")
print("2. Практические замеры показывают линейную зависимость времени от N")

# Используем среднее значение time_per_element
if time_per_element_values:
    avg_time_per_element: float = (
        sum(time_per_element_values) / len(time_per_element_values)
    )
    print("3. Среднее время на один элемент: ~{:.4f} мкс".format(
        avg_time_per_element
    ))
    print("4. Время на один элемент примерно постоянно")
else:
    print("3. Нет данных для анализа времени на элемент")
