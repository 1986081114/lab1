import unittest
from hypothesis import given

import hypothesis.strategies as st

from mutable import UnrolledLinkedList, Node


class TestUnrolledLinkedList(unittest.TestCase):
    def test_size(self):
        lst = UnrolledLinkedList(Node())
        self.assertEqual(lst.size(), 0)
        lst.insert(0, 1)
        self.assertEqual(lst.size(), 1)
        lst.insert(lst.total_size, 2)
        self.assertEqual(lst.size(), 2)

    def test_to_list(self):
        self.assertEqual(UnrolledLinkedList(Node()).to_list(), [])
        lst = UnrolledLinkedList(Node())
        lst.insert(0, 'a')
        self.assertEqual(lst.to_list(), ['a'])
        lst.insert(1, 2)
        self.assertEqual(lst.to_list(), ['a', 2])

    def test_from_list(self):
        test_data = [
            [],
            ['a'],
            ['a', 'b']
        ]
        for i in test_data:
            lst = UnrolledLinkedList(Node())
            lst.from_list(i)
            self.assertEqual(lst.to_list(), i)

    def test_add_to_head(self):
        lst = UnrolledLinkedList(Node())
        self.assertEqual(lst.to_list(), [])
        lst.add_to_head(1)
        self.assertEqual(lst.to_list(), [1])
        lst.add_to_head('a')
        self.assertEqual(lst.to_list(), ['a', 1])

    def test_add_to_tail(self):
        lst = UnrolledLinkedList(Node())
        self.assertEqual(lst.to_list(), [])
        lst.add_to_tail(1)
        self.assertEqual(lst.to_list(), [1])

    def test_map(self):
        lst = UnrolledLinkedList(Node())
        lst.map(str)
        self.assertEqual(lst.to_list(), [])

        lst1 = UnrolledLinkedList(Node())
        lst1.from_list([1, 2, 3])
        lst1.map(str)
        self.assertEqual(lst1.to_list(), ["1", "2", "3"])

    def test_reduce(self):
        lst = UnrolledLinkedList(Node())
        self.assertEqual(lst.reduce(lambda st, e: st + e, 0), 0)
        lst = UnrolledLinkedList(Node())
        lst.from_list([1, 2, 3])
        self.assertEqual(lst.reduce(lambda a, b: a + b, 0), 6)
        test_data = [
            [],
            ['a'],
            ['a', 'b']
        ]
        for e in test_data:
            lst = UnrolledLinkedList(Node())
            lst.from_list(e)
            self.assertEqual(lst.reduce(lambda st, _: st + 1, 0), lst.size())

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a):
        lst = UnrolledLinkedList(Node())
        lst.from_list(a)
        b = lst.to_list()
        self.assertEqual(a, b)

    @given(st.lists(st.integers()))
    def test_python_len_and_list_size_equality(self, a):
        lst = UnrolledLinkedList(Node())
        lst.from_list(a)
        self.assertEqual(lst.size(), len(a))

    def test_iter(self):
        x = [1, 2, 3]
        lst = UnrolledLinkedList(Node())
        lst.from_list(x)
        tmp = []
        i = 0
        for e in lst.head.elements:
            i += 1
            if i > len(x):
                break
            tmp.append(e)
        self.assertEqual(x, tmp)
        self.assertEqual(lst.to_list(), tmp)

        i = iter(UnrolledLinkedList())
        self.assertRaises(StopIteration, lambda: next(i))

    def test_find(self):
        x = [1, 2, 3, ]
        lst = UnrolledLinkedList(Node())
        lst.insert(0, 1)
        lst.insert(1, 2)
        index = lst.find(1)
        self.assertEqual(0, index)

    @given(st.lists(st.integers()))
    def test_monoid_identity(self, a):
        lst = UnrolledLinkedList(Node())
        lst.from_list(a)
        res = UnrolledLinkedList(Node())
        lst_mconcat = UnrolledLinkedList(Node())
        lst_mconcat.mconcat(lst, res.empty())
        self.assertEqual(lst_mconcat.to_list(), a)

        lst_mconcat = UnrolledLinkedList(Node())
        lst_mconcat.mconcat(res.empty(), lst)
        self.assertEqual(lst_mconcat.to_list(), a)

    @given(a=st.lists(st.integers()), b=st.lists(st.integers()), c=st.lists(st.integers()))
    def test_monoid_associativity(self, a, b, c):
        ULlsta = UnrolledLinkedList(Node())
        ULlstb = UnrolledLinkedList(Node())
        ULlstc = UnrolledLinkedList(Node())
        ULlsta.from_list(a)
        ULlstb.from_list(b)
        ULlstc.from_list(c)

        ULlst_test1 = UnrolledLinkedList(Node())
        ULlst_testb = UnrolledLinkedList(Node())
        ULlst_testb.mconcat(ULlsta, ULlstb)
        ULlst_test1.mconcat(ULlst_testb, ULlstc)

        ULlsta = UnrolledLinkedList(Node())
        ULlstb = UnrolledLinkedList(Node())
        ULlstc = UnrolledLinkedList(Node())
        ULlsta.from_list(a)
        ULlstb.from_list(b)
        ULlstc.from_list(c)

        ULlst_test2 = UnrolledLinkedList(Node())
        ULlst_testb = UnrolledLinkedList(Node())
        ULlst_testb.mconcat(ULlstb, ULlstc)
        ULlst_test2.mconcat(ULlsta, ULlst_testb)

        ULlst1 = ULlst_test1.to_list()
        ULlst2 = ULlst_test2.to_list()
        self.assertEqual(ULlst1, ULlst2)


if __name__ == '__main__':
    unittest.main()
