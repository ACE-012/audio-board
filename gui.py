import threading
import tkinter
import os
import threading
from tkinter.constants import *
import player
from pynput.keyboard import Key, Listener
playerthread=player.player("none","none")
buttons=[]
class gui(threading.Thread):
    def __init__(self):
        super().__init__()
        self.Instance_root=tkinter.Tk()
        self.Instance_root.geometry("1280x720")
        self.Instance_root.title("GUI")
        self.Instance_root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.Instance_root.minsize(768,480)
        p1 = tkinter.PhotoImage(file = 'requirements\\play.png')
        self.Instance_root.iconphoto(False,p1)
        self.Instance_root.iconbitmap(default='requirements\\play.ico')
        self.options = []
        self.mydirs=[]
        self.buttons =[]
        self.newFrame=tkinter.Frame(self.Instance_root)
        self.newFrame.pack()
        for root, dirs, files in os.walk(".", topdown=False):
            self.mydirs=dirs
        self.dircheck()
        for dir in self.mydirs:
            self.options.append(dir)
        self.clicked = tkinter.StringVar()
        self.clicked.set("default")
        self.myfiles=[]
        self.drop = tkinter.OptionMenu(self.Instance_root , self.clicked , *self.options ,command=self.myprint)
        self.drop.pack(anchor=NW)
        self.dir=[]
        self.myprint([self.clicked.get()])
        self.Instance_root.mainloop()
    def dircheck(self):        
        for testdir in self.mydirs:
            i=0
            for root, testdirs, files in os.walk(testdir, topdown=False):
                for file in files:
                    if file[-3:]=="mp3" or file[-3:]=="wav" or file[-3:]=="ogg":
                        i+=1
            if i<=0:
                self.mydirs.remove(testdir)
                self.dircheck()
                break
    def close_window(self):
        os._exit(0)
    def mytrim(self,filename):
        filename=filename.replace("-"," ")
        filename=filename.replace("_"," ")
        temp=filename.split()
        return_string=""
        substractor=12
        if len(filename)>12:
            for word in temp:
                if len(return_string+" "+word)<substractor:
                    return_string=return_string+" "+word
                elif len(return_string+" "+word)>=substractor:
                    return_string=return_string+"\n"+word
                    substractor+=12
        else :
            return_string=filename
        return return_string 
    def myprint(self,args):
        if type(args)==list:
            args=args[0]
        self.currentdir=args
        for root, dirs, files in os.walk(args, topdown=False):
            self.myfiles=files
        self.newFrame.destroy()
        self.newFrame=tkinter.Frame(self.Instance_root)
        self.newFrame.pack(anchor=CENTER)
        self.buttons=[]
        i=0
        j=0
        buttons.clear()
        for file in self.myfiles:
            if file[-3:]=="mp3" or file[-3:]=="wav" or file[-3:]=="ogg":
                self.buttons.append(tkinter.Button(self.newFrame ,text = self.mytrim(file[:-4]), height=6,width=12,bd = '5',command=lambda c=file: self.play(args+"\\"+c)).grid(row=j,column=i))
                buttons.append(args+"\\"+file)
                if i<2:
                    i+=1
                else:
                    i=0
                    j+=1
                if j>=3:
                    break
    def run(self):
        pass
    def play(self,dir_name):
        playerthread=player.player(dir_name,"CABLE Input (VB-Audio Virtual Cable)")
        playerthread.start()

class mylistner(threading.Thread):
    def __init__(self):
        super().__init__()
    def on_press(self,key):
        if hasattr(key, 'vk') and 96 <= key.vk <= 105:
            if key.vk-97<len(buttons) and key.vk-97!=-1:
                playerthread=player.player(buttons[key.vk-97],"CABLE Input (VB-Audio Virtual Cable)")
                playerthread.start()
        # if type(key)==Key:
        #     if key==key.num_lock:
        #         os._exit(0)
    def run(self):
        with Listener(on_press=self.on_press) as listener:
            listener.join()
mylistner1=mylistner()
mylistner1.start()
threadgui=gui()
threadgui.start()