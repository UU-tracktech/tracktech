"""Mock exception handler for testing.

"""
from __future__ import print_function
import multiprocessing
from multiprocessing import Process, Pipe
import traceback


class EProcess(multiprocessing.Process):
    """Variation of Process that sends back exceptions

    """
    def __init__(self, *args, **kwargs):
        """Runs multiprocessing.Process init with the arguments

        """
        super().__init__(*args, **kwargs)
        self._pconn, self._ccon = Pipe()
        self._exception = None

    def run(self):
        """Runs the process run with an added exception handler that sends the exception back

        """
        try:
            Process.run(self)
            self._ccon.send(None)
        except Exception as exc:
            traceback.print_exc()
            self._ccon.send(exc)
            raise exc

    @property
    def exception(self):
        """Exception property

        Returns:
            The exception raised, or None if no exception was raised

        """
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception
