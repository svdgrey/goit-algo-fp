
# Власна реалізація мінімальної бінарної купи на основі списку.
class MinHeap:

    def __init__(self, values: list | None = None):
        self.items = []

        if values is not None:
            for value in values:
                self.push(value)

    def __bool__(self):
        return bool(self.items)

    def push(self, value):
        self.items.append(value)
        index = len(self.items) - 1

        # Піднімаємо елемент, доки не відновимо властивість купи.
        while index > 0:
            parent = (index - 1) // 2
            if self.items[parent] <= self.items[index]:
                break
            self.items[parent], self.items[index] = self.items[index], self.items[parent]
            index = parent

    def pop(self):
        if not self.items:
            raise IndexError("Купа порожня")

        minimum = self.items[0]
        last = self.items.pop()
        if not self.items:
            return minimum

        self.items[0] = last
        index = 0
        size = len(self.items)

        # Опускаємо корінь, міняючи його з меншим дочірнім вузлом.
        while True:
            left = 2 * index + 1
            right = left + 1
            smallest = index

            if left < size and self.items[left] < self.items[smallest]:
                smallest = left
            if right < size and self.items[right] < self.items[smallest]:
                smallest = right
            if smallest == index:
                break

            self.items[index], self.items[smallest] = self.items[smallest], self.items[index]
            index = smallest

        return minimum


    def __str__(self):
        if not self.items:
            return "(порожня купа)"

        def build(index, prefix=""):
            result = ""
            left = 2 * index + 1
            right = 2 * index + 2

            for child, label in ((left, "[L]"), (right, "[R]")):
                if child >= len(self.items):
                    continue

                is_last = child == right or right >= len(self.items)
                branch = "+-- " if is_last else "|-- "

                result += prefix + branch + label + " " + str(self.items[child]) + "\n"
                result += build(child, prefix + ("    " if is_last else "|   "))

            return result

        return str(self.items[0]) + "\n" + build(0).rstrip("\n")