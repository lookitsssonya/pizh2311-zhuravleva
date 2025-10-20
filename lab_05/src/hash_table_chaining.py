"""Реализация хеш-таблицы с методом цепочек."""
from typing import Any, List, Optional, Tuple


class HashTableChaining:
    """Хеш-таблица с разрешением коллизий методом цепочек."""

    def __init__(
        self, size: int = 101, hash_func: str = 'polynomial',
        max_load_factor: float = 0.9
    ) -> None:
        """
        Инициализация хеш-таблицы.

        Args:
            size: Начальный размер таблицы (простое число).
            hash_func: Используемая хеш-функция.
            max_load_factor: Максимальный коэффициент заполнения.
        """
        self.size: int = size
        self.count: int = 0
        self.max_load_factor: float = max_load_factor
        self.table: List[List[Tuple[str, Any]]] = [[] for _ in range(size)]
        self.hash_func_name: str = hash_func

        from hash_functions import get_hash_function
        self.hash_func = get_hash_function(hash_func)

    def _hash(self, key: str) -> int:
        """Вычисление хеша для ключа."""
        return self.hash_func(key, self.size)

    def _resize(self) -> None:
        """Увеличение размера таблицы при необходимости."""
        if self.load_factor <= self.max_load_factor:
            return

        new_size = self.size * 2
        while not self._is_prime(new_size):
            new_size += 1

        new_table = [[] for _ in range(new_size)]

        old_table = self.table
        self.table = new_table
        self.size = new_size
        self.count = 0

        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)

    @staticmethod
    def _is_prime(n: int) -> bool:
        """Проверка, является ли число простым."""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True

    @property
    def load_factor(self) -> float:
        """Коэффициент заполнения таблицы."""
        return self.count / self.size

    def insert(self, key: str, value: Any) -> None:
        """
        Вставка элемента в таблицу.

        Args:
            key: Ключ.
            value: Значение.

        Time Complexity:
            Средний случай: O(1 + α).
            Худший случай: O(n).
        """
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.count += 1
        self._resize()

    def search(self, key: str) -> Optional[Any]:
        """
        Поиск элемента по ключу.

        Args:
            key: Ключ для поиска.

        Returns:
            Значение или None, если ключ не найден.

        Time Complexity:
            Средний случай: O(1 + α).
            Худший случай: O(n).
        """
        index = self._hash(key)
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key: str) -> bool:
        """
        Удаление элемента по ключу.

        Args:
            key: Ключ для удаления.

        Returns:
            True если элемент удален, False если не найден.

        Time Complexity:
            Средний случай: O(1 + α).
            Худший случай: O(n).
        """
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                return True
        return False

    def __contains__(self, key: str) -> bool:
        """Проверка наличия ключа в таблице."""
        return self.search(key) is not None

    def __getitem__(self, key: str) -> Any:
        """Получение значения по ключу."""
        value = self.search(key)
        if value is None:
            raise KeyError(f'Key "{key}" not found')
        return value

    def __setitem__(self, key: str, value: Any) -> None:
        """Установка значения по ключу."""
        self.insert(key, value)

    def get_collision_stats(self) -> dict:
        """Статистика коллизий."""
        collisions = 0
        max_chain_length = 0
        non_empty_buckets = 0

        for bucket in self.table:
            if len(bucket) > 0:
                non_empty_buckets += 1
                if len(bucket) > 1:
                    collisions += len(bucket) - 1
                if len(bucket) > max_chain_length:
                    max_chain_length = len(bucket)

        return {
            'total_collisions': collisions,
            'max_chain_length': max_chain_length,
            'non_empty_buckets': non_empty_buckets,
            'load_factor': self.load_factor
        }
