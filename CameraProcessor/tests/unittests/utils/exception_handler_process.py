from __future__ import print_function
import multiprocessing
from multiprocessing import Process, Pipe
import traceback


class EProcess(multiprocessing.Process):
    """Variation of Process that sends back exceptions

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pconn, self._ccon = Pipe()
        self._exception = None

    def run(self):
        try:
            Process.run(self)
            self._ccon.send(None)
        except Exception as e:
            traceback.print_exc()
            self._ccon.send(e)
            raise e

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception
