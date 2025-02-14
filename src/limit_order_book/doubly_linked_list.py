class DoublyLinkedListNode:
    __slots__ = ("data", "prev", "next")

    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = DoublyLinkedListNode(None)
        self.tail = DoublyLinkedListNode(None)

        self.head.next = self.tail
        self.tail.prev = self.head

    def append(self, data):
        new_node = DoublyLinkedListNode(data)

        last = self.tail.prev
        last.next = new_node

        new_node.prev = last
        new_node.next = self.tail

        self.tail.prev = new_node

        return new_node

    def pop_left(self):
        if self.is_empty():
            return None

        first_node = self.head.next
        self.remove(first_node)

        return first_node

    def remove(self, node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

        node.prev = None
        node.next = None

    def is_empty(self):
        return self.head.next == self.tail

    def __iter__(self):
        current = self.head.next
        while current != self.tail:
            yield current.data
            current = current.next
