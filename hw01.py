# Завдання 1. Робота з однозв'язним списком.
from __future__ import annotations # added for compatibility with Python 3.10–3.13
from tabulate import tabulate

# елемент однозв'язного списку
class Node:
    def __init__(self, data: int):
        self.data = data
        self.next: Node | None = None

# Реалізація однозв'язного списку, що підтримує тільки додавання, реверсування та сортування елементів.
class LinkedList:

    def __init__(self, values: list[int] | None = None):
        self.head: Node | None = None
        if values is not None:
            for value in values:
                self.append(value)

    # Додає новий елемент у кінець списку.
    def append(self, data: int):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    # Розвертає список, змінюючи посилання між вузлами.
    def reverse(self):
        previous = None
        current = self.head

        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        self.head = previous

    # Сортує однозв'язний список методом вставок.
    def sort_insertion(self):
        if self.head is None:
            return

        sorted_head = self.head
        current = self.head.next
        sorted_head.next = None

        while current is not None:
            next_node = current.next

            if current.data < sorted_head.data:
                current.next = sorted_head
                sorted_head = current
            else:
                node = sorted_head

                while node.next is not None and node.next.data <= current.data:
                    node = node.next

                current.next = node.next
                node.next = current

            current = next_node

        self.head = sorted_head

    

    # Об'єднує два відсортовані ланцюжки вузлів без створення нових вузлів.
    @staticmethod
    def merge_sorted_nodes(first: Node | None, second: Node | None) -> Node | None:
    
        dummy = Node(0)
        tail = dummy

        while first is not None and second is not None:
            if first.data <= second.data:
                tail.next = first
                first = first.next
            else:
                tail.next = second
                second = second.next
            tail = tail.next

        tail.next = first if first is not None else second
        return dummy.next


    # Рекурсивно сортує однозв'язний список методом злиття.
    @staticmethod
    def merge_sort_list(head: Node | None) -> Node | None:
    
        if head is None or head.next is None:
            return head

        slow = head
        fast = head.next
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

        middle = slow.next
        slow.next = None

        left = LinkedList.merge_sort_list(head)
        right = LinkedList.merge_sort_list(middle)
        return LinkedList.merge_sorted_nodes(left, right)

    
    # Сортує однозв'язний список злиттям
    def sort_merge(self):
        self.head = LinkedList.merge_sort_list(self.head)


    # Об'єднує два відсортовані списки в один відсортований список.
    # Вузли початкових списків переходять до нового списку.
    @staticmethod
    def merge_sorted_lists(first: LinkedList, second: LinkedList) -> LinkedList:

        result = LinkedList()
        result.head = LinkedList.merge_sorted_nodes(first.head, second.head)
        first.head = None
        second.head = None
        return result


    def __str__(self):
        values = []
        current = self.head
        while current is not None:
            values.append(str(current.data))
            current = current.next
        return " -> ".join(values) if values else "(порожній список)"



def main():
    values = [7, 2, 9, 1, 5, 3]
    l = LinkedList(values)
    
    print("Реверсування та сортування:")

    results = [["Початковий список", str(l)]]
    l.reverse()
    results.append(["Після реверсування", str(l)])
    l.sort_insertion()
    results.append(["Після сортування методом вставки", str(l)])
    l.reverse()
    results.append(["Після реверсування", str(l)])
    l.sort_merge()
    results.append(["Після сортування методом злиття", str(l)])

    print(tabulate( 
        results, 
        headers=["Операція", "Список"], 
        tablefmt="github"
    ))

    print()
    print("Об'єднання відсортованих списків:")

    first_list = LinkedList([1, 4, 7])
    results = [["Перший список", str(first_list)]]
    
    second_list  = LinkedList([2, 3, 8])
    results.append(["Другий список", str(second_list)])

    merged_list = LinkedList.merge_sorted_lists(first_list, second_list)
    results.append(["Об'єднаний список", str(merged_list)])

    print(tabulate(
        results,
        headers=["Операція", "Список"],
        tablefmt="github",
    ))


if __name__ == "__main__":
    main()
