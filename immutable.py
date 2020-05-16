class Node:
    def __init__(self, lst, next, capacity=16):
        self.head = None
        self.elements = [None] * capacity
        self.size = 0
        for i in range(0, len(lst)):
            self.elements[i] = lst[i]
            self.size += 1
        self.cap = capacity
        self.next = next

    def __str__(self):
        cur = self.head.next
        for i in range(0, cur.size - 1, 1):
            if type(self.next) is Node:
                return "{} : {}".format(self.elements, self.next)
            return str(self.elements)

    def _eq_(self, other):
        if other is None:
            return False
        cur = self.head.next
        for i in range(0, cur.size - 1, 1):
            if self.elements[i] != other.elements[i]:
                return False
            return self.next == other.next


def size(n):
    if n is None:
        return 0
    else:
        return n.size + size(n.next)


def cons(lst, tail=None):
    if len(lst) > 16:
        return cons(lst[16:], cons(lst[:16], tail))
    return Node(lst, tail)


def remove(n, element):
    assert n is not None, "element should be in list"
    while n is not None:
        for i in range(0, n.size - 1, 1):
            if n.elements[i] == element:
                for t in range(i, n.size - 1, 1):
                    n.elements[t] = n.elements[t + 1]
                n.size -= 1

        return n


def head(n):
    assert type(n) is Node
    return n.elements[0]


def tail(n):
    assert type(n) is Node
    return n.next


def reverse(n, acc=None):
    if n is None:
        return acc
    return reverse(tail(n), Node(head(n), acc))

def mempty():
    return None


def mconcat(a, b):
    if a is None:
        return b
    cur = a
    while cur.next is not None:
        cur = cur.next
    cur.next = b
    return a


def to_list(n):
    if n is None:
        res = []
        return res
    else:
        head = n
        ptr = n
        count = 1

        while ptr.next is not None:
            count += 1
            ptr = ptr.next
        res = []
        while ptr != head:
            if ptr.size == 0:
                ptr = head
                for z in range(0, count - 2):
                    ptr = ptr.next
                count -= 1
            for i in range(0, ptr.size, 1):
                res.append(ptr.elements[i])
                if i == ptr.size - 1:
                    ptr = head
                    for z in range(0, count - 2):
                        ptr = ptr.next
                    count -= 1
        if ptr == head:
            for i in range(0, ptr.size, 1):
                res.append(ptr.elements[i])
        return res





def from_list(lst):
    if len(lst) == 0:
        return cons(lst)
    xd = None
    j = 0
    for i in range(0, len(lst), 8):
        tmp = []
        if len(lst) / 8 >= 1:
            if j < int(len(lst) / 8):
                for t in range(i, i + 8):
                    tmp.append(lst[t])
                xd = cons(tmp, xd)
                j += 1

            else:
                for t in range(i, i + len(lst) % 8):
                    tmp.append(lst[t])
                xd = cons(tmp, xd)
                j += 1

        else:
            for t in range(j, j + len(lst) % 8):
                tmp.append(lst[t])
            xd = cons(tmp, xd)
    return xd



def map(n, f):
    cur = n
    while cur is not None:
        for i in range(0, cur.size,1):
            cur.elements[i] = f(cur.elements[i])
        cur = cur.next
    return n


def reduce(lst, f, initial_state):
    state = initial_state
    cur = lst
    while cur is not None:
        for i in range(0, cur.size):
            state = f(state, cur.elements[i])
        cur = cur.next
    return state


def iterator(lst):
    cur = lst
    tmp = []

    def foo():
        nonlocal cur
        if cur is None: raise StopIteration
        for i in range(0, cur.size):
            if cur.elements[i] == None:
                break
            tmp.append(cur.elements[i])
        cur = cur.next
        return tmp

    return foo()
