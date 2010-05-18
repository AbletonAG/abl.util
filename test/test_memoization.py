from unittest import TestCase

from abl.util import memoized


class MemoizationTests(TestCase):


    def test_memoization_works(self):
        global COUNTER
        COUNTER = 0
        def counter():
            global COUNTER
            COUNTER += 1
            return COUNTER

        # first, make sure the function
        # works.
        assert counter() == 1
        # now memoize it, and
        # subsequent calls will return the
        # same value.
        counter = memoized()(counter)
        assert counter() == 2
        assert counter() == 2


    def test_memoization_fails_gracefully_on_non_hashable_arguments(self):
        global COUNTER
        COUNTER = 0
        
        @memoized()
        def test(arg):
            global COUNTER
            COUNTER += 1
            return str(arg)


        assert test(10) == test(10) and COUNTER == 1

        assert test({}) == test({}) and COUNTER == 3


    def test_memoization_doesnt_mask_exceptions(self):
        global COUNTER
        COUNTER = 0
        
        @memoized()
        def test():
            global COUNTER
            COUNTER += 1
            raise TypeError

        self.failUnlessRaises(TypeError, test)
        # we are only called *once*
        assert COUNTER == 1
        

        COUNTER = 0
        
        @memoized()
        def test():
            global COUNTER
            COUNTER += 1
            raise KeyError

        self.failUnlessRaises(KeyError, test)
        # we are only called *once*
        assert COUNTER == 1
        

    def test_clearing_memoization_cache(self):
        global COUNTER
        COUNTER = 0

        @memoized()
        def test():
            global COUNTER
            COUNTER += 1
            return COUNTER

        @memoized()
        def test_two():
            global COUNTER
            COUNTER += 1
            return COUNTER

        assert test() == 1
        assert test_two() == 2
        test.clear_cache()
        # only the test-cache must be cleared.
        assert test() == 3
        assert test_two() == 2

        # now clear the full global scope.
        test.clear_full_scope()
        assert test() == 4
        assert test_two() == 5
        assert test() == 4
        assert test_two() == 5
        
        
        
    def test_memoization_on_objects(self):
        global COUNTER
        COUNTER = 0
        
        class Test(object):


            @memoized()
            def test_method(self):
                global COUNTER
                COUNTER += 1
                return COUNTER

            @classmethod
            @memoized()
            def test_classmethod(cls):
                global COUNTER
                COUNTER += 1
                return COUNTER


        a = Test()
        b = Test()

        assert a.test_method() == 1
        assert a.test_method() == 1
        assert b.test_method() == 2
        assert b.test_method() == 2
        assert a.test_classmethod() == 3
        assert b.test_classmethod() == 3
        

    def test_scope_isolation(self):
        global COUNTER
        COUNTER = 0
        
        @memoized("foo")
        def test_foo():
            global COUNTER
            COUNTER += 1
            return COUNTER

        @memoized("bar")
        def test_bar():
            global COUNTER
            COUNTER += 1
            return COUNTER

        assert test_foo() == 1
        assert test_bar() == 2
        assert test_foo() == 1
        assert test_bar() == 2

        test_foo.clear_full_scope()
        assert test_foo() == 3
        assert test_bar() == 2
