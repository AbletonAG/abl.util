from functools import partial
import operator

def compare(op, expected_val, err_str):
    def check(obj):
        if not op(obj, expected_val):
            return [err_str]
        else:
            return []
    return check


equals = partial(compare, operator.eq)

not_equals = partial(compare, operator.ne)

is_ = partial(compare, operator.is_)

is_not = partial(compare, operator.is_not)


def attribute(attr, check_func):
    def check(obj):
        original_obj = obj
        attributes = attr.split('.')
        try:
            for name in attributes:
                obj = getattr(obj, name)
            return check_func(obj)
        except AttributeError:
            return ["Attribute {} from {} for obj {} raised AttributeError".format(name, attr, original_obj)]
    return check


def key(key, check_func):
    def check(obj):
        try:
            return check_func(obj[key])
        except KeyError:
            return ["{} has no key {}".format(obj, key)]

    return check


def compose(*checks):
    def check(obj):
        errors = []
        for check in checks:
            errors += check(obj)
        return errors
    return check
