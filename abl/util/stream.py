

class Stream(object):
    """
    A very simple class that makes every file-like object a simple
    stream that only offers the read()-method.

     - **stream** the stream to wrap
    """

    def __init__(self, stream):
        self.stream = stream


    def read(self, n=-1):
        return self.stream.read(n)

    
        

class BufferedStream(object):


    def __init__(self, stream, bufsize=8192):
        self.stream = stream
        self.bufsize = bufsize
        self.pos = 0
        self.bufferoffset = 0
        self.buffer = ''


    def _read_from_stream(self, n=-1):
        data = self.stream.read(n)
        self.pos += len(data)
        return data
    

    def read(self, n=-1):
        # read everything. 
        if n == -1:
            res = ''
            if self.bufferoffset:
                res += self.buffer[self.bufferoffset:]
                self.bufferoffset = 0
            res += self._read_from_stream()
            self.buffer = res[-self.bufsize:]
            return res
        else:
            res = ''
            more = ''
            if self.bufferoffset:
                res += self.buffer[self.bufferoffset:self.bufferoffset + n]
                self.bufferoffset += n
                # we need to read something from the stream
                # to fulfill the request
                if self.bufferoffset > 0:
                    more = self._read_from_stream(self.bufferoffset)
                    self.bufferoffset = 0
            else:
                more = self._read_from_stream(n)

            # append + shift the buffer
            if more:
                res += more
                self.buffer = (self.buffer + more)[-self.bufsize:]

            return res
        

    def seek(self, position):
        assert position <= self.pos
        if position == self.pos:
            return
        assert self.pos - position <= len(self.buffer)
        self.bufferoffset = position - self.pos

        
