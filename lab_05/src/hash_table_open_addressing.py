"""Реализация хеш-таблицы с открытой адресацией."""
from typing import Any, List, Optional

from hash_functions import djb2_hash, polynomial_hash


class HashTableOpenAddressing:
    """Хеш-таблица с разрешением коллизий методом открытой адресации."""

    DELETED = object()

    def __init__(
        self, size: int = 101, method: str = 'linear',
        max_load_factor: float = 0.9
    ) -> None:
        """
        Инициализация хеш-таблицы.

        Args:
            size: Начальный размер таблицы (простое число).
            method: Метод разрешения коллизий ('linear', 'double').
            max_load_factor: Максимальный коэффициент заполнения.
        """
        self.size: int = size
        self.count: int = 0
        self.deleted_count: int = 0
        self.max_load_factor: float = max_load_factor
        self.method: str = method
        self.table: List[Optional[Any]] = [None] * size

    def _hash1(self, key: str) -> int:
        """Первая хеш-функция."""
        return polynomial_hash(key, self.size)

    def _hash2(self, key: str) -> int:
        """Вторая хеш-функция для двойного хеширования."""
        hash_val = djb2_hash(key, self.size - 1) + 1
        return hash_val

    def _probe_sequence(self, key: str, i: int) -> int:
        """
        Последовательность проб для разрешения коллизий.

        Args:
            key: Ключ.
            i: Номер попытки.

        Returns:
            Индекс в таблице.
        """
        if self.method == 'linear':
            return (self._hash1(key) + i) % self.size
        elif self.method == 'double':
            h1 = self._hash1(key)
            h2 = self._hash2(key)
            return (h1 + i * h2) % self.size
        else:
            raise ValueError(f'Unknown method: {self.method}')

    def _resize(self) -> None:
        """Увеличение размера таблицы при необходимости."""
        current_load = self.count / self.size
        if current_load <= self.max_load_factor:
            return

        new_size = self.size * 2 + 1
        while not self._is_prime(new_size):
            new_size += 1

        old_table = self.table

        self.table = [None] * new_size
        self.size = new_size
        self.count = 0
        self.deleted_count = 0

        for item in old_table:
            if item is not None and item != self.DELETED:
                key, value = item
                self._insert_direct(key, value)

    def _insert_direct(self, key: str, value: Any) -> None:
        """Прямая вставка без проверки ресайза."""
        i = 0
        while i < self.size:
            index = self._probe_sequence(key, i)

            is_empty_or_deleted = (
                self.table[index] is None or
                self.table[index] == self.DELETED
            )
            if is_empty_or_deleted:
                self.table[index] = (key, value)
                self.count += 1
                return

            is_same_key = (
                isinstance(self.table[index], tuple) and
                len(self.table[index]) == 2 and
                self.table[index][0] == key
            )
            if is_same_key:
                self.table[index] = (key, value)
                return

            i += 1

        raise RuntimeError('Hash table is full and resize did not happen')

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
        return (self.count + self.deleted_count) / self.size

    def insert(self, key: str, value: Any) -> None:
        """
        Вставка элемента в таблицу.

        Args:
            key: Ключ.
            value: Значение.

        Time Complexity:
            Средний случай: O(1 / (1 - α)).
            Худший случай: O(n).
        """
        if self.count / self.size >= self.max_load_factor:
            self._resize()

        self._insert_direct(key, value)

    def search(self, key: str) -> Optional[Any]:
        """
        Поиск элемента по ключу.

        Args:
            key: Ключ для поиска.

        Returns:
            Значение или None, если ключ не найден.

        Time Complexity:
            Средний случай: O(1 / (1 - α)).
            Худший случай: O(n).
        """
        i = 0
        while i < self.size:
            index = self._probe_sequence(key, i)

            if self.table[index] is None:
                return None

            is_valid_item = (
                self.table[index] != self.DELETED and
                isinstance(self.table[index], tuple) and
                len(self.table[index]) == 2 and
                self.table[index][0] == key
            )
            if is_valid_item:
                return self.table[index][1]

            i += 1

        return None

    def delete(self, key: str) -> bool:
        """
        Удаление элемента по ключу.

        Args:
            key: Ключ для удаления.

        Returns:
            True если элемент удален, False если не найден.

        Time Complexity:
            Средний случай: O(1 / (1 - α)).
            Худший случай: O(n).
        """
        i = 0
        while i < self.size:
            index = self._probe_sequence(key, i)

            if self.table[index] is None:
                return False

            is_valid_item = (
                self.table[index] != self.DELETED and
                isinstance(self.table[index], tuple) and
                len(self.table[index]) == 2 and
                self.table[index][0] == key
            )
            if is_valid_item:
                self.table[index] = self.DELETED
                self.count -= 1
                self.deleted_count += 1

                if self.deleted_count > self.count:
                    self._resize()

                return True

            i += 1

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
        total_probes = 0
        successful_searches = 0

        for item in self.table:
            is_valid_item = (
                item is not None and
                item != self.DELETED and
                isinstance(item, tuple)
            )
            if is_valid_item:
                key, value = item
                probes = 0
                found = False

                while probes < self.size and not found:
                    index = self._probe_sequence(key, probes)
                    is_target_item = (
                        self.table[index] is not None and
                        self.table[index] != self.DELETED and
                        isinstance(self.table[index], tuple) and
                        self.table[index][0] == key
                    )
                    if is_target_item:
                        total_probes += probes + 1
                        successful_searches += 1
                        found = True
                    probes += 1

        avg_probes = (
            total_probes / successful_searches
            if successful_searches > 0 else 0
        )

        return {
            'avg_probes': avg_probes,
            'load_factor': self.count / self.size,
            'cluster_size': self._get_max_cluster_size(),
            'deleted_count': self.deleted_count
        }

    def _get_max_cluster_size(self) -> int:
        """Размер максимального кластера (последовательных занятых ячеек)."""
        max_cluster = 0
        current_cluster = 0

        for item in self.table:
            if item is not None and item != self.DELETED:
                current_cluster += 1
                max_cluster = max(max_cluster, current_cluster)
            else:
                current_cluster = 0

        return max_cluster
