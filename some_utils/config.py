# Author: Teshan Liyanage <teshanuka@gmail.com>


import yaml
import re


class ConfigLoader:
    """For json/yaml configs with string keys"""
    data: dict = None
    sep = '/'

    def __init__(self, file_path=None, string=None, dict_=None, sep='/', validate=True):
        assert sum(bool(k) for k in [file_path, string, dict_]) == 1, \
            "One of the parameters `file_name/string/dict_` must be provided"

        self.sep = sep

        if file_path:
            with open(file_path) as f:
                self.data = yaml.safe_load(f)
        elif string:
            self.data = yaml.safe_load(string)
        elif dict_:
            self.data = dict_

        if validate:
            self.validate(self.data, self.sep)

    @staticmethod
    def validate(data, sep=None):
        if sep is None:
            sep = ConfigLoader.sep
        for k, v in data.items():
            if not (isinstance(k, str)):
                raise AttributeError(f"All keys should be string to use this class. '{k}' is not")
            if sep in k:
                raise AttributeError(f"Keys should not contain the separator '{sep}'")
            if isinstance(v, dict):
                ConfigLoader.validate(v, sep)

    def __getitem__(self, key):
        keys = key.split(self.sep)
        v = self.data[keys[0]]
        for k in keys[1:]:
            try:
                v = v[k]
            except (TypeError, KeyError):
                raise KeyError(f"Invalid path. In path '{key}', key '{k}' not found")
        return v

    def __contains__(self, key):
        try:
            _ = self[key]
            return True
        except KeyError:
            return False

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


class Dict2Str:
    """Encode a dictionary with (str, number/bool) pairs to a unique string and decode string to a the original dict"""
    def __init__(self, properties: dict):
        """Encode a dictionary with (str, number/bool) pairs to a unique string and decode string to a the original dict

        :param properties: Dict with {'key': {<description>}}
            The `description` can have below key/value pairs
                `ignore` (bool) - ignore this param when encoding
                `letter` (ascii alphanumeric) - associated letter to the key
                `multi_factor` (number) - number is multiplied by this and converted to int
                `is_bool` (bool) - whether the param is a bool
                `negative` (bool) - this number can be negative
                `map` (dict) - custom mapping from arg to int values
        """
        from copy import deepcopy
        from string import ascii_letters

        _letters = [_l for _l in ascii_letters]
        for v in properties.values():
            if 'letter' in v:
                if not v['letter'] in _letters:
                    raise ValueError(f"Letter {v['letter']} invalid. Did you duplicate letters? Or used a non ascii letter?")
                _letters.remove(v['letter'])

        self._properties = deepcopy(properties)
        self._decode_fmt = ''
        self._ignore_keys = []
        for k, v in self._properties.items():
            if 'ignore' in v and v['ignore']:
                self._ignore_keys.append(k)
                continue
            if 'letter' not in v:
                v['letter'] = _letters.pop(0)
            v.setdefault('multi_factor', 1)
            v.setdefault('is_bool', False)

            if v.get('negative', False):
                self._decode_fmt += rf"{v['letter']}(-?\d+)"
            else:
                self._decode_fmt += rf"{v['letter']}(\d+)"

    def encode(self, d: dict):
        s = ''
        for k, v in d.items():
            if k in self._ignore_keys:
                continue
            if k not in self._properties:
                raise KeyError(f"Key '{k}' not recognized. Expected keys: {self._properties.keys()}")

            if 'map' in self._properties[k]:
                assert isinstance(self._properties[k]['map'][v], int), "Mapping is expected to map to int values"
                s += f"{self._properties[k]['letter']}{self._properties[k]['map'][v]}"
            else:
                assert isinstance(v, (int, float, bool)), f"Key: {k}; Expected types are `(int, float, bool)`. " \
                                                          f"Got '{v}' of type {type(v)}. Specify a `map` for this " \
                                                          "key if this value is of none of these types"
                if isinstance(v, bool):
                    s += f"{self._properties[k]['letter']}{1 if v else 0}"
                else:
                    s += f"{self._properties[k]['letter']}{int(v*self._properties[k]['multi_factor'])}"
        return s

    def decode(self, s: str):
        try:
            vs = re.search(self._decode_fmt, s).groups()
        except AttributeError as e:
            raise AttributeError(f"Expected string matching format '{self._decode_fmt}'") from e
        ret = {}
        for (k, v), val in zip(self._properties.items(), map(int, vs)):
            if 'map' in v:
                r_map = {_v: _k for _k, _v in v['map'].items()}
                ret[k] = r_map[val]
            elif v['is_bool']:
                ret[k] = bool(val)
            else:
                ret[k] = val / v['multi_factor']
                if ret[k].is_integer():
                    ret[k] = int(ret[k])
        return ret


if __name__ == '__main__':
    cfg_ = ConfigLoader(dict_={'p': 5, 'q': 10})

    d_ = Dict2Str({k: {} for k in cfg_.data})
    print(s_ := d_.encode(cfg_.data))
    print(d_.decode(s_))
