import ctypes
import time
from threading import Thread


class TimedOutThread(Thread):
    def __init__(self, timeout, target, args=(), kwargs=None) -> None:
        super().__init__()
        self._timeout = timeout
        self._target = target
        self._args = args
        self._kwargs = kwargs

    def _async_raise(self, tid, exctyp):
        """Ugly hack with ctypes"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctyp))

    def run(self) -> None:
        t = Thread(target=self._target, args=self._args, kwargs=self._kwargs)
        t.start()
        t.join(self._timeout)
        if t.is_alive():
            self._async_raise(t.ident, SystemExit)


if __name__ == '__main__':

    def foo(i, name='-'):
        try:
            for _i in range(i):
                print(i - _i, name)
                time.sleep(1)
        except SystemExit:
            print("Exc")
            raise

    print("start")
    t = TimedOutThread(3, foo, (6, 'thread'))
    t.start()
    t.join()
    print("stop")
    foo(3)
