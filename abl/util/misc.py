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


