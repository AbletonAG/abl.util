
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
