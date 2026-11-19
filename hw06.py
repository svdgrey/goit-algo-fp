# Завдання 6. Жадібні алгоритми та динамічне програмування.
from tabulate import tabulate


dishes = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


# Вибирає страви за спаданням співвідношення калорійності до вартості.
def greedy_algorithm(dishes: dict, budget: int) -> list[str]:
    sorted_dishes = sorted(
        dishes,
        key=lambda name: dishes[name]["calories"] / dishes[name]["cost"],
        reverse=True,
    )

    selected = []
    for name in sorted_dishes:
        cost = dishes[name]["cost"]
        if cost <= budget:
            selected.append(name)
            budget -= cost

    return selected


# Знаходить оптимальний набір страв методом динамічного програмування.
def dynamic_programming(dishes: dict, budget: int) -> list[str]:
    names = list(dishes)
    n = len(names)
    
    max_calories_by_budget = [
        [0] * (budget + 1) 
        for _ in range(n + 1)
    ]

    for i, name in enumerate(names, start=1):
        cost = dishes[name]["cost"]
        calories = dishes[name]["calories"]
        for b in range(budget + 1):
            max_calories_by_budget[i][b] = max_calories_by_budget[i - 1][b]
            if cost <= b:
                max_calories_by_budget[i][b] = max(max_calories_by_budget[i][b], max_calories_by_budget[i - 1][b - cost] + calories)

    selected = []
    b = budget
    for i in range(n, 0, -1):
        if max_calories_by_budget[i][b] != max_calories_by_budget[i - 1][b]:
            name = names[i - 1]
            selected.append(name)
            b -= dishes[name]["cost"]

    return selected[::-1]


def main():
    budget = 100
    print(f"Бюджет: {budget}\n")

    algorithms = [
        ("Жадібний алгоритм", greedy_algorithm),
        ("Динамічне програмування", dynamic_programming),
    ]

    results = []
    for title, algorithm in algorithms:

        selected = algorithm(dishes, budget)
        total_cost = sum(dishes[name]["cost"] for name in selected)
        total_calories = sum(dishes[name]["calories"] for name in selected)
        assert total_cost <= budget
        assert len(selected) == len(set(selected))
        results.append([title, ", ".join(selected), total_cost, total_calories])

    assert results[1][3] >= results[0][3]

    print(tabulate(
        results,
        headers=["Алгоритм", "Обрані страви", "Вартість", "Калорійність"],
        tablefmt="github",
    ))


if __name__ == "__main__":
    main()
