"""Модуль с реализацией алгоритмов сортировки."""

from typing import List


def bubble_sort(arr: List[int]) -> List[int]:
    """
    Сортировка пузырьком.

    Временная сложность:
    - Худший случай: O(n²)
    - Средний случай: O(n²)
    - Лучший случай: O(n)

    Пространственная сложность: O(1)
    """
    n = len(arr)
    array = arr.copy()

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                swapped = True

        if not swapped:
            break

    return array


def selection_sort(arr: List[int]) -> List[int]:
    """
    Сортировка выбором.

    Временная сложность:
    - Худший случай: O(n²)
    - Средний случай: O(n²)
    - Лучший случай: O(n²)

    Пространственная сложность: O(1)
    """
    array = arr.copy()
    n = len(array)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if array[j] < array[min_idx]:
                min_idx = j

        array[i], array[min_idx] = array[min_idx], array[i]

    return array


def insertion_sort(arr: List[int]) -> List[int]:
    """
    Сортировка вставками.

    Временная сложность:
    - Худший случай: O(n²)
    - Средний случай: O(n²)
    - Лучший случай: O(n)

    Пространственная сложность: O(1)
    """
    array = arr.copy()

    for i in range(1, len(array)):
        key = array[i]
        j = i - 1

        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1

        array[j + 1] = key

    return array


def merge_sort(arr: List[int]) -> List[int]:
    """
    Сортировка слиянием.

    Временная сложность:
    - Худший случай: O(n log n)
    - Средний случай: O(n log n)
    - Лучший случай: O(n log n)

    Пространственная сложность: O(n)
    """
    if len(arr) <= 1:
        return arr.copy()

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    """Вспомогательная функция для слияния двух отсортированных массивов."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def quick_sort(arr: List[int]) -> List[int]:
    """
    Быстрая сортировка.

    Временная сложность:
    - Худший случай: O(n²)
    - Средний случай: O(n log n)
    - Лучший случай: O(n log n)

    Пространственная сложность: O(log n)
    """
    if len(arr) <= 1:
        return arr.copy()

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


def is_sorted(arr: List[int]) -> bool:
    """Проверяет, отсортирован ли массив."""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


SORTING_ALGORITHMS = {
    'bubble_sort': bubble_sort,
    'selection_sort': selection_sort,
    'insertion_sort': insertion_sort,
    'merge_sort': merge_sort,
    'quick_sort': quick_sort
}
