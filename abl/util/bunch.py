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
