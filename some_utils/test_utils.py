# Author: Teshan Liyanage <teshanuka@gmail.com>


def compare(a, b, keys=''):
    """Compare iterables of iterables element-wise recursively"""
    if isinstance(a, (list, tuple)):
        assert isinstance(b, (list, tuple)), f"Keys: {keys} - `a` is iterable `b` is not"
        assert len(a) == len(b), f"Keys: {keys} - Lengths are different"
        for _a, _b in zip(a, b):
            compare(_a, _b, keys)
    elif isinstance(a, dict):
        assert isinstance(b, dict), f"Keys: {keys} - `a` is dict `b` is not"
        for k, v in a.items():
            assert k in b, f"Keys: {keys} - Expected key `{k}` not in `b`"
            compare(v, b[k], keys+f'[{k}]')
    else:
        assert a == b, f"Keys: {keys} - Expected: {a} Got: {b}"
        
class Version(tuple):
    _n_ids = 3
    def __new__(cls, string):
        vals = string.split('.')
        vals += ('0',)*(cls._n_ids-len(vals))
        return tuple.__new__(cls, map(int, vals))
