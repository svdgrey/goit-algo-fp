# Завдання 7. Використання методу Монте-Карло.

import random
from utils import save_figure

import matplotlib.pyplot as plt
from tabulate import tabulate

# Обчислює теоретичні ймовірності сум двох кубиків.
def theoretical_probabilities() -> dict[int, float]:
    return {total: (6 - abs(7 - total)) / 36 for total in range(2, 13)}


# Моделює кидки двох кубиків методом Монте-Карло.
def monte_carlo_probabilities(trials: int) -> dict[int, float]:
    counts = {total: 0 for total in range(2, 13)}

    for _ in range(trials):
        total = random.randint(1, 6) + random.randint(1, 6)
        counts[total] += 1

    return {total: count / trials for total, count in counts.items()}


# Будує графік порівняння теоретичних та експериментальних ймовірностей.
def draw_probabilities(theoretical: dict[int, float], simulated: dict[int, float]):
    sums = list(theoretical)
    theoretical_percent = [theoretical[total] * 100 for total in sums]
    simulated_percent = [simulated[total] * 100 for total in sums]

    plt.figure(figsize=(9, 5))
    plt.plot(sums, theoretical_percent, marker="o", label="Теоретична")
    plt.plot(sums, simulated_percent, marker="x", linestyle="--", label="Монте-Карло")
    plt.xticks(sums)
    plt.xlabel("Сума двох кубиків")
    plt.ylabel("Ймовірність, %")

    title = "Порівняння ймовірностей сум двох кубиків"
    plt.get_current_fig_manager().set_window_title(title)
    plt.title(title)
    plt.legend()
    plt.grid(alpha=0.3)

    save_figure(plt.gcf(), "dice_probabilities.png")
    
    plt.show()
    plt.close()


def main():
    trials = 100_000
    theoretical = theoretical_probabilities()
    simulated = monte_carlo_probabilities(trials)

    assert abs(sum(theoretical.values()) - 1) < 1e-12
    assert abs(sum(simulated.values()) - 1) < 1e-12

    results = [
        [total, f"{theoretical[total] * 100:.2f}%", f"{simulated[total] * 100:.2f}%",
         f"{abs(simulated[total] - theoretical[total]) * 100:.2f}"]
        for total in theoretical
    ]

    print(f"Кількість кидків: {trials}\n")
    print(tabulate(
        results,
        headers=["Сума", "Теоретична", "Монте-Карло", "Відхилення, в.п."],
        tablefmt="github",
    ))

    draw_probabilities(theoretical, simulated)


if __name__ == "__main__":
    main()
