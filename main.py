import threading
import tkinter
import os
import self_listner
from tkinter.constants import *
from tkinter.ttk import *
import sounddevice
import registry_writer
import list_of_devices
if registry_writer.reg_check(r"SOFTWARE\\virtual audio player"):
    registry_writer.read(r"SOFTWARE\\virtual audio player\\player")
else:
    registry_writer.create(r"SOFTWARE\\virtual audio player\\player")
    registry_writer.write(r"SOFTWARE\\virtual audio player\\player","pyaudio")
playervar="pyaudio"
if registry_writer.read(r"SOFTWARE\\virtual audio player\\player")=="pygame":
    import player_pygame as player
    playervar="pygame"
else :
    import player_pyaudio as player
    playervar="pyaudio"
from time import *
from pynput.keyboard import Key, Listener
if playervar=="pygame":
    playerthread=player.player("none","none")
else :
    playerthread=player.player("none",20)
buttons=[]
if playervar=="pyaudio":
    if registry_writer.read(r"SOFTWARE\\virtual audio player\\playback device id")!=None:
        playback_device_id=registry_writer.read(r"SOFTWARE\\virtual audio player\\playback device id")
        playback_device=registry_writer.read(r"SOFTWARE\\virtual audio player\\playback device")
    else:
        registry_writer.write(r"SOFTWARE\\virtual audio player\\playback device","none")
        registry_writer.write(r"SOFTWARE\\virtual audio player\\playback device id","0")
        playback_device=registry_writer.read(r"SOFTWARE\\virtual audio player\\playback device")
        playback_device_id=registry_writer.read(r"SOFTWARE\\virtual audio player\\playback device id")
    if registry_writer.read(r"SOFTWARE\\virtual audio player\\rec device id")!=None:
        rec_device_id=registry_writer.read(r"SOFTWARE\\virtual audio player\\rec device id")
        rec_device=registry_writer.read(r"SOFTWARE\\virtual audio player\\rec device")
    else:
        registry_writer.write(r"SOFTWARE\\virtual audio player\\rec device","none")
        registry_writer.write(r"SOFTWARE\\virtual audio player\\rec device id","0")
        rec_device=registry_writer.read(r"SOFTWARE\\virtual audio player\\rec device")
        rec_device_id=registry_writer.read(r"SOFTWARE\\virtual audio player\\rec device id")
else:
    playback_device=registry_writer.read(r"SOFTWARE\\virtual audio player\\playback device")
    rec_device=registry_writer.read(r"SOFTWARE\\virtual audio player\\rec device")
    # for i in list_of_devices.playbackdevices():
    #     if playback_device in i:
    #         playback_device=i
    # for i in list_of_devices.recdevices():
    #     if rec_device in i:
    #         rec_device=i
class gui(threading.Thread):

    def __init__(self,player):
        super().__init__()
        self.selflisten=self_listner.listen()
        self.Instance_root=tkinter.Tk()
        self.playbackdevices={}
        self.recdevices={}
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
        self.window2option_playback = tkinter.StringVar()
        self.window2option_playback.set(playback_device)
        self.window2option_rec = tkinter.StringVar()
        self.window2option_rec.set(rec_device)
        self.newFrame=tkinter.Frame(self.Instance_root)
        self.newFrame.pack()
        for root, dirs, files in os.walk(".", topdown=False):
            self.mydirs=dirs
        self.dircheck()
        for dir in self.mydirs:
            self.options.append(dir)
        self.clicked = tkinter.StringVar()
        self.clicked.set("default")
        self.toggle_btn_text=tkinter.StringVar()
        self.toggle_btn_text.set(player)
        self.myfiles=[]
        self.drop = tkinter.OptionMenu(self.Instance_root , self.clicked , *self.options ,command=self.myprint)
        self.drop.pack(anchor=NW)
        self.dir=[]
        self.myprint([self.clicked.get()])
        self.selflisten.start()
        self.mymenu()
        self.Instance_root.mainloop()
    def mymenu(self):
        self.mymenubar=tkinter.Menu(self.Instance_root)
        self.mymenuoptions=tkinter.Menu(self.mymenubar)
        self.mymenubar.add_cascade(label="menu",menu=self.mymenuoptions)
        self.mymenuoptions.add_command(label="settings",command=self.settings)
        self.Instance_root.config(menu=self.mymenubar)

    def settings(self):
        try:
            if self.newWindow.state() == "normal":
                self.newWindow.focus()
        except:
            self.newWindow = tkinter.Toplevel(self.Instance_root) 
            self.newWindow.title("Settings")
            self.newWindow.minsize(400,400)
            self.newWindow.geometry("400x400")
            self.toggle_button(self.newWindow)
            self.devices(self.newWindow)
    def devices(self,root):
        n=sounddevice.query_devices()
        j=0
        for i in n:
            if i['max_input_channels']<=0:
                if i['hostapi']==0:
                    if not bool(self.playbackdevices):
                       self.playbackdevices[i['name']]=j
                    else:
                        if  self.playbackdevices.get(i['name'])==None:
                            for d in list_of_devices.playbackdevices():
                                if i['name'] in d:
                                    self.playbackdevices[d]=j
            else:
                if i['hostapi']==0:
                    if not bool(self.recdevices):
                        self.recdevices[i['name']]=j
                    else:
                        if  self.recdevices.get(i['name'])==None:
                            for d in list_of_devices.recdevices():
                                if i['name'] in d:
                                    self.recdevices[d]=j
            j+=1
        tkinter.OptionMenu(root , self.window2option_playback , *self.playbackdevices ,command=self.playback).pack()
        tkinter.OptionMenu(root , self.window2option_rec , *self.recdevices ,command=self.rec_device).pack()
    def playback(self,text):
        registry_writer.write(r"SOFTWARE\\virtual audio player\\playback device",text)
        registry_writer.write(r"SOFTWARE\\virtual audio player\\playback device id",str(self.playbackdevices[text]))
        global playback_device,playback_device_id
        playback_device=text
        playback_device_id=self.playbackdevices[text]
    def rec_device(self,text):
        registry_writer.write(r"SOFTWARE\\virtual audio player\\rec device",text)
        registry_writer.write(r"SOFTWARE\\virtual audio player\\rec device id",str(self.recdevices[text]))
        global rec_device,rec_device_id
        rec_device=text
        rec_device_id=self.recdevices[text]
    def dircheck(self):
        for testdir in self.mydirs:
            if testdir=="temp":
                self.mydirs.remove("temp")
                self.dircheck()
            else:
                i=0
                for root, testdirs, files in os.walk(testdir, topdown=False):
                    for file in files:
                        if file[-3:]=="mp3" or file[-3:]=="wav" or file[-3:]=="ogg":
                            i+=1
                if i<=0:
                    self.mydirs.remove(testdir)
                    self.dircheck()
                    break
    def toggle_button(self,root):
        self.toggle_button_instance=tkinter.Button(root ,text=self.toggle_btn_text.get(), height=2,width=10,bd = '5',command=self.set_toggle_button)
        self.toggle_button_instance.pack()

    def set_toggle_button(self):
        if self.toggle_btn_text.get()=="pyaudio":
            self.toggle_btn_text.set("pygame")
            self.toggle_button_instance.configure(text=self.toggle_btn_text.get())
            registry_writer.write(r"SOFTWARE\\virtual audio player\\player","pygame")
        else:
            self.toggle_btn_text.set("pyaudio")
            self.toggle_button_instance.configure(text=self.toggle_btn_text.get())
            registry_writer.write(r"SOFTWARE\\virtual audio player\\player","pyaudio")

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
        j=3
        buttons.clear()
        for file in self.myfiles:
            if file[-3:]=="mp3" or file[-3:]=="wav" or file[-3:]=="ogg":
                self.buttons.append(tkinter.Button(self.newFrame ,text = self.mytrim(file[:-4]), height=6,width=12,bd = '5',command=lambda c=file: self.play(args+"\\"+c)).grid(row=j,column=i))
                buttons.append(args+"\\"+file)
                if i<2:
                    i+=1
                else:
                    i=0
                    j-=1
                if j<=0:
                    break

    def run(self):
        pass

    def play(self,dir_name):
        global playerthread
        if playerthread.is_alive():
            playerthread.stop()
        if playervar=="pygame":
            playerthread=player.player(dir_name,playback_device)
        else:
            playerthread=player.player(dir_name,9)
        playerthread.start()

class mylistner(threading.Thread):

    def __init__(self):
        super().__init__()

    def on_press(self,key):
            if hasattr(key, 'vk') and 96 <= key.vk <= 105:
                global playerthread
                if key.vk-97<len(buttons) and key.vk-97!=-1:
                    if playerthread.is_alive():
                        playerthread.stop()
                    
                    if playervar=="pygame":
                        playerthread=player.player(buttons[key.vk-97],playback_device)
                    else:
                        playerthread=player.player(buttons[key.vk-97],int(playback_device_id))
                    playerthread.start()
                if key.vk-96==0:
                    playerthread.stop()
        # if type(key)==Key:
        #     if key==key.num_lock:
        #         os._exit(0)

    def run(self):

        with Listener(on_press=self.on_press) as listener:
            listener.join()
class main(threading.Thread):

    def __init__(self):
        super().__init__()
        self.mylistner1=mylistner()
        self.mylistner1.start()

    def run(self):

        if self.mylistner1.is_alive()==False:
            self.mylistner1=mylistner()
            self.mylistner1.start()
        sleep(1)
        self.run()

mainthread=main()
mainthread.start()
threadgui=gui(player=registry_writer.read(r"SOFTWARE\\virtual audio player\\player"))
threadgui.start()