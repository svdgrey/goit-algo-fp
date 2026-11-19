# Завдання 3. Алгоритм Дейкстри з використанням бінарної купи.
import heapq

from tabulate import tabulate
from min_heap import MinHeap

class StandardHeap:
    def __init__(self):
        self.items = []

    def __bool__(self):
        return bool(self.items)

    def push(self, value):
        heapq.heappush(self.items, value)

    def pop(self):
        return heapq.heappop(self.items)


# Знаходить найкоротші відстані та попередників вершин.
def dijkstra(graph: dict[str, dict[str, int]], start: str, heap_class=StandardHeap):

    if start not in graph:
        raise ValueError("Початкова вершина відсутня у графі")

    distances = {vertex: float("inf") for vertex in graph}
    previous = {vertex: None for vertex in graph}
    distances[start] = 0

    heap = heap_class()
    heap.push((0, start))

    while heap:
        current_distance, current_vertex = heap.pop()

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            if weight < 0:
                raise ValueError("Алгоритм Дейкстри не підтримує від'ємні ваги")

            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                heap.push((distance, neighbor))

    return distances, previous

# Відновлює шлях від початкової вершини до заданої.
def restore_path(previous, start, target):
    
    path = []
    current = target
    while current is not None:
        path.append(current)
        if current == start:
            return list(reversed(path))
        current = previous[current]
    return []



def main():
    # Граф із конспекту теми 6.
    graph = {
        "A": {"B": 5, "C": 10},
        "B": {"A": 5, "D": 3},
        "C": {"A": 10, "D": 2},
        "D": {"B": 3, "C": 2, "E": 4},
        "E": {"D": 4},
    }
    start = "A"

    # Стандартна купа
    standard_distances, _ = dijkstra(graph, start, StandardHeap)

    # Власна реалізація
    custom_distances, custom_previous = dijkstra(graph, start, MinHeap)

    assert standard_distances == custom_distances, (
        "Результати стандартної та власної реалізацій купи не збігаються"
    )

    print(f"Найкоротші шляхи від вершини {start} до всіх інших вершин:")
    rows = []
    for vertex, distance in custom_distances.items():
        path = restore_path(custom_previous, start, vertex)
        rows.append([vertex, " -> ".join(path) if path else "Немає шляху",
                     distance if distance != float("inf") else "∞"])
    print(tabulate(rows, headers=["Вершина", "Шлях", "Відстань"], tablefmt="github"))

if __name__ == "__main__":
    main()
