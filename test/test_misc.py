from unittest import TestCase

from abl.util import (
    classproperty,
    partition,
    )

class TestMisc(TestCase):


    def test_classproperty(self):

        value = 100
        class Foo(object):

            FOO = value
            
            @classproperty
            def test(cls):
                return cls.FOO

        assert Foo.test == value
        assert Foo().test == value


    def test_partition(self):
        self.assertEqual(partition(lambda i: i < 5, xrange(10)),
                         ([0, 1, 2, 3, 4], [5, 6, 7, 8, 9]))
               
