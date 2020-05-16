import unittest

from hypothesis import given, settings

import hypothesis.strategies as st

from immutable import *


class TestImmutableList(unittest.TestCase):

    def test_size(self):

        self.assertEqual(size(cons('a', None)), 1)
        lst = [1, 2, 3, 4]
        self.assertEqual(size(cons(lst, None)), 4)

    def test_cons(self):

        self.assertEqual(to_list(cons(['a'], None)), to_list(Node('a', None)))
        self.assertEqual(to_list(cons('a', cons('b', None))), to_list(Node('a', Node('b', None))))

    def test_remove(self):

        self.assertEqual(to_list(remove(cons('b', None), 'b')), to_list(cons(['b'], None)))
        lst = ['a', 'b', 'c', 'd']
        self.assertEqual(to_list(remove(cons(lst, None), 'a')), to_list(cons(['b', 'c', 'd'], None)))

    def test_head(self):
        self.assertRaises(AssertionError, lambda: tail(None))
        self.assertEqual(head(cons('a', None)), 'a')

    def test_tail(self):
        self.assertRaises(AssertionError, lambda: tail(None))
        self.assertEqual(tail(cons('a', None)), None)
        self.assertEqual(to_list(tail(cons('a', cons('b',None)))), to_list(cons('b', None)))

    def test_to_list(self):

        self.assertEqual(to_list(None), [])
        self.assertEqual(to_list(cons('a', None)), ['a'])
        self.assertEqual(to_list(cons('a', cons('b', None))), ['b', 'a'])

    def test_from_list(self):

        test_data = [

            [],

            ['a'],

            ['a', 'b']

        ]

        for e in test_data:
            b = from_list(e)

            a = to_list(b)

            self.assertEqual(a, e)

    def test_map(self):

        lst = from_list([])

        lst = map(lst, str)

        lst = to_list(lst)

        self.assertEqual(lst, [])

        lst1 = from_list([1, 2, 3])

        lst1 = map(lst1, str)

        lst1 = to_list(lst1)

        self.assertEqual(lst1, ["1", "2", "3"])

    def test_reduce(self):

        # sum of empty list

        lst = Node([], None)

        lst = reduce(lst, lambda st, e: st + e, 0)

        self.assertEqual(lst, 0)

        # sum of list

        lst = from_list([1, 2, 3])

        lst = reduce(lst, lambda st, e: st + e, 0)

        self.assertEqual(lst, 6)

        # size

        test_data = [

            ['a'],

            ['a', 'b'],

            ['a', 'b', 'c']

        ]

        for e in test_data:
            lst1 = from_list(e)

            lst = reduce(lst1, lambda st, _: st + 1, 0)

            self.assertEqual(lst, lst1.size)

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a):

        b = from_list(a)

        c = to_list(b)

        self.assertEqual(c, a)

    @given(st.lists(st.integers()))
    def test_monoid_identity(self, lst):

        a = from_list(lst)

        self.assertEqual(mconcat(mempty(), a), a)

        self.assertEqual(mconcat(a, mempty()), a)

    @given(st.lists(st.integers()), st.lists(st.integers()), st.lists(st.integers()))
    def test_monoid_associativity(self, lst1, lst2, lst3):

        q = from_list(lst1)

        w = from_list(lst2)

        e = from_list(lst3)

        a = mconcat(mconcat(q, w), e)

        q = from_list(lst1)

        w = from_list(lst2)

        e = from_list(lst3)

        b = mconcat(q, mconcat(w, e))

        self.assertEqual(to_list(a), to_list(b))

    def test_iter(self):

        x = [1, 2, 3]

        lst = from_list(x)

        sur = iterator(lst)

        self.assertEqual(x, sur)


if __name__ == '__main__':
    unittest.main()
