import threading
import os
import listner
from tkinter.constants import *
from tkinter import *
import tkinter.messagebox
import sounddevice
import registry_writer
import list_of_devices
from time import *
from pynput.keyboard import Key, Listener
import mysystray
import win32gui
import win32con
import player
from PIL import ImageTk, Image
buttons = []
foldername = None
pushtotalkpressed = False
playervar = "pyaudio"
functionkeys = {}
firstplay = int(time()*1000.0)
secondplay = int(time()*1000.0)
rootwindow = None
for i in range(12):
    functionkeys["f"+str(i+1)] = "None"
if registry_writer.reg_check(r"SOFTWARE\\virtual audio player"):
    registry_writer.read(r"SOFTWARE\\virtual audio player\\player")
    firstrun = False
    actual_playback_device = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\actual playback device")
    actual_playback_device_id = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\actual playback device id")
    actual_rec_device = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\actual rec device")
    actual_rec_device_id = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\actual rec device id")
    playback_device = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\playback device")
    playback_device_id = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\playback device id")
    rec_device_id = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\rec device id")
    rec_device = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\rec device")
    pushtotalkkey = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\push to talk key")
    useovarlay = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\overlay")
    systrayvar = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\use systray")
else:
    registry_writer.create(r"SOFTWARE\\virtual audio player\\player")
    firstrun = True
    registry_writer.write(
        r"SOFTWARE\\virtual audio player\\player", "pyaudio")
    registry_writer.write(
        r"SOFTWARE\\virtual audio player\\actual playback device id", "0")
    registry_writer.write(
        r"SOFTWARE\\virtual audio player\\actual playback device", "None")
    registry_writer.write(
        r"SOFTWARE\\virtual audio player\\playback device", "none")
    registry_writer.write(
        r"SOFTWARE\\virtual audio player\\playback device id", "0")
    registry_writer.write(
        r"SOFTWARE\\virtual audio player\\actual rec device id", "0")
    registry_writer.write(
        r"SOFTWARE\\virtual audio player\\actual rec device", "None")
    registry_writer.write(
        r"SOFTWARE\\virtual audio player\\rec device", "none")
    registry_writer.write(
        r"SOFTWARE\\virtual audio player\\rec device id", "0")
    registry_writer.write(
        r"SOFTWARE\\virtual audio player\\push to talk key", "None")
    registry_writer.write(
        r"SOFTWARE\\virtual audio player\\overlay", "False")
    registry_writer.write(
        r"SOFTWARE\\virtual audio player\\use systray", "False")
    actual_playback_device = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\actual playback device")
    actual_playback_device_id = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\actual playback device id")
    actual_rec_device = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\actual rec device")
    actual_rec_device_id = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\actual rec device id")
    playback_device_id = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\playback device id")
    playback_device = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\playback device")
    rec_device = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\rec device")
    rec_device_id = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\rec device id")
    pushtotalkkey = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\push to talk key")
    useovarlay = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\overlay")
    systrayvar = registry_writer.read(
        r"SOFTWARE\\virtual audio player\\use systray")
playervar = registry_writer.read(r"SOFTWARE\\virtual audio player\\player")
if playervar == "pygame":
    playerthread = player.player_pygame("none", "none")
else:
    playerthread = player.player_pyaudio("none", 20)
if len(pushtotalkkey) > 1 or len(pushtotalkkey) < 1:
    pushtotalk = False
else:
    pushtotalk = True
selflisten = listner.listen(rec_device_id, actual_playback_device_id)
actualmiclisten = listner.listen(actual_rec_device_id, playback_device_id)


class gui(threading.Thread):
    def __init__(self):
        super().__init__()
        self.mainwindow = Tk()
        global rootwindow
        rootwindow = self.mainwindow
        self.mainwindow.geometry("0x0")
        self.mainwindow.overrideredirect(1)
        try:
            p1 = PhotoImage(file='requirements\\play.png')
        except:
            tkinter.messagebox.showinfo(
                "Error",
                "Requirements folder not found")
            os._exit(0)
        self.mainwindow.iconphoto(False, p1)
        self.mainwindow.iconbitmap(default='requirements\\play.ico')
        self.windowvar = StringVar()
        self.windowvar.trace("w", lambda name, index, mode,
                             sv=self.windowvar: self.main(sv.get()))
        self.playbackdevices = {}
        self.recdevices = {}
        self.options = []
        self.mydirs = []
        self.buttons = []
        try:
            image = Image.open("requirements\\button.png")
            image = image.resize((100, 100), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(image)
        except:
            self.photo=None
        self.overlayframe = Frame()
        self.window2option_playback = StringVar()
        self.window2option_playback.set(playback_device)
        self.window2option_rec = StringVar()
        self.window2option_rec.set(rec_device)
        self.window2option_actual_playback = StringVar()
        self.window2option_actual_playback.set(actual_playback_device)
        self.window2option_actual_rec = StringVar()
        self.window2option_actual_rec.set(actual_rec_device)
        self.pushtotalktext = StringVar()
        self.pushtotalktext.set(pushtotalkkey)
        self.pushtotalktext.trace(
            "w", lambda name, index, mode, sv=self.pushtotalktext: self.pushtotalkkeychange(sv))
        for root, dirs, files in os.walk(".", topdown=False):
            self.mydirs = dirs
        self.dircheck()
        for dir in self.mydirs:
            self.options.append(dir)
        if firstrun:
            self.folderasign()
            tkinter.messagebox.showinfo(
                "Notice",  "Please Configure it via settings under the menu button")
        global foldername
        foldername = StringVar()
        foldername.set(self.options[0])
        foldername.trace("w", lambda name, index, mode,
                         sv=foldername: self.callback(sv))
        self.toggle_btn_text = StringVar()
        self.toggle_btn_text.set(playervar)
        self.myfiles = []
        self.dir = []
        self.overlayvar = BooleanVar()
        lockcursorkey = StringVar()
        self.rootsystrayvar = BooleanVar()
        self.rootsystrayvar.set(systrayvar)
        selflisten.start()
        self.systraythread = mysystray.mytray(self.windowvar, self.overlayvar)
        self.overlayvar.trace("w", lambda name, index,
                              mode, sv=self.overlayvar: self.myoverlay(sv))
        lockcursorkey.trace("w", lambda name, index, mode,
                            sv=lockcursorkey: self.lockcursorvar(sv))
        self.overlayvar.set(useovarlay)
        if self.rootsystrayvar.get() == True:
            self.mysystemtray()
        self.windowvar.set("main")
        self.mainwindow.mainloop()

    def main(self, check):
        if check == "main":
            try:
                if self.Instance_root.state() == "normal":
                    self.Instance_root.focus()
            except Exception as e:
                self.Instance_root = Toplevel(self.mainwindow)
                self.Instance_root.geometry("1280x720")
                self.Instance_root.title("")
                self.Instance_root.protocol(
                    "WM_DELETE_WINDOW", self.close_window)
                self.Instance_root.minsize(768, 480)
                self.newFrame = Frame(self.Instance_root)
                self.newFrame.pack()
                self.drop = OptionMenu(
                    self.Instance_root, foldername, *self.options)
                self.drop.pack(anchor=NW)
                self.myprint([foldername.get()])
                self.mymenu()
                self.Instance_root.focus()
        elif check == "settings":
            self.settings()
        else:
            try:
                self.newWindow.destroy()
            except:
                pass
            self.Instance_root.destroy()

    def mymenu(self):
        self.mymenubar = Menu(self.Instance_root)
        self.mymenuoptions = Menu(self.mymenubar)
        self.mymenubar.add_cascade(label="menu", menu=self.mymenuoptions)
        self.mymenuoptions.add_command(label="settings", command=self.settings)
        self.Instance_root.config(menu=self.mymenubar)

    def folderasign(self):
        global functionkeys
        i = 1
        for dir in self.mydirs:
            if i <= 12 and functionkeys["f"+str(i)] == "None":
                functionkeys["f"+str(i)] = dir
            i += 1

    def pushtotalkkeychange(self, textvar):
        global pushtotalkkey, pushtotalk
        registry_writer.write(
            r"SOFTWARE\\virtual audio player\\push to talk key", str(textvar.get()).lower())
        pushtotalkkey = str(textvar.get()).lower()
        self.pushtotalktext.set(str(textvar.get()).lower())
        if len(pushtotalkkey) > 1 or len(pushtotalkkey) < 1:
            pushtotalk = False
        else:
            pushtotalk = True

    def settings(self):
        try:
            if self.newWindow.state() == "normal":
                self.newWindow.focus()
        except:
            self.newWindow = Toplevel(self.mainwindow)
            self.newWindow.title("Settings")
            self.newWindow.minsize(400, 400)
            self.newWindow.geometry("400x400")
            Checkbutton(self.newWindow, text="Use Overlay ?",
                        variable=self.overlayvar, onvalue=True, offvalue=False).pack()
            self.systraycheckbox = Checkbutton(self.newWindow, text="On Exit Minimize to System tray ?",
                                               variable=self.rootsystrayvar, onvalue=True, offvalue=False, command=self.mysystemtray).pack()
            self.toggle_button(self.newWindow)
            self.devices()

    def myoverlay(self, status):
        registry_writer.write(
            r"SOFTWARE\\virtual audio player\\overlay", str(status.get()))
        if status.get() == True:
            self.mycreateoverlay()
        else:
            self.destroyoverlay()

    def mysystemtray(self):
        registry_writer.write(
            r"SOFTWARE\\virtual audio player\\use systray", str(self.rootsystrayvar.get()))
        if self.rootsystrayvar.get() == True:
            if self.systraythread.is_alive() == False:
                self.systraythread = mysystray.mytray(
                    self.windowvar, self.overlayvar)
                self.systraythread.start()
        else:
            self.systraythread.stop()
            while self.systraythread.is_alive():
                sleep(0.1)
                self.systraythread.stop()
            self.main("main")

    def mycreateoverlay(self):
        try:
            if self.overlaywindow.state() == "normal":
                self.overlaywindow.focus()
        except:
            self.overlaywindow = Toplevel(self.mainwindow)
            self.overlaywindow.attributes("-fullscreen", True)
            self.overlaywindow.attributes("-transparentcolor", "red")
            self.overlaywindow.update_idletasks()
            self.overlaywindow.lift()
            self.overlayframe = Frame(
                self.overlaywindow,
                bg="red",
                borderwidth=10,
                highlightthickness=0)

            self.overlayframe.pack(
                anchor=CENTER,
                ipady=self.mainwindow.winfo_screenheight(),
                ipadx=self.mainwindow.winfo_screenwidth())
            l = Label(self.overlayframe, textvariable=foldername)
            l.pack(anchor=NW)
            hwnd = l.winfo_id()
            lExStyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            lExStyle |= win32con.WS_EX_LAYERED
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, lExStyle)
            win32gui.SetLayeredWindowAttributes(
                hwnd, 0, 255, win32con.LWA_ALPHA)
            self.mylist()
            self.overlaywindow.wm_attributes("-topmost", True)
            self.overlaywindow.overrideredirect(1)

    def mylist(self):
        try:
            self.l1.destroy()
        except:
            pass
        self.l1 = Listbox(self.overlayframe, width=10, height=9)
        hwnd = self.l1.winfo_id()
        lExStyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        lExStyle |= win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, lExStyle)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
        b = []
        for i in buttons:
            temp = i[:-4]
            if foldername.get() in temp:
                temp = temp.replace(foldername.get(), "")
                temp = temp.replace("\\", "")
            b.append(temp)
        self.l1.insert(1, *b)
        self.l1.configure(state=DISABLED)
        self.l1.pack(anchor=E)

    def destroyoverlay(self):
        try:
            self.overlaywindow.destroy()
        except:
            pass

    def devices(self):
        n = sounddevice.query_devices()
        j = 0
        for i in n:
            if i['max_input_channels'] <= 0:
                if i['hostapi'] == 0:
                    if not bool(self.playbackdevices):
                        self.playbackdevices[i['name']] = j
                    else:
                        if self.playbackdevices.get(i['name']) == None:
                            for d in list_of_devices.playbackdevices():
                                if i['name'] in d:
                                    self.playbackdevices[d] = j
            else:
                if i['hostapi'] == 0:
                    if not bool(self.recdevices):
                        self.recdevices[i['name']] = j
                    else:
                        if self.recdevices.get(i['name']) == None:
                            for d in list_of_devices.recdevices():
                                if i['name'] in d:
                                    self.recdevices[d] = j
            j += 1
        virtualframe = Frame(self.newWindow)
        actualframe = Frame(self.newWindow)
        Label(virtualframe, text="Virtual driver").pack()
        Label(actualframe, text="Physical driver").pack()
        text = Entry(self.newWindow, textvariable=self.pushtotalktext)
        text.pack()
        OptionMenu(virtualframe, self.window2option_playback, *
                   self.playbackdevices, command=self.playback).pack()
        OptionMenu(virtualframe, self.window2option_rec, *
                   self.recdevices, command=self.rec_device).pack()
        OptionMenu(actualframe, self.window2option_actual_playback,
                   *self.playbackdevices, command=self.actual_playback).pack()
        OptionMenu(actualframe, self.window2option_actual_rec, *
                   self.recdevices, command=self.actual_rec).pack()
        virtualframe.pack(anchor=CENTER)
        actualframe.pack(anchor=CENTER)

    def playback(self, text):
        registry_writer.write(
            r"SOFTWARE\\virtual audio player\\playback device", text)
        registry_writer.write(r"SOFTWARE\\virtual audio player\\playback device id", str(
            self.playbackdevices[text]))
        global playback_device, playback_device_id, actualmiclisten
        playback_device = text
        playback_device_id = self.playbackdevices[text]

    def rec_device(self, text):
        registry_writer.write(
            r"SOFTWARE\\virtual audio player\\rec device", text)
        registry_writer.write(
            r"SOFTWARE\\virtual audio player\\rec device id", str(self.recdevices[text]))
        global rec_device, rec_device_id, selflisten
        rec_device = text
        rec_device_id = self.recdevices[text]
        selflisten.running = False
        selflisten = listner.listen(rec_device_id, actual_playback_device_id)
        selflisten.start()

    def actual_playback(self, text):
        registry_writer.write(
            r"SOFTWARE\\virtual audio player\\actual playback device", text)
        registry_writer.write(r"SOFTWARE\\virtual audio player\\actual playback device id", str(
            self.playbackdevices[text]))
        global actual_playback_device, actual_playback_device_id, selflisten
        actual_playback_device = text
        actual_playback_device_id = self.playbackdevices[text]
        selflisten.running = False
        selflisten = listner.listen(rec_device_id, actual_playback_device_id)
        selflisten.start()

    def actual_rec(self, text):
        registry_writer.write(
            r"SOFTWARE\\virtual audio player\\actual rec device", text)
        registry_writer.write(
            r"SOFTWARE\\virtual audio player\\actual rec device id", str(self.recdevices[text]))
        global actual_rec_device, actual_rec_device_id, actualmiclisten
        actual_rec_device = text
        actual_rec_device_id = self.recdevices[text]

    def callback(self, sv):
        self.myprint(sv.get())

    def dircheck(self):
        for testdir in self.mydirs:
            if testdir == "temp":
                self.mydirs.remove("temp")
                self.dircheck()
            else:
                i = 0
                for root, testdirs, files in os.walk(testdir, topdown=False):
                    for file in files:
                        if file[-3:] == "mp3" or file[-3:] == "wav" or file[-3:] == "ogg":
                            i += 1
                if i <= 0:
                    self.mydirs.remove(testdir)
                    self.dircheck()
                    break
        i = 1
        for dir in self.mydirs:
            if functionkeys["f"+str(i)] != dir:
                self.folderasign()
                break
            i += 1
        i = 1
        for key in functionkeys.values():
            if key not in self.mydirs:
                functionkeys["f"+str(i)] = "None"
            i += 1

    def toggle_button(self, root):
        self.toggle_button_instance = Button(root, text=self.toggle_btn_text.get(
        ), height=2, width=10, bd='5', command=self.set_toggle_button)
        self.toggle_button_instance.pack()

    def set_toggle_button(self):
        global playervar
        if self.toggle_btn_text.get() == "pyaudio":
            self.toggle_btn_text.set("pygame")
            self.toggle_button_instance.configure(
                text=self.toggle_btn_text.get())
            registry_writer.write(
                r"SOFTWARE\\virtual audio player\\player", "pygame")
            playervar = "pygame"
        else:
            self.toggle_btn_text.set("pyaudio")
            self.toggle_button_instance.configure(
                text=self.toggle_btn_text.get())
            registry_writer.write(
                r"SOFTWARE\\virtual audio player\\player", "pyaudio")
            playervar = "pyaudio"

    def close_window(self):
        if self.rootsystrayvar.get() == False:
            os._exit(0)
        else:
            self.windowvar.set("destroy")

    def mytrim(self, filename):
        filename = filename.replace("-", " ")
        filename = filename.replace("_", " ")
        temp = filename.split()
        return_string = ""
        substractor = 12
        if len(filename) > 12:
            for word in temp:
                if len(return_string+" "+word) < substractor:
                    return_string = return_string+" "+word
                elif len(return_string+" "+word) >= substractor:
                    return_string = return_string+"\n"+word
                    substractor += 12
        else:
            return_string = filename
        return return_string

    def myprint(self, args):
        if type(args) == list:
            args = args[0]
        self.currentdir = args
        for root, dirs, files in os.walk(args, topdown=False):
            self.myfiles = files
        try:
            self.newFrame.destroy()
        except:
            pass
        self.newFrame = Frame(self.Instance_root)
        self.newFrame.pack(anchor=CENTER)
        self.buttons = []
        i = 0
        j = 3
        buttons.clear()
        for file in self.myfiles:
            if file[-3:] == "mp3" or file[-3:] == "wav" or file[-3:] == "ogg":
                try:
                        Button(
                            self.newFrame,
                            text=self.mytrim(file[:-4]),
                            height=6 if self.photo==None else 100, width=12 if self.photo==None else 100,
                            bd='5',
                            image=self.photo,
                            command=lambda c=file: self.play(args+"\\"+c)).grid(row=j, column=i)

                except Exception as e:
                    print(e)
                    pass
                buttons.append(args+"\\"+file)
                if i < 2:
                    i += 1
                else:
                    i = 0
                    j -= 1
                if j <= 0:
                    break
        self.mylist()

    def run(self):
        pass

    def play(self, dir_name):
        global playerthread, secondplay, firstplay
        secondplay = int(time()*1000.0)
        if secondplay-firstplay >= 100:
            firstplay = secondplay
            if pushtotalkpressed == False:
                if playerthread.is_alive():
                    playerthread.stop()
                if playervar == "pygame":
                    playerthread = player.player_pygame(
                        dir_name, playback_device, pushtotalkkey, pushtotalk)
                else:
                    playerthread = player.player_pyaudio(dir_name, int(
                        playback_device_id), pushtotalkkey, pushtotalk)
                playerthread.start()


class mylistner(threading.Thread):
    def __init__(self):
        super().__init__()
        self.locked = False

    def on_press(self, key):
        global playerthread, actualmiclisten
        if playerthread.is_alive() == False:
            if actualmiclisten.is_alive() == False:
                if hasattr(key, 'char'):
                    if key.char == pushtotalkkey[0]:
                        playerthread.stop()
                        selflisten.running = False
                        actualmiclisten = listner.listen(
                            actual_rec_device_id, playback_device_id)
                        actualmiclisten.start()
                        global pushtotalkpressed
                        pushtotalkpressed = True
        if hasattr(key, 'vk') and 96 <= key.vk <= 105:
            global firstplay, secondplay
            if key.vk-97 < len(buttons) and key.vk-97 != -1:
                secondplay = int(time()*1000.0)
                if secondplay-firstplay >= 100:
                    firstplay = secondplay
                    if pushtotalkpressed == False:
                        if playerthread.is_alive():
                            playerthread.stop()
                        if playervar == "pygame":
                            playerthread = player.player_pygame(
                                buttons[key.vk-97], playback_device, pushtotalkkey, pushtotalk)
                        else:
                            playerthread = player.player_pyaudio(
                                buttons[key.vk-97], int(playback_device_id), pushtotalkkey, pushtotalk)
                        playerthread.start()
            if key.vk-96 == 0:
                playerthread.stop()
        if type(key) == Key:
            if key == key.f1:
                if functionkeys["f1"] != "None":
                    foldername.set(functionkeys["f1"])
            elif key == key.f2:
                if functionkeys["f2"] != "None":
                    foldername.set(functionkeys["f2"])
            elif key == key.f3:
                if functionkeys["f3"] != "None":
                    foldername.set(functionkeys["f3"])
            elif key == key.f4:
                if functionkeys["f4"] != "None":
                    foldername.set(functionkeys["f4"])
            elif key == key.f5:
                if functionkeys["f5"] != "None":
                    foldername.set(functionkeys["f5"])
            elif key == key.f6:
                if functionkeys["f6"] != "None":
                    foldername.set(functionkeys["f6"])
            elif key == key.f7:
                if functionkeys["f7"] != "None":
                    foldername.set(functionkeys["f7"])
            elif key == key.f8:
                if functionkeys["f8"] != "None":
                    foldername.set(functionkeys["f8"])
            elif key == key.f9:
                if functionkeys["f9"] != "None":
                    foldername.set(functionkeys["f9"])
            elif key == key.f10:
                if functionkeys["f10"] != "None":
                    foldername.set(functionkeys["f10"])
            elif key == key.f11:
                if functionkeys["f11"] != "None":
                    foldername.set(functionkeys["f11"])
            elif key == key.f12:
                if functionkeys["f12"] != "None":
                    foldername.set(functionkeys["f12"])

    def on_release(self, key):
        global selflisten, actualmiclisten, pushtotalkpressed
        if playerthread.is_alive() == False:
            if hasattr(key, 'char'):
                if key.char == pushtotalkkey[0]:
                    while pushtotalkpressed == True:
                        if selflisten.is_alive() == False:
                            if actualmiclisten.is_alive():
                                actualmiclisten.running = False
                                while actualmiclisten.is_alive():
                                    sleep(0.01)
                                selflisten = listner.listen(
                                    rec_device_id, actual_playback_device_id)
                                selflisten.start()
                                pushtotalkpressed = False

    def run(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


#


class main(threading.Thread):

    def __init__(self):
        super().__init__()
        self.mylistner1 = mylistner()
        self.mylistner1.start()
        # self.server = myserver()

    def run(self):
        # if self.server.is_alive() == False:
        #     self.server.start()
        if self.mylistner1.is_alive() == False:
            self.mylistner1 = mylistner()
            self.mylistner1.start()
        sleep(1)
        self.run()


mainthread = main()
mainthread.start()
threadgui = gui()
threadgui.start()
# class myserver(threading.Thread):
#     def __init__(self):
#         super().__init__()
#         self.s = socket.socket()
#         self.s.bind(('0.0.0.0', 8090))
#         self.s.listen(0)
#         self.content = ""
#         print("Listening")

#     def run(self):
#         while True:
#             client, addr = self.s.accept()
#             data = json.dumps(buttons)
#             threading.Thread(target=self.client, args=(
#                 client, addr, data, )).start()

#     def client(self, client: socket.socket, addr: tuple, message):
#         print("Connected to")
#         print(*addr, sep="")
#         recv_t = threading.Thread(target=self.client_recv, args=(client, ))
#         recv_t.start()
#         while True:
#             if self.content!=b'':
#                 print(self.content)
#                 send_t = threading.Thread(target=self.client_send, args=(client,buttons, ))
#                 send_t.start()
#                 self.content=b''
#             if recv_t.is_alive()==False:
#                 break
#         s = ""
#         for i in addr:
#             s += str(i)
#         print("Closing connection to "+s)
#         client.close()

#     def client_send(self, client, message):
#         if type(message)==list:
#             for i in message:
#                 t=i.split("\\")
#                 t.reverse()
#                 client.sendall(bytes(t[0], encoding="utf-8"))
#                 sleep(0.1)

#     def client_recv(self, client):
#         while True:
#             try:
#                 self.content = client.recv(32)
#             except ConnectionResetError:
#                 break
