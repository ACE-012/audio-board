import threading
import os
import self_listner
from tkinter.constants import *
from tkinter import *
import sounddevice
import registry_writer
import list_of_devices
import actual_mic_listner
from time import *
import tkinter.messagebox
from pynput.keyboard import Key,Listener
buttons=[]
foldername=None
pushtotalkpressed=False
playervar="pyaudio"
functionkeys={}
if registry_writer.reg_check(r"SOFTWARE\\virtual audio player"):
    registry_writer.read(r"SOFTWARE\\virtual audio player\\player")
    firstrun=False
    actual_playback_device=registry_writer.read(r"SOFTWARE\\virtual audio player\\actual playback device")
    actual_playback_device_id=registry_writer.read(r"SOFTWARE\\virtual audio player\\actual playback device id")
    actual_rec_device=registry_writer.read(r"SOFTWARE\\virtual audio player\\actual rec device")
    actual_rec_device_id=registry_writer.read(r"SOFTWARE\\virtual audio player\\actual rec device id")
    playback_device=registry_writer.read(r"SOFTWARE\\virtual audio player\\playback device")
    playback_device_id=registry_writer.read(r"SOFTWARE\\virtual audio player\\playback device id")
    rec_device_id=registry_writer.read(r"SOFTWARE\\virtual audio player\\rec device id")
    rec_device=registry_writer.read(r"SOFTWARE\\virtual audio player\\rec device")
    pushtotalkkey=registry_writer.read(r"SOFTWARE\\virtual audio player\\push to talk key")
    useovarlay=registry_writer.read(r"SOFTWARE\\virtual audio player\\overlay")
    for i in range(12):
        functionkeys["f"+str(i+1)]=registry_writer.read(r"SOFTWARE\\virtual audio player\\f"+str(i+1))
else:
    registry_writer.create(r"SOFTWARE\\virtual audio player\\player")
    firstrun=True
    registry_writer.write(r"SOFTWARE\\virtual audio player\\player","pyaudio")
    registry_writer.write(r"SOFTWARE\\virtual audio player\\actual playback device id","0")
    registry_writer.write(r"SOFTWARE\\virtual audio player\\actual playback device","None")
    registry_writer.write(r"SOFTWARE\\virtual audio player\\playback device","none")
    registry_writer.write(r"SOFTWARE\\virtual audio player\\playback device id","0")
    registry_writer.write(r"SOFTWARE\\virtual audio player\\actual rec device id","0")
    registry_writer.write(r"SOFTWARE\\virtual audio player\\actual rec device","None")
    registry_writer.write(r"SOFTWARE\\virtual audio player\\rec device","none")
    registry_writer.write(r"SOFTWARE\\virtual audio player\\rec device id","0")
    registry_writer.write(r"SOFTWARE\\virtual audio player\\push to talk key","None")
    registry_writer.write(r"SOFTWARE\\virtual audio player\\overlay","False")
    actual_playback_device=registry_writer.read(r"SOFTWARE\\virtual audio player\\actual playback device")
    actual_playback_device_id=registry_writer.read(r"SOFTWARE\\virtual audio player\\actual playback device id")
    actual_rec_device=registry_writer.read(r"SOFTWARE\\virtual audio player\\actual rec device")
    actual_rec_device_id=registry_writer.read(r"SOFTWARE\\virtual audio player\\actual rec device id")
    playback_device_id=registry_writer.read(r"SOFTWARE\\virtual audio player\\playback device id")
    playback_device=registry_writer.read(r"SOFTWARE\\virtual audio player\\playback device")
    rec_device=registry_writer.read(r"SOFTWARE\\virtual audio player\\rec device")
    rec_device_id=registry_writer.read(r"SOFTWARE\\virtual audio player\\rec device id")
    pushtotalkkey=registry_writer.read(r"SOFTWARE\\virtual audio player\\push to talk key")
    useovarlay=registry_writer.read(r"SOFTWARE\\virtual audio player\\overlay")
    for i in range(12):
        registry_writer.write(r"SOFTWARE\\virtual audio player\\f"+str(i+1),"None")
        functionkeys["f"+str(i+1)]="None"
if registry_writer.read(r"SOFTWARE\\virtual audio player\\player")=="pygame":
    import player_pygame as player
    playervar="pygame"
else :
    import player_pyaudio as player
    playervar="pyaudio"
if playervar=="pygame":
    playerthread=player.player("none","none")
else :
    playerthread=player.player("none",20)
if len(pushtotalkkey)>1 or len(pushtotalkkey)<1:
    pushtotalk=False
else :
    pushtotalk=True
selflisten=self_listner.listen(rec_device_id,actual_playback_device_id)
actualmiclisten=actual_mic_listner.listen(actual_rec_device_id,playback_device_id)
class gui(threading.Thread):

    def __init__(self,player):
        super().__init__()
        self.Instance_root=Tk()
        self.playbackdevices={}
        self.recdevices={}
        self.Instance_root.geometry("1280x720")
        self.Instance_root.title("GUI")
        self.Instance_root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.Instance_root.minsize(768,480)
        p1 = PhotoImage(file = 'requirements\\play.png')
        self.Instance_root.iconphoto(False,p1)
        self.Instance_root.iconbitmap(default='requirements\\play.ico')
        self.options = []
        self.mydirs=[]
        self.buttons =[]
        self.overlayframe=Frame()
        self.window2option_playback = StringVar()
        self.window2option_playback.set(playback_device)
        self.window2option_rec = StringVar()
        self.window2option_rec.set(rec_device)
        self.window2option_actual_playback = StringVar()
        self.window2option_actual_playback.set(actual_playback_device)
        self.window2option_actual_rec = StringVar()
        self.window2option_actual_rec.set(actual_rec_device)
        self.newFrame=Frame(self.Instance_root)
        self.newFrame.pack()
        self.pushtotalktext=StringVar()
        self.pushtotalktext.set(pushtotalkkey)
        self.pushtotalktext.trace("w", lambda name, index, mode, sv=self.pushtotalktext: self.pushtotalkkeychange(sv))
        for root, dirs, files in os.walk(".", topdown=False):
            self.mydirs=dirs
        self.dircheck()
        for dir in self.mydirs:
            self.options.append(dir)
        if firstrun:
            self.folderasign()
            tkinter.messagebox.showinfo("Notice",  "Please Configure it via settings under the menu button")
        global foldername
        foldername=StringVar()
        foldername.set("default")
        foldername.trace("w", lambda name, index, mode, sv=foldername: self.callback(sv))
        self.toggle_btn_text=StringVar()
        self.toggle_btn_text.set(player)
        self.myfiles=[]
        self.drop = OptionMenu(self.Instance_root , foldername , *self.options)
        self.drop.pack(anchor=NW)
        self.dir=[]
        self.overlayvar=BooleanVar()
        self.overlayvar.set(useovarlay)
        self.myprint([foldername.get()])
        self.mymenu()
        selflisten.start()
        if self.overlayvar.get()==True:
            self.mycreateoverlay()
        self.Instance_root.mainloop()
    def mymenu(self):
        self.mymenubar=Menu(self.Instance_root)
        self.mymenuoptions=Menu(self.mymenubar)
        self.mymenubar.add_cascade(label="menu",menu=self.mymenuoptions)
        self.mymenuoptions.add_command(label="settings",command=self.settings)
        self.Instance_root.config(menu=self.mymenubar)
    def folderasign(self):
        global functionkeys
        i=1
        for dir in self.mydirs:
            if i<=12 and functionkeys["f"+str(i)]=="None":
                functionkeys["f"+str(i)]=dir
                registry_writer.write(r"SOFTWARE\\virtual audio player\\f"+str(i),dir)
            i+=1
    def pushtotalkkeychange(self,textvar):
        global pushtotalkkey,pushtotalk
        registry_writer.write(r"SOFTWARE\\virtual audio player\\push to talk key",str(textvar.get()).lower())
        pushtotalkkey=str(textvar.get()).lower()
        self.pushtotalktext.set(str(textvar.get()).lower())
        if len(pushtotalkkey)>1 or len(pushtotalkkey)<1:
            pushtotalk=False
        else :
            pushtotalk=True
    def settings(self):
        try:
            if self.newWindow.state() == "normal":
                self.newWindow.focus()
        except:
            self.newWindow = Toplevel(self.Instance_root) 
            self.newWindow.title("Settings")
            self.newWindow.minsize(400,400)
            self.newWindow.geometry("400x400")
            self.overlaycheckbox=Checkbutton(self.newWindow,text="Use Overlay ?",variable=self.overlayvar ,onvalue=True,offvalue=False,command=self.myoverlay).pack()
            self.toggle_button(self.newWindow)
            self.devices()
    def myoverlay(self):
        registry_writer.write(r"SOFTWARE\\virtual audio player\\overlay",str(self.overlayvar.get()))
        if self.overlayvar.get()==True:
            self.mycreateoverlay()
        else:
            self.destroyoverlay()
    def mycreateoverlay(self):
        try:
            if self.overlaywindow.state() == "normal":
                self.overlaywindow.focus()
        except:
            self.overlaywindow = Toplevel(self.Instance_root)
            self.overlaywindow.attributes("-fullscreen", True)
            self.overlaywindow.attributes("-transparentcolor", "red")
            self.overlayframe=Frame(self.overlaywindow,bg="red",borderwidth=10)
            self.overlayframe.pack(anchor=CENTER,ipady=self.Instance_root.winfo_screenheight(),ipadx=self.Instance_root.winfo_screenwidth())
            l=Label(self.overlayframe, textvariable=foldername)
            l.pack(anchor=NW)
            self.mylist()
            self.overlaywindow.wm_attributes("-topmost", True)
    def mylist(self):
        try :
            self.l1.destroy()
        except:
            pass
        self.l1=Listbox(self.overlayframe,width=10,height=9)
        b=[]
        for i in buttons:
            temp=i[:-4]
            if foldername.get() in temp:
                temp=temp.replace(foldername.get(),"")
                temp=temp.replace("\\","")
            b.append(temp)
        self.l1.insert(1,*b)
        self.l1.configure(state=DISABLED)
        self.l1.pack(anchor=E)
    def destroyoverlay(self):
        try:
            self.overlaywindow.destroy()
        except:
            pass
    def devices(self):
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
        virtualframe=Frame(self.newWindow)
        actualframe=Frame(self.newWindow)
        Label(virtualframe, text="Virtual driver").pack()
        Label(actualframe, text="Actual driver").pack()
        text=Entry(self.newWindow ,textvariable=self.pushtotalktext)
        text.pack()
        OptionMenu(virtualframe , self.window2option_playback , *self.playbackdevices ,command=self.playback).pack()
        OptionMenu(virtualframe , self.window2option_rec , *self.recdevices ,command=self.rec_device).pack()
        OptionMenu(actualframe , self.window2option_actual_playback , *self.playbackdevices ,command=self.actual_playback).pack()
        OptionMenu(actualframe , self.window2option_actual_rec , *self.recdevices ,command=self.actual_rec).pack()
        virtualframe.pack(anchor=CENTER)
        actualframe.pack(anchor=CENTER)
    def playback(self,text):
        registry_writer.write(r"SOFTWARE\\virtual audio player\\playback device",text)
        registry_writer.write(r"SOFTWARE\\virtual audio player\\playback device id",str(self.playbackdevices[text]))
        global playback_device,playback_device_id,actualmiclisten
        playback_device=text
        playback_device_id=self.playbackdevices[text]
    def rec_device(self,text):
        registry_writer.write(r"SOFTWARE\\virtual audio player\\rec device",text)
        registry_writer.write(r"SOFTWARE\\virtual audio player\\rec device id",str(self.recdevices[text]))
        global rec_device,rec_device_id,selflisten
        rec_device=text
        rec_device_id=self.recdevices[text]
        selflisten.running=False
        selflisten=self_listner.listen(rec_device_id,actual_playback_device_id)
        selflisten.start()
    def actual_playback(self,text):
        registry_writer.write(r"SOFTWARE\\virtual audio player\\actual playback device",text)
        registry_writer.write(r"SOFTWARE\\virtual audio player\\actual playback device id",str(self.playbackdevices[text]))
        global actual_playback_device,actual_playback_device_id,selflisten
        actual_playback_device=text
        actual_playback_device_id=self.playbackdevices[text]
        selflisten.running=False
        selflisten=self_listner.listen(rec_device_id,actual_playback_device_id)
        selflisten.start()
    def actual_rec(self,text):
        registry_writer.write(r"SOFTWARE\\virtual audio player\\actual rec device",text)
        registry_writer.write(r"SOFTWARE\\virtual audio player\\actual rec device id",str(self.recdevices[text]))
        global actual_rec_device,actual_rec_device_id,actualmiclisten
        actual_rec_device=text
        actual_rec_device_id=self.recdevices[text]
    def callback(self,sv):
        self.myprint(sv.get())
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
        i=1
        for dir in self.mydirs:
            if functionkeys["f"+str(i)]!=dir:
                self.folderasign()
                break
            i+=1
        i=1
        for key in functionkeys.values():
            if key not in self.mydirs:
                functionkeys["f"+str(i)]="None"
                registry_writer.write(r"SOFTWARE\\virtual audio player\\f"+str(i),"None")
            i+=1
    def toggle_button(self,root):
        self.toggle_button_instance=Button(root ,text=self.toggle_btn_text.get(), height=2,width=10,bd = '5',command=self.set_toggle_button)
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
        self.newFrame=Frame(self.Instance_root)
        self.newFrame.pack(anchor=CENTER)
        self.buttons=[]
        i=0
        j=3
        buttons.clear()
        for file in self.myfiles:
            if file[-3:]=="mp3" or file[-3:]=="wav" or file[-3:]=="ogg":
                self.buttons.append(Button(self.newFrame ,text = self.mytrim(file[:-4]), height=6,width=12,bd = '5',command=lambda c=file: self.play(args+"\\"+c)).grid(row=j,column=i))
                buttons.append(args+"\\"+file)
                if i<2:
                    i+=1
                else:
                    i=0
                    j-=1
                if j<=0:
                    break
        self.mylist()

    def run(self):
        pass

    def play(self,dir_name):
        global playerthread
        if pushtotalkpressed==False:
            if playerthread.is_alive():
                playerthread.stop()
            if playervar=="pygame":
                playerthread=player.player(dir_name,playback_device,pushtotalkkey,pushtotalk)
            else:
                playerthread=player.player(dir_name,9,pushtotalkkey,pushtotalk)
            playerthread.start()

class mylistner(threading.Thread):

    def __init__(self):
        super().__init__()

    def on_press(self,key):
        global playerthread,actualmiclisten
        if playerthread.is_alive()==False:
            if actualmiclisten.is_alive()==False:
                if hasattr(key,'char'):
                    if key.char==pushtotalkkey[0]:
                        selflisten.running=False
                        actualmiclisten=actual_mic_listner.listen(actual_rec_device_id,playback_device_id)
                        actualmiclisten.start()
                        global pushtotalkpressed
                        pushtotalkpressed=True
        if hasattr(key, 'vk') and 96 <= key.vk <= 105:
            if key.vk-97<len(buttons) and key.vk-97!=-1:
                if pushtotalkpressed==False:
                    if playerthread.is_alive():
                        playerthread.stop()
                    if playervar=="pygame":
                        playerthread=player.player(buttons[key.vk-97],playback_device,pushtotalkkey,pushtotalk)
                    else:
                        playerthread=player.player(buttons[key.vk-97],int(playback_device_id),pushtotalkkey,pushtotalk)
                    playerthread.start()
            if key.vk-96==0:
                playerthread.stop()
        if type(key)==Key:
            if key==key.f1:
                if functionkeys["f1"]!="None":
                    foldername.set(functionkeys["f1"])
            elif key==key.f2:
                if functionkeys["f2"]!="None":
                    foldername.set(functionkeys["f2"])
            elif key==key.f3:
                if functionkeys["f3"]!="None":
                    foldername.set(functionkeys["f3"])
            elif key==key.f4:
                if functionkeys["f4"]!="None":
                    foldername.set(functionkeys["f4"])
            elif key==key.f5:
                if functionkeys["f5"]!="None":
                    foldername.set(functionkeys["f5"])
            elif key==key.f6:
                if functionkeys["f6"]!="None":
                    foldername.set(functionkeys["f6"])
            elif key==key.f7:
                if functionkeys["f7"]!="None":
                    foldername.set(functionkeys["f7"])
            elif key==key.f8:
                if functionkeys["f8"]!="None":
                    foldername.set(functionkeys["f8"])
            elif key==key.f9:
                if functionkeys["f9"]!="None":
                    foldername.set(functionkeys["f9"])
            elif key==key.f10:
                if functionkeys["f10"]!="None":
                    foldername.set(functionkeys["f10"])
            elif key==key.f11:
                if functionkeys["f11"]!="None":
                    foldername.set(functionkeys["f11"])
            elif key==key.f12:
                if functionkeys["f12"]!="None":
                    foldername.set(functionkeys["f12"])
        #     if key==key.num_lock:
        #         os._exit(0)
    def on_release(self,key):
        global selflisten,actualmiclisten,pushtotalkpressed
        if playerthread.is_alive()==False:
            if hasattr(key,'char'):
                if key.char==pushtotalkkey[0]:
                    while pushtotalkpressed==True:
                        if selflisten.is_alive()==False:
                            if actualmiclisten.is_alive():
                                actualmiclisten.running=False
                                selflisten=self_listner.listen(rec_device_id,actual_playback_device_id)
                                selflisten.start()
                                pushtotalkpressed=False
    def run(self):
        with Listener(on_press=self.on_press,on_release=self.on_release) as listener:
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