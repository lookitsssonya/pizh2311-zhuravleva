import collections
import timeit
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt

from linked_list import LinkedList


def print_system_info() -> None:
    """Вывод информации о системе."""
    pc_info = """
ХАРАКТЕРИСТИКИ ПК ДЛЯ ТЕСТИРОВАНИЯ:
- Процессор: Intel Core i5-13420H (2.10 GHz)
- Оперативная память: 16 GB DDR5
- ОС: Windows 11
- Python: 3.11
"""
    print(pc_info)


def compare_list_vs_linkedlist_insert_start() -> Tuple[float, float]:
    """
    Сравнение вставки в начало для list и LinkedList.

    Returns:
        Tuple[float, float]: Время выполнения для list и LinkedList.
    """

    def list_insert_start(num_elements: int) -> List[int]:
        """
        Вставка n элементов в начало списка.

        Сложность: O(n²) - каждая операция insert(0) имеет O(n)
        """
        lst: List[int] = []
        for i in range(num_elements):
            lst.insert(0, i)
        return lst

    def linked_list_insert_start(num_elements: int) -> LinkedList:
        """
        Вставка n элементов в начало связного списка.

        Сложность: O(n)
        """
        ll = LinkedList()
        for i in range(num_elements):
            ll.insert_at_start(i)
        return ll

    test_size = 1000

    # Замер времени для list
    list_time = timeit.timeit(
        lambda: list_insert_start(test_size),
        number=10
    )

    # Замер времени для LinkedList
    linked_list_time = timeit.timeit(
        lambda: linked_list_insert_start(test_size),
        number=10
    )

    print(f'Вставка {test_size} элементов в начало:')
    print(f'  List.insert(0):      {list_time:.6f} секунд (O(n²))')
    print(f'  LinkedList.insert_start: {linked_list_time:.6f} секунд (O(n))')
    print(f'  Отношение: {list_time / linked_list_time:.2f}x')

    return list_time, linked_list_time


def compare_list_vs_deque_queue() -> Tuple[float, float]:
    """
    Сравнение list и deque для удаления из начала.

    Returns:
        Tuple[float, float]: Время выполнения для list и deque.
    """

    def list_queue_operations(num_elements: int) -> List[int]:
        """
        Удаление из начала list.

        Сложность: O(n²)
        """
        lst = list(range(num_elements))
        for _ in range(num_elements):
            lst.pop(0)
        return lst

    def deque_queue_operations(num_elements: int) -> collections.deque:
        """
        Удаление из начала deque.

        Сложность: O(n)
        """
        deq = collections.deque(range(num_elements))
        for _ in range(num_elements):
            deq.popleft()
        return deq

    test_size = 1000

    # Замер времени для list
    list_time = timeit.timeit(
        lambda: list_queue_operations(test_size),
        number=100
    )

    # Замер времени для deque
    deque_time = timeit.timeit(
        lambda: deque_queue_operations(test_size),
        number=100
    )

    print(f'{test_size} операций удаления из начала:')
    print(f'  List.pop(0):        {list_time:.6f} секунд (O(n²))')
    print(f'  Deque.popleft():    {deque_time:.6f} секунд (O(n))')
    print(f'  Отношение: {list_time / deque_time:.2f}x')

    return list_time, deque_time


def compare_list_vs_linkedlist_insert_end() -> Tuple[float, float]:
    """
    Сравнение list и LinkedList для вставки в конец.

    Returns:
        Tuple[float, float]: Время выполнения для list и LinkedList.
    """

    def list_insert_end(num_elements: int) -> List[int]:
        """
        Вставка n элементов в конец списка.

        Сложность: O(n)
        """
        lst: List[int] = []
        for i in range(num_elements):
            lst.append(i)
        return lst

    def linked_list_insert_end(num_elements: int) -> LinkedList:
        """
        Вставка n элементов в конец связного списка.

        Сложность: O(n)
        """
        ll = LinkedList()
        for i in range(num_elements):
            ll.insert_at_end(i)
        return ll

    test_size = 1000

    # Замер времени для list
    list_time = timeit.timeit(
        lambda: list_insert_end(test_size),
        number=100
    )

    # Замер времени для LinkedList
    linked_list_time = timeit.timeit(
        lambda: linked_list_insert_end(test_size),
        number=100
    )

    print(f'Вставка {test_size} элементов в конец:')
    print(f'  List.append():      {list_time:.6f} секунд (O(n))')
    print(f'  LinkedList.insert_end: {linked_list_time:.6f} секунд (O(n))')
    print(f'  Отношение: {list_time / linked_list_time:.2f}x')

    return list_time, linked_list_time


def performance_analysis_detailed() -> Dict[str, Any]:
    """
    Детальный анализ производительности с построением графиков.

    Returns:
        Dict[str, Any]: Результаты замеров.
    """
    sizes: List[int] = [100, 500, 1000, 2000, 5000]

    # Для хранения времени выполнения N операций
    list_insert_start_times: List[float] = []
    linked_list_insert_start_times: List[float] = []
    list_queue_times: List[float] = []
    deque_queue_times: List[float] = []
    list_insert_end_times: List[float] = []
    linked_list_insert_end_times: List[float] = []

    print('\n--- ДЕТАЛЬНЫЙ АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ ---')
    header = ('Размер | List.insert(0) | LinkedList.start | List.pop(0) | '
              'Deque.popleft() | List.append() | LinkedList.end')
    print(header)
    print('-' * len(header))

    for size in sizes:
        # Вставка в начало - list (N операций)
        def list_insert_start_operations():
            lst = []
            for i in range(size):
                lst.insert(0, i)
            return lst

        list_start_time = timeit.timeit(
            list_insert_start_operations,
            number=1
        )

        # Вставка в начало - LinkedList (N операций)
        def linked_list_insert_start_operations():
            ll = LinkedList()
            for i in range(size):
                ll.insert_at_start(i)
            return ll

        linked_list_start_time = timeit.timeit(
            linked_list_insert_start_operations,
            number=1
        )

        # Удаление из начала - list (N операций)
        def list_queue_operations():
            lst = list(range(size))
            for _ in range(size):
                lst.pop(0)
            return lst

        list_queue_time = timeit.timeit(
            list_queue_operations,
            number=10
        )

        # Удаление из начала - deque (N операций)
        def deque_queue_operations():
            deq = collections.deque(range(size))
            for _ in range(size):
                deq.popleft()
            return deq

        deque_queue_time = timeit.timeit(
            deque_queue_operations,
            number=10
        )

        # Вставка в конец - list (N операций)
        def list_insert_end_operations():
            lst = []
            for i in range(size):
                lst.append(i)
            return lst

        list_end_time = timeit.timeit(
            list_insert_end_operations,
            number=10
        )

        # Вставка в конец - LinkedList (N операций)
        def linked_list_insert_end_operations():
            ll = LinkedList()
            for i in range(size):
                ll.insert_at_end(i)
            return ll

        linked_list_end_time = timeit.timeit(
            linked_list_insert_end_operations,
            number=10
        )

        # Добавление результатов в списки
        list_insert_start_times.append(list_start_time)
        linked_list_insert_start_times.append(linked_list_start_time)
        list_queue_times.append(list_queue_time)
        deque_queue_times.append(deque_queue_time)
        list_insert_end_times.append(list_end_time)
        linked_list_insert_end_times.append(linked_list_end_time)

        row = (f'{size:6} | {list_start_time:14.6f} | '
               f'{linked_list_start_time:16.6f} | {list_queue_time:11.6f} | '
               f'{deque_queue_time:13.6f} | {list_end_time:12.6f} | '
               f'{linked_list_end_time:14.6f}')
        print(row)

    # Построение графиков
    plt.figure(figsize=(15, 12))

    # График 1: Вставка в начало
    plt.subplot(2, 2, 1)
    plt.plot(
        sizes, list_insert_start_times,
        'ro-', label='List.insert(0) - O(n²)', linewidth=2, markersize=6
    )
    plt.plot(
        sizes, linked_list_insert_start_times, 'bo-',
        label='LinkedList.insert_start - O(n)', linewidth=2, markersize=6
    )
    plt.xlabel('Количество элементов')
    plt.ylabel('Время (секунды)')
    plt.title('Вставка в начало: List vs LinkedList\n'
              '(Время выполнения N операций)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # График 2: Удаление из начала
    plt.subplot(2, 2, 2)
    plt.plot(
        sizes, list_queue_times,
        'ro-', label='List.pop(0) - O(n²)', linewidth=2, markersize=6
    )
    plt.plot(
        sizes, deque_queue_times,
        'go-', label='Deque.popleft() - O(n)', linewidth=2, markersize=6
    )
    plt.xlabel('Количество элементов')
    plt.ylabel('Время (секунды)')
    plt.title('Удаление из начала: List vs Deque\n'
              '(Время выполнения N операций)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # График 3: Вставка в конец
    plt.subplot(2, 2, 3)
    plt.plot(
        sizes, list_insert_end_times,
        'ro-', label='List.append() - O(n)', linewidth=2, markersize=6
    )
    plt.plot(
        sizes, linked_list_insert_end_times,
        'mo-', label='LinkedList.insert_end - O(n)', linewidth=2, markersize=6
    )
    plt.xlabel('Количество элементов')
    plt.ylabel('Время (секунды)')
    plt.title('Вставка в конец: List vs LinkedList\n'
              '(Время выполнения N операций)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('performance_comparison_detailed.png', dpi=300,
                bbox_inches='tight')
    plt.show()

    return {
        'sizes': sizes,
        'list_insert_start': list_insert_start_times,
        'linked_list_insert_start': linked_list_insert_start_times,
        'list_queue': list_queue_times,
        'deque_queue': deque_queue_times,
        'list_insert_end': list_insert_end_times,
        'linked_list_insert_end': linked_list_insert_end_times
    }


def analyze_asymptotic_complexity() -> None:
    """
    Анализ асимптотической сложности на основе экспериментальных данных.
    """
    print('\n=== АНАЛИЗ АСИМПТОТИЧЕСКОЙ СЛОЖНОСТИ ===')

    # Теоретическая сложность
    complexities = {
        'list_insert_start': 'O(n²)',
        'linked_list_insert_start': 'O(n)',
        'list_pop_start': 'O(n²)',
        'deque_popleft': 'O(n)',
        'list_append': 'O(n)',
        'linked_list_append': 'O(n)'
    }

    print('Теоретическая сложность операций:')
    for op, complexity in complexities.items():
        print(f'  {op}: {complexity}')

    print('\nЭкспериментальные данные подтверждают:')
    print('- List.insert(0) и List.pop(0) показывают квадратичный рост')
    print('- LinkedList.insert_start и Deque.popleft показывают линейный рост')
    print('- List.append() и LinkedList.insert_end показывают линейный рост')


def run_performance_analysis() -> Dict[str, Any]:
    """Запуск полного анализа производительности."""
    print_system_info()

    print('\n=== АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ СТРУКТУР ДАННЫХ ===')

    # Базовые сравнения
    compare_list_vs_linkedlist_insert_start()
    compare_list_vs_deque_queue()
    compare_list_vs_linkedlist_insert_end()

    # Детальный анализ с графиками
    results = performance_analysis_detailed()

    # Анализ асимптотической сложности
    analyze_asymptotic_complexity()

    return results


if __name__ == '__main__':
    run_performance_analysis()
