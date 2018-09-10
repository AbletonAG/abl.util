from multiprocessing import Process, Queue
from unittest import TestCase
import tempfile

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
    except Exception as error:
        r.put("something else went wrong: {}".format(error))


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
        self.assertEqual(r.get(), "locked")
        # now start the failer
        failer_p = Process(target=failer, args=(fname, r))
        failer_p.start()

        failer_result = r.get()
        try:
            self.assertEqual(failer_result, "failed properly")
        finally:
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
        self.assertEqual(r.get(), "locked")
        # now start the waiter
        waiter_p = Process(target=waiter, args=(fname, q, r))
        waiter_p.start()

        # now make the locker release the lock
        q.put("unlock")

        # this means the waiter should have it
        waiter_result = r.get()
        self.assertEqual(waiter_result, "got lock")

        # and the failer should still fail, that poor fella
        failer_p = Process(target=failer, args=(fname, r))
        failer_p.start()

        failer_result = r.get()
        try:
            self.assertEqual(failer_result, "failed properly")
        finally:
            # now let the waiter terminate
            q.put("whatever")
