"""
bunch.py
"""

import datetime
import logging
from optparse import OptionValueError
import os
import sys

try:
    import json
except ImportError:
    import simplejson as json

def unicodify(text, codecs=('utf-8', 'latin-1', 'cp1252')):
    "make sure that the result is a unicode string, even if the encoding is not known"
    assert isinstance(text, basestring)
    if isinstance(text, unicode):
        return text
    for codec in codecs:
        try:
            return text.decode(codec)
        except UnicodeDecodeError:
            pass
    return unicode(text, errors='ignore')

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

    def get_prefix(self, prefix, remove_prefix=False):
        other = self.__class__()
        keys = [x for x in self.keys() if x.startswith(prefix)]
        for key in keys:
            new_key = key
            if remove_prefix:
                new_key = key[len(prefix):]
            other[new_key] = self[key]
        return other

class Configuration(Bunch):
    """
    If access is via attributes, the value is interpolated first.
    If the attribute does not exist, return None.
    Example (string interpolation):

    >>> env = Configuration(
    >>> env = Configuration(name='Tim', greeting='Hello %(name)s')
    >>> env.greeting
    'Hello Tim'
    >>> env.name = 'Tom'
    >>> env.greeting
    'Hello Tom'
    >>> env.family_name = 'Miller'
    >>> env.name = 'Jack %(family_name)s'
    >>> env.greeting
    'Hello Jack Miller'
    >>> env.family_name = 'Bush'
    >>> env.greeting
    'Hello Jack Bush'
    >>>
    """

    def __getattr__(self, key):
        try:
            result = self[key]
            next = result % self
            while result != next:
                result = next
                next = result % self
            return next
        except KeyError:
            if not key in self:
                return None
            else:
                return result
        except TypeError:
            return self[key]

    def __getstate__(self):
        "when pickling a Configuration, we don't want 'private' attributes"
        rdict = self.copy()
        underscore_keys = [x for x in rdict if x.startswith('_')]
        for key in underscore_keys:
                del rdict[key]
        return rdict

    def jsonify(self):
        the_copy = self.copy()
        for key in self:
            if (
                key.startswith('_') or 
                isinstance(the_copy[key], datetime.datetime) or
                'passwd' in key
                ):
                del the_copy[key]
        return json.dumps(the_copy, sort_keys=True, indent=4)
