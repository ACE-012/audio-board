from winreg import *
from contextlib import suppress
import os
def read(path, root=HKEY_CURRENT_USER):
    path, name = os.path.split(path)
    with suppress(FileNotFoundError), OpenKey(root, path) as key:
        return QueryValueEx(key, name)[0]
def write(path, value, root=HKEY_CURRENT_USER):
    path, name = os.path.split(path)
    with OpenKey(root, path, 0, KEY_WRITE) as key:
        SetValueEx(key, name, 0, REG_SZ, value)