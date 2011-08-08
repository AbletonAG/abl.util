from __future__ import with_statement

from contextlib import nested

import logging

from functools import wraps


def classproperty(f):
    """
    Create a property on a class, not an instance.

    Works only for getting.
    """
    class Descriptor(object):
        def __get__(self, _obj, objtype):
            return f(objtype)

    return Descriptor()


def partition(predicate, sequence):
    """
    Takes a predicate & a sequence of items, and
    applies the predicate to each of them.

    Returns a tuple with the first item being the
    list of matched items, and the second being
    the list of not matched items.
    """
    match, nomatch = [], []
    for item in sequence:
        if predicate(item):
            match.append(item)
        else:
            nomatch.append(item)
    return match, nomatch


class Bunch(dict):
    def __setattr__(self, key, item):
        self[key] = item


    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError


    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError


    def __getstate__(self):
        return dict(**self)


    def __setstate__(self, data):
        self.update(data)


    def copy(self):
        return self.__class__(**super(Bunch, self).copy())


    def __repr__(self):
        res = ["<%s" % self.__class__.__name__]
        for name in self:
            if not name.startswith("__"):
                res.append("    '%s' = %r" % (name, self[name]))
        res.append("    >")
        return "\n".join(res)


#==============================================================================

class TeeBuffer(object):
    """
    Stream that buffers output and optionally also passes it to a given stream.
    """
    def __init__(self, oldstream=None):
        self.__buffer = []
        self._oldstream = oldstream


    def write(self, data):
        self.__buffer.append(data)
        if self._oldstream is not None:
            self._oldstream.write(data)


    def flush(self):
        if self._oldstream is not None:
            self._oldstream.flush()


    def getvalue(self):
        return "".join(self.__buffer)


def unicodify(text, codecs=('utf-8', 'latin-1', 'cp1252'), errors='ignore'):
    """
    cast any kind of string into a unicode string, even if the encoding is not known.
    If none of the codecs work, use 'unicode' with the errors attribute.
    """
    assert isinstance(text, basestring)
    if isinstance(text, unicode):
        return text
    for codec in codecs:
        try:
            return text.decode(codec)
        except UnicodeDecodeError:
            pass
    return unicode(text, errors=errors)


class NullHandler(logging.Handler):
    """
    The NullHandler can be used to set up logging so
    that no "no logger installed for ..." messages
    appear.

    Use it like this::

      logging.getLogger().addHandler(NullHandler())

    """

    def emit(self, *args, **kwargs):
        pass




def fixpoint(f, arg):
    """
    Simple function that takes a function and an argument and
    invokes f(f(...)) until f^t == f^(t - 1)
    """
    new_arg = arg
    while True:
        new_arg = f(arg)
        if new_arg == arg:
            break
        arg = new_arg
    return new_arg


class SafeModifier(object):
    """
    A simple context to set an attribute on
    a given object to a value, and before
    leaving the the context re-set it.
    """


    def __init__(self, o, name, value):
        """

        :param o: the object to modify
        :param name: the name of the attribute to set
        :param value: the value to replace.
        """

        self.o = o
        self.name = name
        self.value = value


    def __enter__(self):
        try:
            self.old_value = getattr(self.o, self.name)
        except AttributeError:
            pass
        setattr(self.o, self.name, self.value)


    def __exit__(self, _et, _e, _tb):
        try:
            setattr(self.o, self.name, self.old_value)
        except AttributeError:
            delattr(self.o, self.name)
        return False


def with_(*managers):
    """
    Decorator that applies a context manager. ie::

        @with_(cm)
        def foo():
            ...

    Is equivalent to::

        def foo():
            with cm:
                ...

    """
    def _with_decorator(f):
        def _with_(*args, **kwargs):
            with nested(*managers):
                return f(*args, **kwargs)
        return wraps(f)(_with_)
    return _with_decorator
