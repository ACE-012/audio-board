from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import time
import pygame
import threading
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.ogg import OggFileType
from pynput.keyboard import Controller
class player(threading.Thread):
    def __init__(self,name,device,key=None,pushtotalk=False):
        super().__init__()
        print(device)
        self.audioname=name
        if name!="none" or device!="none":
            pygame.mixer.pre_init(devicename=device)
        pygame.mixer.init()
        self.pushtotalk=pushtotalk
        self.running=True
        if pushtotalk:
            self.pushkey=key
            self.c=Controller()
    def stop(self):
        if self.audioname!="none":
            pygame.mixer.quit()
            self.running=False
    def run(self):
        if self.audioname!="none":
            pygame.mixer.music.load(self.audioname)
            if self.audioname[-3:]=="mp3":
                self.song = MP3(self.audioname)
            elif self.audioname[-3:]=="wav":
                self.song=WAVE(self.audioname)
            elif self.audioname[-3:]=="ogg":
                self.song=OggFileType(self.audioname)#not tested
            self.songLength = self.song.info.length
            if self.pushtotalk:
                self.c.press(self.pushkey)
            pygame.mixer.music.play()
            while self.running==True and pygame.mixer.music.get_busy()==True:
                time.sleep(0.5)
                pass
            if self.pushtotalk:
                self.c.release(self.pushkey)