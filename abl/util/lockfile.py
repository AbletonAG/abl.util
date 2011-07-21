import os
import logging
import errno

import platform
is_windows = False
if platform.system() == 'Windows':
    is_windows = True

if is_windows:
    import msvcrt #@UnresolvedImport
else:
    import fcntl


logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------

class LockFileCreationException(Exception):
    pass


#-------------------------------------------------------------------------------

class LockFileObtainException(Exception):
    pass



#-------------------------------------------------------------------------------

class LockFile(object):

    def __init__(self, name, fail_on_lock=False, cleanup=True):
        self.name = name
        self.cleanup = cleanup
        self.fail_on_lock = fail_on_lock
        self.fd = None
        self.file = None


    def __enter__(self):

        try:
            self.fd = os.open(self.name, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
        except OSError, e:
            if e[0] == errno.ENOENT:
                raise LockFileCreationException()
            else:
                raise
        self.file = os.fdopen(self.fd, "w")
        if is_windows:
            lock_flags = msvcrt.LK_LOCK
        else:
            lock_flags = fcntl.LOCK_EX
        if self.fail_on_lock:
            if is_windows:
                lock_flags = msvcrt.LK_NBLCK
            else:
                lock_flags |= fcntl.LOCK_NB
        try:
            if is_windows:
                msvcrt.locking(self.file.fileno(), lock_flags, 1)
            else:
                fcntl.flock(self.file, lock_flags)
        except IOError, e:
            if e[0] == errno.EAGAIN:
                raise LockFileObtainException()
            raise


        return self.file


    def __exit__(self, unused_exc_type, unused_exc_val, unused_exc_tb):
        if not is_windows:
            fcntl.flock(self.file, fcntl.LOCK_UN)
        self.file.close()
        # we are told to cleanup after ourselves,
        # however it might be that another process
        # has done so - so we don't fail in that
        # case.
        if self.cleanup:
            try:
                os.remove(self.name)
            except OSError, e:
                if e[0] != errno.ENOENT:
                    raise

