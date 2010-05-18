from collections import defaultdict
from functools import partial

#==============================================================================

# A dict with scopes as keys and lists of memoized objects as values.
MEMOIZED = defaultdict(list)

def memoized(scope='global'):
    """
    Decorator that caches a function's return value when it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.

     - param **scope**: You can hand in a scope to clean exactly the caches under
        this scope via calling `clear_full_scope` on the memoized function.
    """

    class Memoized(object):

        def __init__(self, func):
            self._func = func
            self._cache = {}
            self._scope = scope
            MEMOIZED[scope].append(self)


        def __call__(self, *args, **kwargs):
            key = args + tuple(kwargs.items())
            try:
                return self._cache[key]
            except KeyError:
                self._cache[key] = value = self._func(*args, **kwargs)
                return value
            except TypeError:
                # Uncachable -- for instance, passing a list or dict as an
                # argument. Better to not cache than to blow up entirely.
                return self._func(*args, **kwargs)


        def __get__(self, instance, class_):
            if instance is not None:
                return partial(self.__call__, instance)
            return self
                

        def __repr__(self):
            """Return the function's docstring."""
            return self._func.__doc__


        def clear_cache(self):
            """
            The cache that is used with this memoized decorators is cleaned.

            Usage:

                @memorized(SCOPE)
                def foo():
                    do_something()

                foo.clear_cache()
            """
            self._cache = {}


        def clear_full_scope(self):
            """
            All cached values that are used with memoized decorators with the
            same scope are cleaned.

            Usage:

                @memorized(SCOPE)
                def foo():
                    do_something()

                foo.clear_full_scope()
            """
            for memoized_obj in MEMOIZED[self._scope]:
                memoized_obj.clear_cache()


    if callable(scope):
        raise Exception('"memoized"-decorator was not called on initialization.')

    return Memoized

