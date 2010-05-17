# -*- coding: utf-8 -*-
from __future__ import with_statement

from unittest import TestCase

from abl.util import (
    unicodify,
    Bunch,
    Configuration
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

class TestBunch(TestCase):
    # Todo std: write Tests
    pass

class TestConfiguration(TestCase):
    # Todo std: write Tests
    pass
