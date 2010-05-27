# -*- coding: utf-8 -*-
from unittest import TestCase

from abl.util import (
    classproperty,
    partition,
    unicodify,
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

