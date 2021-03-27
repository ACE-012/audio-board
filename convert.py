from os import path
import os
import threading
from pydub import AudioSegment

class convert_mp3_to_wav(threading.Thread):
    def __init__(self,filename):
        super().__init__()
        self.src = filename
        self.name=self.src[self.src.index("\\")+1:len(self.src)]
        self.name=self.name[:-4]
        self.dst = "temp\\"+self.name+".wav"
    def run(self):
        sound = AudioSegment.from_mp3(self.src)
        try :
            sound.export(self.dst, format="wav")
        except:
            os.mkdir("temp")
            sound.export(self.dst, format="wav")
