"""Модуль для генерации тестовых данных."""

import random
from typing import List, Dict


def generate_random_array(
    size: int,
    min_val: int = 0,
    max_val: int = 10000
) -> List[int]:
    """Генерирует массив случайных чисел."""
    return [random.randint(min_val, max_val) for _ in range(size)]


def generate_sorted_array(
    size: int,
    min_val: int = 0,
    max_val: int = 10000
) -> List[int]:
    """Генерирует отсортированный массив."""
    arr = generate_random_array(size, min_val, max_val)
    arr.sort()
    return arr


def generate_reversed_array(
    size: int,
    min_val: int = 0,
    max_val: int = 10000
) -> List[int]:
    """Генерирует обратно отсортированный массив."""
    arr = generate_sorted_array(size, min_val, max_val)
    arr.reverse()
    return arr


def generate_almost_sorted_array(
    size: int,
    sorted_ratio: float = 0.95
) -> List[int]:
    """Генерирует почти отсортированный массив."""
    arr = generate_sorted_array(size)
    num_to_shuffle = int(size * (1 - sorted_ratio))

    for _ in range(num_to_shuffle):
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        arr[i], arr[j] = arr[j], arr[i]

    return arr


def generate_test_datasets(
    sizes: List[int]
) -> Dict[str, Dict[int, List[int]]]:
    """Генерирует тестовые данные."""
    data_types = {
        'random': generate_random_array,
        'sorted': generate_sorted_array,
        'reversed': generate_reversed_array,
        'almost_sorted': generate_almost_sorted_array
    }

    datasets = {}

    for data_type, generator in data_types.items():
        datasets[data_type] = {}
        for size in sizes:
            datasets[data_type][size] = generator(size)

    return datasets
