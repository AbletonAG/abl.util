# -*- coding: utf-8 -*-

from __future__ import with_statement

from unittest import TestCase

from abl.util import (
    SafeModifier,
    classproperty,
    fixpoint,
    partition,
    unicodify,
    with_,
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


class TestUnicodify(TestCase):

    def test_unicode_unity(self):
        utest = u"Hülle"
        assert unicodify(utest) is utest

    def test_utf8_to_unicode(self):
        teststring = 'H\xc3\xbclle'
        assert unicodify(teststring) == u"Hülle"

    def test_ignore_errors(self):
        teststring = 'H\xc3\xbclle'
        assert unicodify(teststring, codecs=()) == u"Hlle"


class FixpointTests(TestCase):

    def test_fixpoint(self):

        def f(x):
            if x == 10:
                return x
            return x + 1

        assert fixpoint(f, 1) == 10


class SafeModifierTests(TestCase):

    class Foo(object):
        pass


    def test_override_existing(self):
        foo = self.Foo()
        foo.bar = 42

        with SafeModifier(foo, 'bar', 17):
            self.assertEqual(foo.bar, 17)

        self.assertEqual(foo.bar, 42)


    def test_set_unset(self):
        foo = self.Foo()

        with SafeModifier(foo, 'bar', 17):
            self.assertEqual(foo.bar, 17)

        self.assertFalse(hasattr(foo, 'bar'))


class WithDecoratorTests(TestCase):

    class Foo(object):
        pass


    def test_decorate_function(self):

        foo = self.Foo()
        foo.bar = 42

        @with_(SafeModifier(foo, 'bar', 17))
        def decorated(x):
            self.assertEqual(foo.bar, 17)
            self.assertEqual(x, 1)

        decorated(1)
        self.assertEqual(foo.bar, 42)


    def test_decorate_method(self):

        foo = self.Foo()
        foo.bar = 42

        class MethodDecorationTest(object):
            @with_(SafeModifier(foo, 'bar', 13))
            def decorated(self, x):
                assert x == 1
                assert foo.bar == 13

        MethodDecorationTest().decorated(1)
        self.assertEqual(foo.bar, 42)


    def test_decorate_many(self):

        foo = self.Foo()
        foo.bar = 42
        foo.foo = 20

        class MethodDecorationTest(object):
            @with_(SafeModifier(foo, 'bar', 13), SafeModifier(foo, 'foo', 2))
            def decorated(self, x):
                assert x == 1
                assert foo.bar == 13
                assert foo.foo == 2

        MethodDecorationTest().decorated(1)
        self.assertEqual(foo.bar, 42)
        self.assertEqual(foo.foo, 20)

