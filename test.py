from pynput.keyboard import Key,Listener
import os
def on_press(key):
    print(key)
    if type(key)==Key:
        if key==key.esc:
            os._exit(0)
with Listener(on_press=on_press) as listener:
    listener.join()