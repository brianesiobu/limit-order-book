import random


class SkipListNode:
    __slots__ = ("key", "value", "forward")

    def __init__(self, key, value, level) -> None:
        self.key = key
        self.value = value
        self.forward = [None] * level


class SkipList:
    def __init__(self) -> None:
        self.max_level = 16
        self.p = 0.5
        self.level = 1
        self.header = SkipListNode(-float("inf"), None, self.max_level)

    def random_level(self):
        level = 1
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level

    def insert(self, key, value):
        update = [None] * self.max_level
        current = self.header
        for i in range(self.level - 1, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        current = current.forward[0]

        if current and current.key == key:
            current.value = value
            return current

        level = self.random_level()
        if level > self.level:
            for i in range(self.level, level):
                update[i] = self.header
            self.level = level

        new_node = SkipListNode(key, value, level)

        for i in range(level):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

        return new_node

    def search(self, key):
        current = self.header
        for i in range(self.level - 1, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]

        if current and current.key == key:
            return current

        return None

    def delete(self, key):
        update = [None] * self.max_level
        current = self.header
        for i in range(self.level - 1, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        current = current.forward[0]

        if current and current.key == key:
            for i in range(self.level):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]
            while (
                self.level > 1 and self.header.forward[self.level - 1] is None
            ):
                self.level -= 1
            return True

        return False

    def get_min(self):
        return self.header.forward[0]
