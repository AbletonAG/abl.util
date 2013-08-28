from unittest import TestCase

from abl.util.checks import (equals,
                    attribute,
                    key,
                    compose,
                    )

class Obj(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class CheckTests(TestCase):

    def test_equals(self):

        f = equals(3, "is not 3")
        result = f(3)
        self.assertEqual([], result)

    def test_equals_fail(self):
        f = equals(3, "is not 3")
        result = f(2)
        self.assertEqual(['is not 3'], result)

    def test_attribute(self):
        f = attribute('a', equals(3, "is not 3"))
        obj = Obj(a=3)
        result = f(obj)
        self.assertEqual([], result)

    def test_nested_attribute(self):
        f = attribute('a.b', equals(3, "is not 3"))
        obj = Obj(a=Obj(b=3))
        result = f(obj)
        self.assertEqual([], result)

    def test_nested_attribute_failing(self):
        f = attribute('a.b', equals(3, "is not 3"))
        obj = Obj(a=3)
        result = f(obj)
        self.assertTrue('AttributeError' in result[0])

    def test_key(self):
        f = key('a', equals(3, "is not 3"))
        result = f({'a':3})
        self.assertEqual([], result)

    def test_key_not_there(self):
        f = key('b', equals(3, "is not 3"))
        result = f({'a':3})
        self.assertTrue('has no key' in result[0])

    def test_compose(self):
        attr_func_1 = attribute('a', equals(3, "is not 3"))
        attr_func_2 = attribute('b', equals(2, "is not 2"))
        f = compose(attr_func_1, attr_func_2)
        result = f(Obj(a=3, b=2))
        self.assertEqual([], result)

    def test_compose_one_failing(self):
        attr_func_1 = attribute('a', equals(3, "is not 3"))
        attr_func_2 = attribute('b', equals(2, "is not 2"))
        f = compose(attr_func_1, attr_func_2)
        result = f(Obj(a=3, b=3))
        self.assertEqual(['is not 2'], result)

    def test_compose_all_failing(self):
        attr_func_1 = attribute('a', equals(3, "is not 3"))
        attr_func_2 = attribute('b', equals(2, "is not 2"))
        f = compose(attr_func_1, attr_func_2)
        result = f(Obj(a=4, b=3))
        self.assertEqual(set(['is not 2', 'is not 3']), set(result))

