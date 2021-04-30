import sounddevice as sd
import numpy
assert numpy
import time
import threading

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata
class listen(threading.Thread):
    def __init__(self,input,output,channels=2):
        super().__init__()
        self.running=True
        self.inputdevice=input
        self.outputdevice=output
        self.channels=channels
    def run(self):
        try:
            with sd.Stream(device=(int(self.inputdevice), int(self.outputdevice)),
                           channels=self.channels, callback=callback):
                while self.running:
                    time.sleep(0.01)
        except KeyboardInterrupt:
            exit('')
        except Exception as e:
            exit(type(e).__name__ + ': ' + str(e))