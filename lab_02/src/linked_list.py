from typing import Any, Optional, List


class Node:
    """Узел связного списка."""

    def __init__(self, data: Any) -> None:
        """
        Инициализация узла.

        Args:
            data: Данные для хранения в узле.
        """
        self.data: Any = data
        self.next: Optional['Node'] = None


class LinkedList:
    """Связный список"""

    def __init__(self) -> None:
        """Инициализация пустого списка."""
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """
        Проверка на пустоту списка.

        Returns:
            bool: True если список пуст, иначе False.
        """
        return self.head is None

    def size(self) -> int:
        """
        Получение размера списка.

        Returns:
            int: Количество элементов в списке.
        """
        return self._size

    def insert_at_start(self, data: Any) -> None:
        """
        Вставка элемента в начало списка.

        Сложность: O(1)

        Args:
            data: Данные для вставки.
        """
        new_node = Node(data)  # O(1) - создание узла
        if self.is_empty():  # O(1) - проверка пустоты
            self.head = new_node  # O(1) - установка головы
            self.tail = new_node  # O(1) - установка хвоста
        else:
            new_node.next = self.head  # O(1) - обновление указателя
            self.head = new_node  # O(1) - обновление головы
        self._size += 1  # O(1) - инкремент счетчика

    def insert_at_end(self, data: Any) -> None:
        """
        Вставка элемента в конец списка.

        Сложность: O(1)

        Args:
            data: Данные для вставки.
        """
        new_node = Node(data)  # O(1) - создание узла
        if self.is_empty():  # O(1) - проверка пустоты
            self.head = new_node  # O(1) - установка головы
            self.tail = new_node  # O(1) - установка хвоста
        else:
            if self.tail:  # O(1) - проверка хвоста
                self.tail.next = new_node  # O(1) - обновление указателя
            self.tail = new_node  # O(1) - обновление хвоста
        self._size += 1  # O(1) - инкремент счетчика

    def delete_from_start(self) -> Optional[Any]:
        """
        Удаление элемента из начала списка.

        Сложность: O(1)

        Returns:
            Optional[Any]: Удаленные данные или None если список пуст.
        """
        if self.is_empty():  # O(1) - проверка пустоты
            return None  # O(1) - возврат None

        data = self.head.data if self.head else None  # O(1) - получение данных

        if self.head == self.tail:  # O(1) - проверка одного элемента
            self.head = None  # O(1) - обнуление головы
            self.tail = None  # O(1) - обнуление хвоста
        else:
            self.head = self.head.next if self.head else None  # O(1)

        self._size -= 1  # O(1) - декремент счетчика
        return data  # O(1) - возврат данных

    def traversal(self) -> List[Any]:
        """
        Обход списка и возврат всех элементов.

        Сложность: O(n)

        Returns:
            List[Any]: Список всех элементов в порядке обхода.
        """
        elements: List[Any] = []  # O(1) - создание списка
        current = self.head  # O(1) - установка текущего узла
        while current:  # O(n) - цикл по всем элементам
            elements.append(current.data)  # O(1) - добавление в список
            current = current.next  # O(1) - переход к следующему
        return elements  # O(1) - возврат результата

    def search(self, data: Any) -> bool:
        """
        Поиск элемента в списка.

        Сложность: O(n)

        Args:
            data: Искомые данные.

        Returns:
            bool: True если элемент найден, иначе False.
        """
        current = self.head  # O(1) - установка текущего узла
        while current:  # O(n) - цикл по всем элементам
            if current.data == data:  # O(1) - сравнение данных
                return True  # O(1) - возврат при нахождении
            current = current.next  # O(1) - переход к следующему
        return False  # O(1) - возврат при отсутствии

    def __str__(self) -> str:
        """Строковое представление списка."""
        elements = self.traversal()
        if not elements:
            return 'LinkedList: пуст'
        return ' -> '.join(map(str, elements)) + ' -> None'

    def __len__(self) -> int:
        """Получение длины списка."""
        return self._size


def demonstrate_linked_list() -> None:
    """Демонстрация работы связного списка."""
    print('=== ДЕМОНСТРАЦИЯ СВЯЗНОГО СПИСКА ===')

    ll = LinkedList()
    print(f'Создан пустой список: {ll}')
    print(f'Размер: {len(ll)}, Пуст: {ll.is_empty()}')

    print('\n1. Вставка в начало:')
    for i in range(3):
        ll.insert_at_start(i)
        print(f'   После вставки {i}: {ll}')

    print('\n2. Вставка в конец:')
    for i in range(3, 6):
        ll.insert_at_end(i)
        print(f'   После вставки {i}: {ll}')

    print('\n3. Поиск элементов:')
    test_values = [0, 5, 10]
    for val in test_values:
        found = ll.search(val)
        print(f'   Элемент {val}: {"найден" if found else "не найден"}')

    print('\n4. Удаление из начала:')
    while not ll.is_empty():
        removed = ll.delete_from_start()
        print(f'   Удален: {removed}, Текущий список: {ll}')

    print(f'\nИтоговый размер: {len(ll)}')


if __name__ == '__main__':
    demonstrate_linked_list()
