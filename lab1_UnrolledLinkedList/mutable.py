class Node:
    def __init__(self, capacity=16):
        self.elements = [None] * capacity
        self.size = 0
        self.next = None
        self.cap = capacity


class UnrolledLinkedList(object):

    def __init__(self, head=None):
        self.total_size = 0  # The total number of elements in a linked list
        self.head, self.tail = head, Node(-1)  # Sentinel node
        node = Node()
        node.next = self.tail

    def __str__(self):
        return " : ".join(map(str, self.to_list()))

    def size(self):
        return self.total_size

    def to_list(self):
        res = []
        cur = self.head
        while cur is not None:
            for i in range(0, cur.size):
                res.append(cur.elements[i])
            cur = cur.next
        return res

    def from_list(self, lst):
        if len(lst) == 0:
            self.head = Node()
            return
        for a in reversed(lst):
            self.insert(0, a)

    def find(self, is_even):
        cur = self.head
        count = 0
        while cur is not None:
            for i in range(0, cur.size):
                if is_even == cur.elements[i]:
                    count += 1
                    index = count - 1
                    return index
            return -1

    def insert(self, idx, obj):
        if idx < 0 or idx > self.total_size:
            return
        # Find the insertion node and position
        cur = self.head
        while idx >= cur.size:
            if idx == cur.size:
                break
            idx -= cur.size
            cur = cur.next
        # Insert node is full, create a new node
        if cur.size == cur.cap:
            node = Node()
            sec = cur.next
            cur.next = node
            node.next = sec
            # Move the general element of the inserted node to the new node
            move_idx = cur.size // 2
            for i in range(move_idx, cur.size):
                node.elements[i - move_idx] = cur.elements[i]
                cur.elements[i] = None
                cur.size -= 1
                node.size += 1
            # Update insertion position
            if idx >= move_idx:
                idx -= move_idx
                cur = node
        # Insert element
        for i in range(cur.size - 1, idx - 1, -1):
            cur.elements[i + 1] = cur.elements[i]
        cur.elements[idx] = obj

        cur.size += 1
        self.total_size += 1

    def add_to_head(self, value):
        self.insert(0, value)
        self.total_size += 1

    def add_to_tail(self, value):
        self.insert(self.total_size, value)
        self.total_size += 1

    def remove(self, idx):
        if idx < 0 or idx >= self.total_size:
            return

        # Find the node and position of the deleted element
        cur = self.head.next
        while idx >= cur.size - 1:
            if idx == cur.size - 1:
                break
            idx -= cur.size
            cur = cur.next
        # Delete element
        for i in range(idx, cur.size - 1, 1):
            cur.elements[i] = cur.elements[i + 1]
        cur.elements[cur.size - 1] = None
        cur.size -= 1
        if cur.next.cap != -1 and cur.cap >= cur.size + cur.next.size:
            # Merge and delete the next node of the element node to the current node
            next = cur.next
            for i in range(0, next.size):
                cur.elements[cur.size + i] = next.elements[i]
            cur.size += next.size
            cur.next = next.next
        self.total_size -= 1

    def get(self, idx):
        if idx < 0 or idx >= self.total_size:
            return None
        cur = self.head.next
        while idx >= cur.size:
            idx -= cur.size
            cur = cur.next
        return cur.elements[idx]

    def map(self, a):
        cur = self.head
        while cur is not None:
            for i in range(0, cur.size):
                cur.elements[i] = a(cur.elements[i])
            cur = cur.next

    def reduce(self, a, initial_state):
        state = initial_state
        cur = self.head
        while cur is not None:
            for i in range(0, cur.size):
                state = a(state, cur.elements[i])
            cur = cur.next
        return state

    def empty(self):
        return None

    def mconcat(self, a, b):
        ele = self.head
        if a is not None:
            while ele.next is not None:
                ele = ele.next
            ele.next = a.head
        if b is not None:
            while ele.next is not None:
                ele = ele.next
            ele.next = b.head

    def __iter__(self):
        return UnrolledLinkedList(self.head)

    def __next__(self):
        cur = self.head
        if cur is None:
            raise StopIteration
        for i in range(0, cur.size):
            ele = cur.elements[i]
            return ele
        self.head = cur.next
