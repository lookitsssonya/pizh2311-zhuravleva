"""Модуль с реализацией различных хеш-функций для строк."""
from typing import Callable


def simple_hash(key: str, table_size: int) -> int:
    """
    Простая хеш-функция - сумма кодов символов.

    Args:
        key: Входная строка.
        table_size: Размер хеш-таблицы.

    Returns:
        Хеш-значение в диапазоне [0, table_size-1].
    """
    hash_value = 0
    for char in key:
        hash_value += ord(char)
    return hash_value % table_size


def polynomial_hash(
    key: str, table_size: int, base: int = 31
) -> int:
    """
    Полиномиальная хеш-функция.

    Args:
        key: Входная строка.
        table_size: Размер хеш-таблицы.
        base: Основание полинома.

    Returns:
        Хеш-значение в диапазоне [0, table_size-1].
    """
    hash_value = 0
    for char in key:
        hash_value = hash_value * base + ord(char)
    return hash_value % table_size


def djb2_hash(key: str, table_size: int) -> int:
    """
    Хеш-функция DJB2.

    Args:
        key: Входная строка.
        table_size: Размер хеш-таблицы.

    Returns:
        Хеш-значение в диапазоне [0, table_size-1].
    """
    hash_value = 5381
    for char in key:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)
    return hash_value % table_size


def get_hash_function(name: str) -> Callable[[str, int], int]:
    """
    Фабрика хеш-функций.

    Args:
        name: Название хеш-функции.

    Returns:
        Функция хеширования.
    """
    hash_functions = {
        'simple': simple_hash,
        'polynomial': polynomial_hash,
        'djb2': djb2_hash
    }
    return hash_functions.get(name, polynomial_hash)
