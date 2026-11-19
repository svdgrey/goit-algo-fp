# Завдання 2. Рекурсивне створення фрактала "Дерево Піфагора" за допомогою рекурсії.
from math import cos, radians, sin

import matplotlib.pyplot as plt

from utils import save_figure

# Рекурсивно малює фрактальне дерево з двох гілок на кожному рівні.
def draw_pythagoras_tree(ax, x, y, length, angle, level):
    if level == 0:
        return

    # Обчислюємо кінцеву точку поточної гілки.
    end_x = x + length * cos(radians(angle))
    end_y = y + length * sin(radians(angle))

    # Малюємо поточну гілку.
    ax.plot([x, end_x], [y, end_y], color="firebrick", linewidth=1.2)

    # Кожна наступна гілка коротша за попередню.
    next_length = length * 0.7

    # Рекурсивно створюємо ліву та праву гілки.
    draw_pythagoras_tree(ax, end_x, end_y, next_length, angle + 45, level - 1)
    draw_pythagoras_tree(ax, end_x, end_y, next_length, angle - 45, level - 1)


def main():
    try:
        level = int(input("Введіть рівень рекурсії (0-10): "))
        if not 0 <= level <= 10:
            raise ValueError
    except ValueError:
        print("Помилка: введіть ціле число від 0 до 10.")
        return

    fig, ax = plt.subplots(figsize=(10, 10))
    draw_pythagoras_tree(ax, 0, 0, 1, 90, level)

    ax.set_aspect("equal", adjustable="datalim")
    ax.autoscale_view()
    ax.margins(0.06)
    ax.axis("off")
    
    title = f"Дерево Піфагора (рівень рекурсії: {level})"
    plt.get_current_fig_manager().set_window_title(title)
    ax.set_title(title)

    save_figure(fig, "pythagoras_tree.png", dpi=150)
    
    plt.show()

if __name__ == "__main__":
    main()
