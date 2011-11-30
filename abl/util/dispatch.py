"""
The super-simple event system HOWTO
-----------------------------------

To register a function as an event handler::

    from ableton.dispatch import events

    @events.the_event.register
    def my_event_handler(arg1, arg2):
        do_some_stuff()


the_event is your event. You can use any name you want; if the event
is unknown it will be created automatically.

To fire an event and invoke all its handlers::

    from ableton.dispatch import events

    events.the_event.fire(arg1, arg2)

Note that you must fire the event using the same arguments that all
its handlers expect. If you don't, bad things will happen.

To prevent further handlers from processing an event::

    from ableton.dispatch import events, DONT_PROPOGATE

    @events.the_event.register
    def my_event_handler(arg1, arg2):
        do_some_stuff()
        return DONT_PROPOGATE

To detach your handler from an event::

    events.the_event.detach(my_event_handler)

"""

from collections import defaultdict

DONT_PROPAGATE = 'dont_propagate'


class Event(object):

    def __init__(self):
        self.callables = []


    def register(self, func):
        self.callables.append(func)
        return func


    def detach(self, func):
        if func in self.callables:
            self.callables.remove(func)


    def detach_all(self):
        self.callables = []


    def fire(self, *args, **kwargs):
        for func in self.callables:
            returnvalue = func(*args, **kwargs)
            if returnvalue is DONT_PROPAGATE:
                break



class DispatcherObject(object):

    def __init__(self):
        self.events = defaultdict(Event)


    def __getattr__(self, attr):
        return self.events[attr]


    def eventnames(self):
        return self.events.keys()


    def clear_all(self):
        self.events = defaultdict(Event)
