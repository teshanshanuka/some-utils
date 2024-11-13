# Author: Teshan Liyanage <teshanuka@gmail.com>


import os
import pickle
from functools import wraps


def simple_cache(file):
    def decor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if os.path.exists(file):
                with open(file, 'rb') as fd:
                    ret = pickle.load(fd)
                return ret
            ret = func(*args, **kwargs)
            with open(file, 'wb') as fd:
                pickle.dump(ret, fd)
            return ret

        return wrapper

    return decor


if __name__ == '__main__':

    @simple_cache('tmp.pkl')
    def mult(a, b):
        return a * b

    print(mult(2, 5))
