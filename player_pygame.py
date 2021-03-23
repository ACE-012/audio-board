from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import time
import pygame
import threading
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.ogg import OggFileType
class player(threading.Thread):
    def __init__(self,name,device):
        super().__init__()
        self.audioname=name
        self.thispygame=pygame
        if name!="none" or device!="none":
            self.thispygame.mixer.pre_init(devicename=device)
        self.thispygame.mixer.init()
        # self.p = test.myplaysound(self.audioname)
    def stop(self):
        if self.audioname!="none":
            self.thispygame.mixer.quit()
        # self.p.stop()
    def run(self):
        if self.audioname!="none":
            self.thispygame.mixer.music.load(self.audioname)
            if self.audioname[-3:]=="mp3":
                self.song = MP3(self.audioname)
            elif self.audioname[-3:]=="wav":
                self.song=WAVE(self.audioname)
            elif self.audioname[-3:]=="ogg":
                self.song=OggFileType(self.audioname)#not tested
            self.songLength = self.song.info.length
            self.thispygame.mixer.music.play()
            # while self.thispygame.mixer.get_busy():
            #     time.sleep(int(self.songLength))
# thread1 = player("default\\bubble_gum.mp3","CABLE Input (VB-Audio Virtual Cable)")
# thread1.start()
# print("started")