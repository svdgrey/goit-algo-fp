# Завдання 4. Візуалізація бінарної купи.
import uuid

import matplotlib.pyplot as plt
import networkx as nx

from min_heap import MinHeap
from utils import save_figure

class Node:
    def __init__(self, key: int, color: str = "skyblue", fore_color: str = "black"):
        self.left: Node | None = None
        self.right: Node | None = None
        self.val = key
        self.color = color
        self.fore_color = fore_color
        self.id = str(uuid.uuid4())


# Перетворює список, що представляє купу, на двійкове дерево.
def heap_to_tree(heap: list[int]) -> Node | None:
    if not heap:
        return None

    nodes = [Node(value) for value in heap]
    for i, node in enumerate(nodes):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(nodes):
            node.left = nodes[left]
        if right < len(nodes):
            node.right = nodes[right]

    return nodes[0]


# Додає вузли та ребра дерева до графа NetworkX.
def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(
            node.id,
            color=node.color,
            fore_color=node.fore_color,
            label=node.val,
        )

        if node.left:
            graph.add_edge(node.id, node.left.id)
            left_x = x - 1 / 2 ** layer
            pos[node.left.id] = (left_x, y - 1)
            add_edges(graph, node.left, pos, x=left_x, y=y - 1, layer=layer + 1)

        if node.right:
            graph.add_edge(node.id, node.right.id)
            right_x = x + 1 / 2 ** layer
            pos[node.right.id] = (right_x, y - 1)
            add_edges(graph, node.right, pos, x=right_x, y=y - 1, layer=layer + 1)

    return graph


# Візуалізує бінарну купу та зберігає зображення для README.
def draw_tree(tree_root: Node | None, title: str):
    if tree_root is None:
        print("Купа порожня")
        return

    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {node_id: data["label"] for node_id, data in tree.nodes(data=True)}

    plt.figure(figsize=(9, 6))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=1800,
            node_color=colors, edgecolors="gray", font_size=11)
    
    plt.title(title)
    plt.get_current_fig_manager().set_window_title(title)

    save_figure(plt.gcf(), "heap_visualization.png")
    plt.show()
    plt.close()


def main():
    values = [10, 3, 7, 1, 5, 8, 2, 4, 6]
    print(f"Початковий список: {values}")

    heap = MinHeap(values)
    print("Мінімальна купа:")
    print(heap)

    root = heap_to_tree(heap.items)
    draw_tree(root, "Мінімальна бінарна купа")


if __name__ == "__main__":
    main()
