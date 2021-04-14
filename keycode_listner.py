from tkinter.constants import BOTH
from pynput.keyboard import Key,Listener
from time import sleep
btn=None
listener=None
def on_press(key):
    # print(getstr(key))
    global btn
    btn=key
    listener.stop()
def getstr(key):
    if hasattr(key,'char'):
        return str(key.char)
    elif type(key)==Key:
        for v in Key:
            if key==v:
                return str(v)
def check(key,key1):
    key=getstr(key)
    key1=getstr(key1)
    if key==key1:
        return True
    else:
        return False
def get_button_str():
    global listener
    listener=Listener(on_press=on_press)
    listener.start()
    while listener.is_alive():
        sleep(0.1)
    return getstr(btn)
if __name__=='__main__':
    with Listener(on_press=on_press) as listener:
        listener.join()