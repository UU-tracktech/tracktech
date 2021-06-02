"""Mock exception handler for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from __future__ import print_function
import multiprocessing
from multiprocessing import Process, Pipe
import traceback


class EProcess(multiprocessing.Process):
    """Variation of Process that sends back exceptions.

    Attributes:
        _pconn (Connection): One of two process connections.
        _ccon (Connection): One of two process connections.
        _exception (): Property an exception is put inside
    """
    def __init__(self, *args, **kwargs):
        """Runs multiprocessing.Process init with the arguments.

        Args:
            **kwargs (Any): Other arguments given to the function.
        """
        super().__init__(*args, **kwargs)
        self._pconn, self._ccon = Pipe()
        self._exception = None

    def run(self):
        """Runs the process run with an added exception handler that sends the exception back."""
        try:
            Process.run(self)
            self._ccon.send(None)
        except Exception as exc:
            traceback.print_exc()
            self._ccon.send(exc)
            raise exc

    @property
    def exception(self):
        """Exception property.

        Returns:
            Exception: The exception raised, or None if no exception was raised.
        """
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception
