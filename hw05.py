# Завдання 5. Візуалізація обходу бінарного дерева в глибину та в ширину.

from collections import deque

import matplotlib.pyplot as plt
import networkx as nx
from tabulate import tabulate

from min_heap import MinHeap
from hw04 import heap_to_tree, add_edges
from utils import save_figure


def get_color(step: int, total: int) -> tuple[str, str]:
    t = step / max(total - 1, 1)

    red = round(25 + 160 * t)
    green = round(65 + 155 * t)
    blue = round(110 + 130 * t)

    color = f"#{red:02X}{green:02X}{blue:02X}"

    # щоб підписи були читабельними на темних вузлах, визначаємо колір тексту
    # по формулі розрвхунку контрастної яскравості: Y = 0.299 * R + 0.587 * G + 0.114 * B
    fore_color = "white" if (0.299 * red + 0.587 * green + 0.114 * blue) < 135 else "black"

    return color, fore_color
    

# Обходить дерево в глибину за допомогою стека (корінь, ліво, право).
def dfs(root):
    if root is None:
        return []

    stack = [root]
    visited = []

    while stack:
        node = stack.pop()
        visited.append(node)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)

    for step, node in enumerate(visited):
        node.color, node.fore_color = get_color(step, len(visited))
    return [node.val for node in visited]

# Обходить дерево в ширину за допомогою черги.
def bfs(root):

    if root is None:
        return []

    queue = deque([root])
    visited = []

    while queue:
        node = queue.popleft()
        visited.append(node)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)

    for step, node in enumerate(visited):
        node.color, node.fore_color = get_color(step, len(visited))
    return [node.val for node in visited]


# Візуалізує обхід дерева та зберігає зображення.
def draw_traversal(root, title: str, filename: str):
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(tree, root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]

    plt.figure(figsize=(9, 6))

    nx.draw(
        tree, pos=pos, arrows=False,
        node_size=1800, node_color=colors, edgecolors="gray",
    )

    for node_id, data in tree.nodes(data=True):
        nx.draw_networkx_labels(
            tree, pos,
            labels={node_id: data["label"]},
            font_color=data["fore_color"],
            font_size=11,
        )

    plt.title(title)
    plt.get_current_fig_manager().set_window_title(title)
    save_figure(plt.gcf(), filename)




def main():
    values = [10, 3, 7, 1, 5, 8, 2, 4, 6]
    heap = MinHeap(values)
    print("Купа:")
    print(heap)

    root = heap_to_tree(heap.items)

    dfs_order = dfs(root)
    draw_traversal(root, "Обхід дерева в глибину (DFS)", "dfs_traversal.png")

    bfs_order = bfs(root)
    draw_traversal(root, "Обхід дерева в ширину (BFS)", "bfs_traversal.png")

    print("\nПорядок відвідування вузлів:")
    print(tabulate(
        [[i + 1, dfs_order[i], bfs_order[i]] for i in range(len(dfs_order))],
        headers=["Крок", "DFS", "BFS"], tablefmt="github",
    ))
    plt.show()
    plt.close("all")


if __name__ == "__main__":
    main()
