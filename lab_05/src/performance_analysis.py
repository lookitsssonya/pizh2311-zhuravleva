"""Проведение экспериментов и визуализация для хеш-таблиц."""
import random
import string
import time
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from hash_table_chaining import HashTableChaining
from hash_table_open_addressing import HashTableOpenAddressing
from hash_functions import polynomial_hash, djb2_hash


def system_info() -> None:
    """Вывод информации о системе."""
    print('''
ХАРАКТЕРИСТИКИ ПК ДЛЯ ТЕСТИРОВАНИЯ:
- Процессор: Intel Core i5-13420H (2.10 GHz)
- Оперативная память: 16 GB DDR5
- ОС: Windows 11
- Python: 3.11
''')


def generate_random_string(length: int = 10) -> str:
    """Генерация случайной строки."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def measure_performance(
        table_type: str,
        hash_func: str,
        method: str = 'linear',
        load_factors: List[float] = None,
        num_operations: int = 100
) -> Dict[str, Any]:
    if load_factors is None:
        load_factors = [0.1, 0.3, 0.5, 0.7, 0.9]

    results = {
        'insert_times': [],
        'search_times': [],
        'delete_times': [],
        'load_factors': load_factors,
        'successful_operations': []
    }

    for lf in load_factors:
        print(f'Testing {table_type} with {hash_func}, load factor: {lf}')

        successful_inserts = 0
        successful_searches = 0
        successful_deletes = 0

        try:
            initial_size = 101
            if table_type == 'open':
                initial_size = 251
                max_lf = 0.75
            else:
                max_lf = 1.0

            if table_type == 'chaining':
                table = HashTableChaining(
                    size=initial_size, hash_func=hash_func,
                    max_load_factor=max_lf
                )
            else:
                table = HashTableOpenAddressing(
                    size=initial_size, method=method,
                    max_load_factor=max_lf
                )

            target_size = min(int(table.size * lf), table.size - 10)
            test_data = []

            for i in range(target_size):
                key = generate_random_string()
                value = f'value_{i}'
                table.insert(key, value)
                test_data.append(key)

            insert_times = []
            search_times = []
            delete_times = []

            for i in range(num_operations):
                key = generate_random_string()
                start_time = time.perf_counter()
                try:
                    table.insert(key, f'test_value_{i}')
                    end_time = time.perf_counter()
                    insert_times.append(end_time - start_time)
                    successful_inserts += 1
                except (ValueError, RuntimeError) as e:
                    print(f"  Insert failed: {e}")
                    continue

            search_keys = test_data[:min(num_operations, len(test_data))]
            for key in search_keys:
                start_time = time.perf_counter()
                result = table.search(key)
                end_time = time.perf_counter()
                if result is not None:
                    search_times.append(end_time - start_time)
                    successful_searches += 1

            delete_keys = test_data[:min(num_operations, len(test_data))]
            for key in delete_keys:
                start_time = time.perf_counter()
                success = table.delete(key)
                end_time = time.perf_counter()
                if success:
                    delete_times.append(end_time - start_time)
                    successful_deletes += 1

            results['insert_times'].append(
                np.mean(insert_times) * 1e6 if insert_times else 0
            )
            results['search_times'].append(
                np.mean(search_times) * 1e6 if search_times else 0
            )
            results['delete_times'].append(
                np.mean(delete_times) * 1e6 if delete_times else 0
            )

            success_msg = (
                f"Successful Inserts: {successful_inserts}/{num_operations}, "
                f"Searches: {successful_searches}/{len(search_keys)}, "
                f"Deletes: {successful_deletes}/{len(delete_keys)}"
            )
            print(success_msg)

        except (ValueError, RuntimeError, KeyError) as e:
            print(f'Error testing {table_type} with load factor {lf}: {e}')
            results['insert_times'].append(0)
            results['search_times'].append(0)
            results['delete_times'].append(0)

    return results


def calculate_probe_index(
    key: str, table_size: int, method: str, i: int
) -> int:
    """Вычисляет индекс пробы для открытой адресации."""
    if method == 'linear':
        return (polynomial_hash(key, table_size) + i) % table_size
    elif method == 'double':
        h1 = polynomial_hash(key, table_size)
        h2 = djb2_hash(key, table_size - 1) + 1
        return (h1 + i * h2) % table_size
    else:
        return (polynomial_hash(key, table_size) + i) % table_size


def run_collision_test(num_keys: int = 500) -> List[Dict[str, Any]]:
    """Тест коллизий."""
    results = []
    hash_functions = ['simple', 'polynomial', 'djb2']
    load_factors = [0.1, 0.3, 0.5, 0.7]
    print('\nStarting collision comparison...')

    for func_name in hash_functions:
        for lf in load_factors:
            table_size = max(101, int(num_keys / lf))
            while True:
                is_prime = True
                for i in range(2, int(table_size ** 0.5) + 1):
                    if table_size % i == 0:
                        is_prime = False
                        break
                if is_prime:
                    break
                table_size += 1

            test_data = [generate_random_string() for _ in range(num_keys)]

            print(f'Testing chaining: {func_name}, LF: {lf}')
            try:
                ht_chain = HashTableChaining(
                    size=table_size, hash_func=func_name
                )
                for key in test_data:
                    ht_chain.insert(key, f'value_{key}')

                chain_stats = ht_chain.get_collision_stats()
                results.append({
                    'method': 'chaining',
                    'hash_function': func_name,
                    'load_factor': lf,
                    'total_collisions': chain_stats.get('total_collisions', 0),
                    'max_chain_length': chain_stats.get('max_chain_length', 0),
                })

            except (ValueError, RuntimeError) as e:
                print(f'Error in chaining {func_name}, LF {lf}: {e}')

            print(f'Testing open addressing: {func_name}, LF: {lf}')
            try:
                ht_open = HashTableOpenAddressing(
                    size=table_size, method='linear'
                )
                total_collisions = 0

                for key in test_data:
                    i = 0
                    found_empty = False
                    insert_index = None

                    while i < ht_open.size and not found_empty:
                        probe_index = calculate_probe_index(
                            key, ht_open.size, ht_open.method, i
                        )

                        try:
                            if ht_open.search(key) is None:
                                cell = ht_open.table[probe_index]
                                if cell is None or cell == ht_open.DELETED:
                                    if i > 0:
                                        total_collisions += i
                                    found_empty = True
                                    insert_index = probe_index
                                else:
                                    i += 1
                            else:
                                i += 1
                        except (ValueError, RuntimeError, IndexError):
                            i += 1

                    if found_empty and insert_index is not None:
                        ht_open.table[insert_index] = (key, f'value_{key}')
                        ht_open.count += 1
                    elif not found_empty:
                        total_collisions += i

                results.append({
                    'method': 'open_linear',
                    'hash_function': func_name,
                    'load_factor': lf,
                    'total_collisions': total_collisions,
                })

            except (ValueError, RuntimeError) as e:
                print(f'Error in open addressing {func_name}, LF {lf}: {e}')

    return results


def plot_performance_comparison():
    """Построение графиков производительности."""
    load_factors = [0.1, 0.3, 0.5, 0.7, 0.9]

    configurations = [
        ('chaining', 'simple', 'linear', 'Метод цепочек (simple)'),
        ('chaining', 'polynomial', 'linear', 'Метод цепочек (polynomial)'),
        ('chaining', 'djb2', 'linear', 'Метод цепочек (djb2)'),
        ('open', 'polynomial', 'linear', 'Открытая адресация (linear)'),
        ('open', 'polynomial', 'double', 'Открытая адресация (double)')
    ]

    all_results = {}

    print('Starting performance comparison...')
    for table_type, hash_func, method, label in configurations:
        print(f'Testing configuration: {label}')
        results = measure_performance(
            table_type, hash_func, method, load_factors, 50
        )
        all_results[label] = results

    fig, axes = plt.subplots(1, 3, figsize=(20, 6))

    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
    markers = ['o', 's', '^', 'D', 'v']

    for idx, (label, results) in enumerate(all_results.items()):
        color = colors[idx % len(colors)]
        marker = markers[idx % len(markers)]

        insert_times = results['insert_times']
        search_times = results['search_times']
        delete_times = results['delete_times']

        axes[0].plot(
            load_factors, insert_times, marker=marker, color=color,
            label=label, markersize=6, linewidth=2, linestyle='-'
        )
        axes[1].plot(
            load_factors, search_times, marker=marker, color=color,
            label=label, markersize=6, linewidth=2, linestyle='-'
        )
        axes[2].plot(
            load_factors, delete_times, marker=marker, color=color,
            label=label, markersize=6, linewidth=2, linestyle='-'
        )

    axes[0].set_title('Время вставки', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Коэффициент заполнения', fontsize=12)
    axes[0].set_ylabel('Время (микросекунды)', fontsize=12)
    axes[0].legend(fontsize=8, loc='upper left', bbox_to_anchor=(0, 1))
    axes[0].grid(True, alpha=0.3)

    axes[1].set_title('Время поиска', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Коэффициент заполнения', fontsize=12)
    axes[1].set_ylabel('Время (микросекунды)', fontsize=12)
    axes[1].legend(fontsize=8, loc='upper left', bbox_to_anchor=(0, 1))
    axes[1].grid(True, alpha=0.3)

    axes[2].set_title('Время удаления', fontsize=14, fontweight='bold')
    axes[2].set_xlabel('Коэффициент заполнения', fontsize=12)
    axes[2].set_ylabel('Время (микросекунды)', fontsize=12)
    axes[2].legend(fontsize=8, loc='upper left', bbox_to_anchor=(0, 1))
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

    return all_results


def visualize_histograms(results: List[Dict[str, Any]]):
    """Построение гистограмм коллизий."""
    df = pd.DataFrame(results)

    plt.style.use('seaborn-v0_8')
    colors = {'simple': '#ff6b6b', 'polynomial': '#4ecdc4', 'djb2': '#45b7d1'}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    chain_data = df[df['method'] == 'chaining']
    if not chain_data.empty:
        collisions_by_hash = chain_data.groupby('hash_function')[
            'total_collisions'
        ].mean()
        colors_list = [colors.get(h, 'gray') for h in collisions_by_hash.index]

        bars1 = ax1.bar(
            collisions_by_hash.index, collisions_by_hash.values,
            color=colors_list, alpha=0.8, edgecolor='black'
        )
        ax1.set_title(
            'Среднее количество коллизий\n(Chaining)',
            fontsize=14, fontweight='bold'
        )
        ax1.set_xlabel('Хеш-функция', fontsize=12)
        ax1.set_ylabel('Количество коллизий', fontsize=12)
        ax1.grid(True, alpha=0.3, axis='y')

        for bar in bars1:
            height = bar.get_height()
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                height + max(collisions_by_hash.values) * 0.01,
                f'{int(height)}', ha='center', va='bottom',
                fontweight='bold'
            )

    open_data = df[df['method'] == 'open_linear']
    if not open_data.empty:
        collisions_by_hash = open_data.groupby('hash_function')[
            'total_collisions'
        ].mean()
        colors_list = [colors.get(h, 'gray') for h in collisions_by_hash.index]

        bars2 = ax2.bar(
            collisions_by_hash.index, collisions_by_hash.values,
            color=colors_list, alpha=0.8, edgecolor='black'
        )
        ax2.set_title(
            'Среднее количество коллизий\n(Open linear)',
            fontsize=14, fontweight='bold'
        )
        ax2.set_xlabel('Хеш-функция', fontsize=12)
        ax2.set_ylabel('Количество коллизий', fontsize=12)
        ax2.grid(True, alpha=0.3, axis='y')

        for bar in bars2:
            height = bar.get_height()
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                height + max(collisions_by_hash.values) * 0.01,
                f'{int(height)}', ha='center', va='bottom',
                fontweight='bold'
            )

    plt.tight_layout()
    plt.savefig('collisions_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()


def print_comprehensive_analysis(
    performance_results: Dict,
    collision_results: List[Dict[str, Any]]
):
    """Вывод анализа результатов."""
    print('\nАнализ производительности:')
    print('-' * 50)

    best_per_method = {}
    for operation in ['insert_times', 'search_times', 'delete_times']:
        best_method = None
        best_avg_time = float('inf')

        for method_name, results in performance_results.items():
            avg_time = np.mean(results[operation])
            if 0 < avg_time < best_avg_time:
                best_avg_time = avg_time
                best_method = method_name

        if best_method:
            op_name = operation.replace('_times', '').title()
            print(f'{op_name}: {best_method} ({best_avg_time:.6f} мкс)')
            best_per_method[operation] = (best_method, best_avg_time)

    print('\nАнализ коллизий:')
    print('-' * 50)

    df = pd.DataFrame(collision_results)

    for method in ['chaining', 'open_linear']:
        method_name = ('Метод цепочек' if method == 'chaining'
                       else 'Открытая адресация')
        method_data = df[df['method'] == method]

        if not method_data.empty:
            print(f'\n{method_name}:')
            for hash_func in ['simple', 'polynomial', 'djb2']:
                func_data = method_data[
                    method_data['hash_function'] == hash_func
                ]
                if not func_data.empty:
                    avg_collisions = func_data['total_collisions'].mean()
                    print(f'  - {hash_func}: {avg_collisions:.0f} коллизий')

    print('\nАнализ хеш-функций:')
    print('-' * 50)
    chain_data = df[df['method'] == 'chaining']
    if not chain_data.empty:
        hash_collisions = chain_data.groupby('hash_function')[
            'total_collisions'
        ].mean()
        best_hash = hash_collisions.idxmin()
        worst_hash = hash_collisions.idxmax()
        print(f'Лучшая: {best_hash} (наименьшее количество коллизий)')
        print(f'Худшая: {worst_hash} (наибольшее количество коллизий)')


def main():
    """Основная функция запуска анализа."""
    system_info()

    performance_results = plot_performance_comparison()

    collision_results = run_collision_test()

    visualize_histograms(collision_results)

    print_comprehensive_analysis(performance_results, collision_results)

    print('\nРезультаты сохранены в файлах:')
    print('performance_comparison.png (графики производительности)')
    print('collisions_comparison.png (гистограммы коллизий)')


if __name__ == '__main__':
    main()
