import pygame._sdl2 as sdl2
import pygame
import time

pygame.init()
def playbackdevices():
    is_capture = 0
    num = sdl2.get_num_audio_devices(is_capture)
    names = [str(sdl2.get_audio_device_name(i, is_capture), encoding="utf-8") for i in range(num)]
    return names
def recdevices():
    is_capture = 1
    num = sdl2.get_num_audio_devices(is_capture)
    names = [str(sdl2.get_audio_device_name(i, is_capture), encoding="utf-8") for i in range(num)]
    return names