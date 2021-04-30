import sounddevice as sd
import soundfile as sf
import threading
import convert
import os
import time
from pynput.keyboard import Controller
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.ogg import OggFileType
from pynput.keyboard import Controller
class player_pyaudio(threading.Thread):
    def __init__(self,audio,deviceid,key=None,pushtotalk=False):
        super().__init__()
        self.audio=audio
        self.device=deviceid
        self.pushtotalk=pushtotalk
        if self.pushtotalk:
            self.pushkey=key
            self.c=Controller()
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
                while t.is_alive():
                    time.sleep(0.5)
                    pass
    def run(self):
        self.check(self.audio)
        self.audio_play(self.audio,self.device)
    def audio_play(self,audio,deviceid):
        if self.pushtotalk:
            self.c.press(self.pushkey)
        data, fs = sf.read(audio, dtype='float32')
        sd.play(data, fs, device=deviceid,blocking=True)
        if self.pushtotalk:
            self.c.release(self.pushkey)
        time.sleep(1)
    def stop(self):
        sd.stop()
class player_pygame(threading.Thread):
    def __init__(self,name,device,key=None,pushtotalk=False):
        super().__init__()
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