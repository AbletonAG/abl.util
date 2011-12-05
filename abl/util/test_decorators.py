from datetime import date


def disable(f):
    """Mark a test as disabled."""
    f.__test__ = False
    return f


def disable_if(predicate):
    """
    Disables a test if predicate yields True at parse time.

    @param predicate: a callable that gets passed the test as whole or the
        method under test and returns a bool
    @param reason: function that is responsible for the conditional, if nothing
        is passed, disable_if is assumed (used for disable_unless)
    @return: a decorator
    """
    def _decorator(f):
        if predicate():
            f.__test__ = False
        return f
    return _decorator


def disable_before(year, month=None, day=None):
    """
    Disables a test before the given day.

    Give year/month/day as int, and make sure not to pass in something like
    <09>, but pass <9> instead (<09> would be interpreted as being octal).

    @note: Please use this only when having a very good reason to disable
        a test before a certain date.

    @return: a decorator
    """
    if month is None and day is None:
        year, month, day = year.year, year.month, year.day
    def _decorator(f):
        if date.today() < date(year, month, day):
            f.__test__ = False
        return f
    return _decorator


def disable_unless(predicate):
    """
    Disables a test unless predicate yields True at parse time.

    @param predicate: a callable that gets passed the test
                      as whole or the method under test
                      and returns a bool
    @return: a decorator
    """
    def neg(*args):
        return not predicate(*args)
    return disable_if(neg)


def not_a_test(f):
    """Use this to mark methods that have test in their name but are not
    an actual test method."""
    f.__test__ = False
    f.__not_a_test__ = True
    return f

# not_a_test() is not a test
not_a_test = not_a_test(not_a_test)
