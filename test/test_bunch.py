from unittest import TestCase

import pickle

from abl.util import (
    Bunch,
    )

class Derived(Bunch):
    pass

class TestBunch(TestCase):

    def test_as_dict(self):
        bunch = Bunch(a='a', b='b')
        assert bunch == dict(a='a', b='b')

    def test_as_obj(self):
        bunch = Bunch(a='a', b='b')
        assert bunch.a == 'a'
        assert bunch.b == 'b'

    def test_failing_attribute(self):
        bunch = Bunch(a='a', b='b')
        self.assertRaises(AttributeError, getattr, bunch, 'c')

    def test_failing_key(self):
        bunch = Bunch(a='a', b='b')
        self.assertRaises(KeyError, lambda:bunch['c'])

    def test_pickling(self):
        bunch = Bunch(a='a', b='b')
        dump = pickle.dumps(bunch)
        from_pickle = pickle.loads(dump)
        assert bunch == from_pickle
        assert from_pickle.__class__ is Bunch

    def test_pickling_derived_class(self):

        derived = Derived(a='a', b='b')
        dump = pickle.dumps(derived)
        from_pickle = pickle.loads(dump)
        assert derived == from_pickle
        assert from_pickle.__class__ is Derived
