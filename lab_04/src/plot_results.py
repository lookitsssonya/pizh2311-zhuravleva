"""Модуль для визуализации результатов тестирования."""

import matplotlib.pyplot as plt
from typing import Dict, Any
import numpy as np
import csv


def plot_time_vs_size(
    results_data: Dict[str, Any],
    data_type: str = 'random'
) -> None:
    """
    Строит график зависимости времени выполнения от размера массива.
    """
    plt.figure(figsize=(12, 8))

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    markers = ['o', 's', '^', 'D', 'v']

    for i, (algo_name, data_types_data) in enumerate(results_data.items()):
        if data_type in data_types_data:
            sizes = []
            times = []

            for size, time_taken in data_types_data[data_type].items():
                sizes.append(size)
                times.append(time_taken)

            sorted_indices = np.argsort(sizes)
            sizes_sorted = [sizes[i] for i in sorted_indices]
            times_sorted = [times[i] for i in sorted_indices]

            plt.plot(
                sizes_sorted,
                times_sorted,
                marker=markers[i],
                label=algo_name,
                linewidth=2,
                color=colors[i],
                markersize=6
            )

    plt.xlabel('Размер массива')
    plt.ylabel('Время выполнения (секунды)')
    plt.title('Зависимость времени выполнения от размера массива\n'
              f'({data_type} данные)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.xticks([100, 1000, 5000, 10000])
    plt.yscale('log')

    plt.tight_layout()
    plt.savefig(f'time_vs_size_{data_type}.png', dpi=300)
    plt.show()


def plot_time_vs_datatype(
    results_data: Dict[str, Any],
    size: int = 5000
) -> None:
    """
    Строит график зависимости времени выполнения от типа данных.
    """
    plt.figure(figsize=(12, 8))

    data_types = ['random', 'sorted', 'reversed', 'almost_sorted']

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    markers = ['o', 's', '^', 'D', 'v']

    for i, (algo_name, data_types_data) in enumerate(results_data.items()):
        times = []

        for data_type in data_types:
            if (data_type in data_types_data and
                    size in data_types_data[data_type]):
                times.append(data_types_data[data_type][size])

        if times:
            plt.plot(
                data_types,
                times,
                marker=markers[i],
                label=algo_name,
                linewidth=2,
                color=colors[i],
                markersize=8
            )

    plt.xlabel('Тип данных')
    plt.ylabel('Время выполнения (секунды)')
    plt.title(
        'Зависимость времени выполнения от типа данных\n'
        f'(размер массива: {size} элементов)'
    )
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')

    plt.tight_layout()
    plt.savefig(f'time_vs_datatype_size_{size}.png', dpi=300)
    plt.show()


def create_summary_table(results_data: Dict[str, Any]) -> str:
    """Создает сводную таблицу результатов."""
    table = "\nСводная таблица результатов\n"

    sizes = [100, 1000, 5000, 10000]
    data_types = ['random', 'sorted', 'reversed', 'almost_sorted']

    for data_type in data_types:
        table += f"{data_type.upper()}:\n"
        table += "-" * 60 + "\n"

        header = "Алгоритм" + " " * 10
        for size in sizes:
            header += f"{size:<8}"
        table += header + "\n"
        table += "-" * 60 + "\n"

        for algo_name in results_data.keys():
            if data_type in results_data[algo_name]:
                row = f"{algo_name:<15}"
                for size in sizes:
                    if size in results_data[algo_name][data_type]:
                        time_val = results_data[algo_name][data_type][size]
                        row += f"{time_val:>8.4f}"
                    else:
                        row += " " * 8
                table += row + "\n"
        table += "\n"

    return table


def save_results_to_csv(
    results_data: Dict[str, Any],
    filename: str = 'results_detailed.csv'
) -> None:
    """Сохраняет детальные результаты в CSV."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['Алгоритм', 'Тип данных', 'Размер', 'Время (сек)'])

        for algo_name, data_types_data in results_data.items():
            for data_type, sizes_data in data_types_data.items():
                for size, time_val in sizes_data.items():
                    row = [
                        algo_name, data_type, size, f"{time_val:.6f}"
                    ]
                    writer.writerow(row)


def main() -> None:
    """Основная функция."""
    from performance_test import run_performance_tests

    test_results = run_performance_tests()

    plot_time_vs_size(test_results, 'random')

    plot_time_vs_datatype(test_results, 5000)

    summary_table = create_summary_table(test_results)
    print(summary_table)

    save_results_to_csv(test_results)

    print("Результаты сохранены в файлы:")
    print("- results_detailed.csv")
    print("- time_vs_size_random.png")
    print("- time_vs_datatype_size_5000.png")


if __name__ == '__main__':
    main()
