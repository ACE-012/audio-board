from winreg import *
from contextlib import suppress
import os
def reg_check(path):
    try:
        reg = ConnectRegistry(None, HKEY_CURRENT_USER)
        k = OpenKey(reg, path)
        return True
    except:
        return False
def read(path, root=HKEY_CURRENT_USER):
    path, name = os.path.split(path)
    with suppress(FileNotFoundError), OpenKey(root, path) as key:
        return QueryValueEx(key, name)[0]
def write(path, value, root=HKEY_CURRENT_USER):
    path, name = os.path.split(path)
    with OpenKey(root, path, 0, KEY_WRITE) as key:
        SetValueEx(key, name, 0, REG_SZ, value)
def create(path,root=HKEY_CURRENT_USER):
    CreateKey(root, r'SOFTWARE\\virtual audio player')