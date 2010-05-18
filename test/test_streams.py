from __future__ import with_statement
import tempfile

from unittest import TestCase

from abl.util import (
    Stream,
    BufferedStream,
    )



class TestStreams(TestCase):


    def test_simple_stream(self):
        tf = tempfile.mktemp()
        with open(tf, "w") as outf:
            outf.write("*" * 10)

        with open(tf) as inf:
            wf = Stream(inf)
            assert wf.read(5) == "*" * 5
            self.assertEqual(wf.read(), "*" * 5)


    def test_buffered_stream(self):
        testdata = "abcdefghijklmn" * 10000 # must be larger than our bufsize

        tf = tempfile.mktemp()
        with open(tf, "w") as outf:
            outf.write(testdata)

        with open(tf) as inf:
            wf = Stream(inf)
            bs = BufferedStream(wf)
            assert bs.read() == testdata

        with open(tf) as inf:
            wf = Stream(inf)
            bs = BufferedStream(wf)
            bs.read(100)
            bs.seek(0)
            assert bs.tell() == 0
            assert bs.read() == testdata

        # seek into the buffer,
        # then read a chunk over it's size
        with open(tf) as inf:
            wf = Stream(inf)
            bs = BufferedStream(wf)
            bs.read(100)
            bs.seek(10)
            assert bs.tell() == 10
            assert bs.read(300) == testdata[10:10 + 300]
            
            
        # seek into the buffer,
        # then read a chunk over it's size
        with open(tf) as inf:
            wf = Stream(inf)
            bs = BufferedStream(wf)
            bs.read(100)
            bs.seek(10)
            assert bs.tell() == 10
            assert bs.read(20) == testdata[10:10 + 20]
            assert bs.tell() == 30
            assert bs.read(1000) == testdata[30:1000 + 30]
            assert bs.tell() == 1030

        
        # read the last character out of the
        # buffer. That caused an error at some time.
        with open(tf) as inf:
            wf = Stream(inf)
            bs = BufferedStream(wf)
            bs.read(100)
            bs.seek(99)
            assert bs.read(1) == testdata[99]

        
            
