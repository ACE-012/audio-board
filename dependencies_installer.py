import pip
#Dependencies:
#pynput
#tkinter
#mutagen
#playsound
#pygame
#sounddevice
def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

# Example
if __name__ == '__main__':
    install('pynput')
    install('mutagen')
    install('playsound')
    install('pygame')
    install('sounddevice')