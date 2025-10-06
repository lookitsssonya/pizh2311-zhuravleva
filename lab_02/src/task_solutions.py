import collections
from typing import Deque, List


def check_brackets_balance(expression: str) -> bool:
    """
    Проверка сбалансированности скобок с использованием стека.

    Сложность: O(n) - каждый символ обрабатывается один раз

    Args:
        expression: Строка со скобками для проверки.

    Returns:
        bool: True если скобки сбалансированы, иначе False.
    """
    stack: List[str] = []  # O(1) - создание стека
    brackets_map = {'(': ')', '[': ']', '{': '}'}  # O(1) - создание словаря

    for char in expression:  # O(n) - цикл по всем символам
        if char in brackets_map:  # O(1) - проверка в словаре
            stack.append(char)  # O(1) - добавление в стек
        elif char in brackets_map.values():  # O(1) - проверка в значениях
            if not stack:  # O(1) - проверка пустоты стека
                return False  # O(1) - возврат при ошибке
            last_open = stack.pop()  # O(1) - извлечение из стека
            if brackets_map[last_open] != char:  # O(1) - сравнение скобок
                return False  # O(1) - возврат при несоответствии

    return len(stack) == 0  # O(1) - проверка пустоты стека


def print_queue_simulation(tasks: List[str]) -> List[str]:
    """
    Симуляция обработки задач в очереди печати.

    Сложность: O(n) - каждая задача обрабатывается один раз

    Args:
        tasks: Список задач для обработки.

    Returns:
        List[str]: Список обработанных задач в порядке обработки.
    """
    queue: Deque[str] = collections.deque(tasks)  # O(n) - создание очереди
    processed: List[str] = []  # O(1) - создание списка результатов

    print('\n=== СИМУЛЯЦИЯ ОЧЕРЕДИ ПЕЧАТИ ===')
    print(f'Начальная очередь: {list(queue)}')

    task_number = 1  # O(1) - инициализация счетчика
    while queue:  # O(n) - цикл по всем задачам
        current_task = queue.popleft()  # O(1) - извлечение из очереди
        status = f'{task_number}. Обработана: {current_task}'
        processed.append(status)  # O(1) - добавление в результаты
        print(status)  # O(1) - вывод
        task_number += 1  # O(1) - инкремент счетчика

        if queue:  # O(1) - проверка очереди
            print(f'   Очередь: {list(queue)}')
        else:
            print('   Очередь пуста')  # O(1) - вывод

    return processed  # O(1) - возврат результатов


def is_palindrome(sequence: str) -> bool:
    """
    Проверка, является ли последовательность палиндромом с использованием дека.

    Сложность: O(n) - каждый символ обрабатывается один раз

    Args:
        sequence: Проверяемая последовательность.

    Returns:
        bool: True если последовательность является палиндромом, иначе False.
    """
    # Очистка строки - O(n)
    cleaned_sequence = ''.join(  # O(n) - объединение символов
        char.lower() for char in sequence if char.isalnum()  # O(n) - фильтр
    )

    if not cleaned_sequence:  # O(1) - проверка пустоты
        return True  # O(1) - возврат для пустой строки

    deq: Deque[str] = collections.deque(cleaned_sequence)  # O(n) - дек

    while len(deq) > 1:  # O(n) - цикл до середины строки
        if deq.popleft() != deq.pop():  # O(1) - сравнение с двух концов
            return False  # O(1) - возврат при несовпадении

    return True  # O(1) - возврат при успехе


def demonstrate_brackets_balance() -> None:
    """Демонстрация проверки сбалансированности скобок."""
    print('\n=== ПРОВЕРКА СБАЛАНСИРОВАННОСТИ СКОБОК ===')

    test_expressions = [
        "((()))",  # Сбалансированы
        "([{}])",  # Сбалансированы
        "({[}])",  # Не сбалансированы
        "((())",  # Не сбалансированы
        "())(",  # Не сбалансированы
        "abc(def[ghi]jkl)",  # Со смешанным содержимым
    ]

    for expr in test_expressions:
        result = check_brackets_balance(expr)
        status = "Сбалансированы" if result else "Не сбалансированы"
        print(f'"{expr}" -> {status}')


def demonstrate_palindrome_check() -> None:
    """Демонстрация проверки палиндромов."""
    print('\n=== ПРОВЕРКА ПАЛИНДРОМОВ ===')

    test_sequences = [
        "А роза упала на лапу Азора",
        "racecar",
        "hello",
        "Madam",
        "Was it a car or a cat I saw",
        "12321",
        "345643",
        "not a palindrome",
    ]

    for seq in test_sequences:
        result = is_palindrome(seq)
        status = "Палиндром" if result else "Не палиндром"
        display_seq = seq if len(seq) <= 30 else seq[:27] + "..."
        print(f'"{display_seq}" -> {status}')


def demonstrate_all_solutions() -> None:
    """Демонстрация всех решений задач."""
    print('\n=== РЕШЕНИЕ ПРАКТИЧЕСКИХ ЗАДАЧ ===')

    demonstrate_brackets_balance()

    tasks = [
        'doc1.pdf',
        'doc2.pdf',
        'report.docx',
        'image.png',
        'presentation.ppt'
    ]
    print_queue_simulation(tasks)

    demonstrate_palindrome_check()


if __name__ == '__main__':
    demonstrate_all_solutions()
