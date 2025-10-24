class Node:
    """Элемент списка List2L"""
    def __init__(self, key=None, value=None):
        """Инициализация"""
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

    def get_key(self):
        """Получить ключ"""
        return self.key

    def get_value(self):
        """Получить значение"""
        return self.value

    def set_value(self, val):
        """Установить значение"""
        self.value = val


class List2L:
    """Классический двусвязный список"""
    def __init__(self):
        """Инициализация"""
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_front(self, node):
        """Добавляем ноду в начало"""
        node.prev = self.head
        node.next = self.head.next

        self.head.next.prev = node
        self.head.next = node

    def remove(self, node):
        """Удаляем ноду из любой позиции"""
        prev_node = node.prev
        next_node = node.next

        prev_node.next = next_node
        next_node.prev = prev_node

    def pop_last(self):
        """Достаём последний элемент списка"""
        last_node = self.tail.prev
        self.remove(last_node)
        return last_node


class LRUCache:
    """Класс для кеширования объектов"""
    def __init__(self, limit=42):
        """Инициализация"""
        self.limit = limit
        self.list = List2L()
        self.cache = {}

    def get(self, key):
        """Получить значение"""
        if key not in self.cache:
            return None

        node = self.cache[key]
        self.list.remove(node)
        self.list.add_front(node)
        return node.get_value()

    def set(self, key, value):
        """Установить значение"""
        if key in self.cache:
            node = self.cache[key]
            node.set_value(value)
            self.list.remove(node)
            self.list.add_front(node)
        else:
            if len(self.cache) >= self.limit:
                last_node = self.list.pop_last()
                self.cache.pop(last_node.get_key())

            new_node = Node(key, value)
            self.cache[key] = new_node
            self.list.add_front(new_node)
