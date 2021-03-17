import threading
from playsound import playsound
class myplaysound(threading.Thread):
    def __init__(self,file):
        super().__init__()
        self.filename=file
    def run(self):
        self.p = playsound(self.filename)
    def stop(self):
        s=1+"s"