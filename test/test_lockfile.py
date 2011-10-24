from __future__ import with_statement

try:
    from multiprocessing import Process, Queue
except ImportError:
    print "This test needs the module multiprocessing."
    print "Please either use python >= 2.6 or install it."
else:
    from unittest import TestCase
    import tempfile
    import time

    from abl.util import LockFile, LockFileObtainException


    def locker(q, r):
        lock_file_name = q.get()
        with LockFile(lock_file_name):
            r.put("locked")
            while True:
                command = q.get()
                if command == "unlock":
                    break



    def failer(fname, r):
        try:
            with LockFile(fname, fail_on_lock=True):
                pass
        except LockFileObtainException:
            r.put("failed properly")
        except:
            r.put("something else went wrong")


    def waiter(fname, q, r):
        with LockFile(fname, fail_on_lock=True):
            r.put("got lock")
            # just wait until something happens
            q.get()


    class LockFileTests(TestCase):


        def test_lock_with_fail(self):
            q = Queue()
            r = Queue()
            locker_p = Process(target=locker, args=(q,r))
            locker_p.start()
            fname = tempfile.mktemp()
            q.put(fname)
            # wait until the locker really has the lock
            assert r.get() == "locked"
            # now start the failer
            failer_p = Process(target=failer, args=(fname, r))
            failer_p.start()

            failer_result = r.get()
            assert failer_result == "failed properly", failer_result
            # make the locker release it's lock
            q.put("unlock")


        def test_lock_with_wait(self):
            q = Queue()
            r = Queue()
            locker_p = Process(target=locker, args=(q,r))
            locker_p.start()
            fname = tempfile.mktemp()
            q.put(fname)
            # wait until the locker really has the lock
            assert r.get() == "locked"
            # now start the waiter
            waiter_p = Process(target=waiter, args=(fname, q, r))
            waiter_p.start()

            # now make the locker release the lock
            q.put("unlock")

            # this means the waiter should have it
            waiter_result = r.get()
            assert waiter_result == "got lock", waiter_result

            # and the failer should still fail, that poor fella
            failer_p = Process(target=failer, args=(fname, r))
            failer_p.start()

            failer_result = r.get()
            assert failer_result == "failed properly", failer_result

            # now let the waiter terminate
            q.put("whatever")


