import os
from typing import List, Optional


def binary_search_recursive(
    arr: List[int],
    target_value: int,
    left: int = 0,
    right: Optional[int] = None
) -> Optional[int]:
    """
    Рекурсивная реализация бинарного поиска.

    Args:
        arr: Отсортированный массив
        target_value: Искомый элемент
        left: Левая граница поиска
        right: Правая граница поиска

    Returns:
        Индекс элемента или None если не найден
    """
    if right is None:
        right = len(arr) - 1

    if left > right:
        return None

    mid = (left + right) // 2

    if arr[mid] == target_value:
        return mid
    elif arr[mid] < target_value:
        return binary_search_recursive(arr, target_value, mid + 1, right)
    else:
        return binary_search_recursive(arr, target_value, left, mid - 1)


# Временная сложность: O(log n).  Глубина рекурсии: O(log n).


def file_system_traversal(
    start_path: str,
    level: int = 0,
    max_depth: Optional[int] = None
) -> None:
    """
    Рекурсивный обход файловой системы с выводом дерева каталогов.

    Args:
        start_path: Начальный путь для обхода
        level: Текущий уровень вложенности
        max_depth: Максимальная глубина рекурсии
    """
    if max_depth is not None and level > max_depth:
        return

    try:
        entries = os.listdir(start_path)
    except PermissionError:
        print('  ' * level + f'[Доступ запрещен: {start_path}]')
        return
    except FileNotFoundError:
        print('  ' * level + f'[Путь не найден: {start_path}]')
        return

    for entry in sorted(entries):
        full_path = os.path.join(start_path, entry)

        if os.path.isdir(full_path):
            print('  ' * level + f'-- {entry}/')
            file_system_traversal(full_path, level + 1, max_depth)
        else:
            print('  ' * level + f'- {entry}')


# Временная сложность: O(n).  Глубина рекурсии: O(d).


def hanoi_towers(
    num_disks: int,
    source_rod: str = 'A',
    auxiliary_rod: str = 'B',
    target_rod: str = 'C'
) -> None:
    """
    Решение задачи о Ханойских башнях для n дисков.

    Args:
        num_disks: Количество дисков
        source_rod: Исходный стержень
        auxiliary_rod: Вспомогательный стержень
        target_rod: Целевой стержень
    """
    if num_disks == 1:
        print(f'Переместить диск 1 с {source_rod} на {target_rod}')
        return

    hanoi_towers(num_disks - 1, source_rod, target_rod, auxiliary_rod)
    print(f'Переместить диск {num_disks} с {source_rod} на {target_rod}')
    hanoi_towers(num_disks - 1, auxiliary_rod, source_rod, target_rod)


# Временная сложность: O(2^n).  Глубина рекурсии: O(n).


if __name__ == '__main__':
    test_arr = [1, 3, 5, 7, 9, 11, 13, 15]
    search_target = 7
    result = binary_search_recursive(test_arr, search_target)
    print(f'Бинарный поиск {search_target} в {test_arr}: индекс {result}')

    print('\nХанойские башни для 3 дисков:')
    hanoi_towers(3)

    print('\nОбход файловой системы (текущая директория, глубина 2):')
    file_system_traversal('.', max_depth=2)
