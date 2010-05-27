
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


#--------------------------------------------------------------------------------

class Bunch(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


    def __repr__(self):
        res = ["<Bunch"]
        for name in sorted(self.__dict__.keys()):
            if not name.startswith("__"):
                res.append("%s = %r" % (name, getattr(self, name)))
        return "\n".join(res)


    def pop(self, key):
        return self.__dict__.pop(key)


    def append(self, **kwargs):
        self.__dict__.update(kwargs)


    def get_values(self):
        return self.__dict__.copy()




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


