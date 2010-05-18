# -*- coding: utf-8 -*-
from unittest import TestCase

from abl.util import (
    unicodify,
    )

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

