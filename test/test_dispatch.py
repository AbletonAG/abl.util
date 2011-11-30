from unittest import TestCase
from abl.util import Event, DispatcherObject, DONT_PROPAGATE


class Test_events(TestCase):

    def setUp(self):
        self.events = DispatcherObject()


    def test_first(self):
        empty_event = self.events.no_registered_event
        self.assert_(isinstance(empty_event, Event))


    def test_register(self):
        log = []
        def call_me(msg):
            log.append(msg)
        self.events.first_event.register(call_me)
        self.events.first_event.fire('my man')
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0], 'my man')


    def test_detach(self):
        def nothing():pass
        self.events.some_event.register(nothing)
        self.assertEqual(len(self.events.some_event.callables), 1)
        self.events.some_event.detach(nothing)
        self.assertEqual(len(self.events.some_event.callables), 0)


    def test_detach_all(self):
        def nothing():pass
        self.events.some_event.register(nothing)
        self.events.some_event.register(nothing)
        self.events.some_event.register(nothing)
        self.assertEqual(len(self.events.some_event.callables), 3)
        self.events.some_event.detach_all()
        self.assertEqual(len(self.events.some_event.callables), 0)


    def test_register_classmethod(self):
        class MyClass(object):
            log = []

            @classmethod
            def run_me(cls, msg):
                cls.log.append(msg)

        self.events.run_me.register(MyClass.run_me)

        myobj = MyClass()
        self.events.run_me.fire('help!!!')
        self.assertEqual(myobj.log, ['help!!!'])


    def test_propagate(self):
        log = []
        def foo(msg):
            log.append(msg)

        def bar(msg):
            log.append(msg)
            return DONT_PROPAGATE

        def foobar(msg):
            log.append(msg)

        self.events.me.register(foo)
        self.events.me.register(bar)
        self.events.me.register(foobar)

        self.events.me.fire('help!!!')
        self.assertEqual(len(log), 2)


    def test_eventnames(self):
        self.events.foo.fire()
        self.events.bar.fire()
        self.assertEqual(len(self.events.eventnames()), 2)
        self.assertEqual(set(self.events.eventnames()), set(('foo', 'bar')))
