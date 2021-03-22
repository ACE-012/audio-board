import sounddevice as sd
import soundfile as sf
import threading
from threading import Thread
import convert
import os
import time
class player(threading.Thread):
    def __init__(self,audio,deviceid1,deviceid2):
        super().__init__()
        self.audio=audio
        self.device1=deviceid1
        self.device2=deviceid2
        self.playing=True
    def check(self,audio):
        if audio[-3]!="wav":
            t=convert.convert_mp3_to_wav(audio)
            found=False
            for root, dirs, files in os.walk("temp", topdown=False):
                for file in files:
                    if file==(t.name+".wav"):
                        found=True
                        break
            if found:
                self.audio=t.dst
            else:
                t.start()
                self.audio=t.dst
                time.sleep(1)
    def run(self):
        self.check(self.audio)
        self.t1=Thread(target=self.audio1,args=(self.audio,self.device1,))
        self.t2=Thread(target=self.audio2,args=(self.audio,self.device2,))
        self.t1.start()
        self.t2.start()
    def audio2(self,audio,deviceid):
        data1, fs1 = sf.read(audio, dtype='float32')
        def check1():
            while True:
                print("checking")
                if self.playing==False:
                    print("stopping")
                    sd.stop()
                    break
                time.sleep(0.75)
        # Thread(target=check1).start()
        sd.play(data1, fs1, device=deviceid,blocking=True)
    def audio1(self,audio,deviceid):
        pass
        # data2, fs2 = sf.read(audio, dtype='float32')
        # def check1():
        #     while True:
        #         print("checking")
        #         if self.playing==False:
        #             print("stopping")
        #             sd.stop()
        #             break
        #         time.sleep(0.75)
        # Thread(target=check1).start()
        # sd.play(data2, fs2, device=deviceid,blocking=True)
        # self.stop()
    def stop(self):
        sd.stop()
if __name__=="__main__":
    p=player("default\\hello there.mp3",5,8).start()