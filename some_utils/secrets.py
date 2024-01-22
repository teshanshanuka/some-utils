# Author: Teshan Liyanage <teshanuka@gmail.com>

from abc import ABC, abstractmethod
from getpass import getpass
import os
import re

import keyring


def set_passwd(app: str, usr: str, passwd: str = None, input_=False, set_prompt=""):
    if (passwd is None) is not input_:
        raise RuntimeError("Either `passwd` or `input_` argument must be given")
    if input_:
        passwd = getpass(set_prompt)
    keyring.set_password(app, usr, passwd)


def get_passwd(app: str, usr: str, set_=False, set_prompt=""):
    passwd = keyring.get_password(app, usr)
    if passwd or not set_:
        return passwd
    set_passwd(app, usr, input_=True, set_prompt=set_prompt)
    return keyring.get_password(app, usr)


class SecretStorage(ABC):
    @abstractmethod
    def _get_password(self, app, key) -> str:
        """Get from secret storage"""

    @abstractmethod
    def _set_password(self, app, key, pwd) -> None:
        """Set password for app:key"""

    @abstractmethod
    def _delete_password(self, app, key) -> None:
        """Delete from secret storage"""

    def set(self, app: str, usr: str, passwd: str = None, input_=False, set_prompt=""):
        if (passwd is None) is not input_:
            raise RuntimeError("Either `passwd` or `input_` argument must be given")
        if input_:
            passwd = getpass(set_prompt)
        self._set_password(app, usr, passwd)

    def get(self, app: str, usr: str, set_=False, set_prompt=""):
        passwd = self._get_password(app, usr)
        if passwd or not set_:
            return passwd
        self.set(app, usr, input_=True, set_prompt=set_prompt)
        return self._get_password(app, usr)

    def delete(self, app: str, usr: str):
        self._delete_password(app, usr)


class KeyRingSecrets(SecretStorage):
    def _get_password(self, app, key):
        return keyring.get_password(app, key)

    def _set_password(self, app, key, pwd):
        return keyring.set_password(app, key, pwd)

    def _delete_password(self, app, key) -> None:
        return keyring.delete_password(app, key)


class EnvVarSecrets(SecretStorage):
    @staticmethod
    def get_var_name(app, key):
        var_name = f"{app}_{key}".upper()
        if not re.match(r"\w+", var_name):
            raise ValueError(f"app and key must match r'\w+' - got {app=} {key=} {var_name=}")
        return var_name

    def _get_password(self, app, key) -> str:
        var_name = self.get_var_name(app, key)
        return os.getenv(var_name)

    def _set_password(self, app, key, pwd) -> None:
        var_name = self.get_var_name(app, key)
        os.environ[var_name] = pwd

    def _delete_password(self, app, key) -> None:
        self._set_password(app, key, '')
