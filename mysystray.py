from pystray import *
import threading
from PIL import Image

class mytray(threading.Thread):
    def __init__(self,windowthread,overlaythread):
        super().__init__()
        self.image = Image.open("requirements\\play.ico")
        self.menu = Menu(
            MenuItem(
                'Open Main Window', 
                self.setvalue,
                default=True),
            MenuItem(
                'Overlay',
                self.setoverlay,
                checked=lambda item:self.overlaythread.get()),
            MenuItem(
                'Open Settings', 
                self.settings),
            Menu.SEPARATOR, 
            MenuItem(
                'Exit', 
                self.exit))
        self.windowthread=windowthread
        self.overlaythread=overlaythread
    def test(self,boo):
        print(boo)
    def setvalue(self):
        self.windowthread.set("main")
    def settings(self):
        self.windowthread.set("settings")
    def setoverlay(self,item,item1):
        self.overlaythread.set(not item1.checked)
    def exit(self):
        os._exit(0)
    def run(self):
        self.trayicon=Icon(name ="Player", icon =self.image, title ="Player", menu =self.menu)
        self.trayicon.HAS_DEFAULT_ACTION = True
        self.trayicon.run()
    def stop(self):
        self.trayicon.stop()
if __name__=='__main__':
    t=mytray()
    t.start()
    print("test")
