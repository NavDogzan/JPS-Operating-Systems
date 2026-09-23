import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import datetime as datetime_module
from PIL import Image, ImageDraw, ImageTk
import pygame 
import time 
import random
import os
import pickle
import sys

dt = datetime_module.datetime.now().strftime("%H:%M")
print(dt)
pygame.mixer.init()
pysound = pygame.mixer
now = datetime_module.datetime.now()

number_date = now.strftime("%d/%m/%Y")
words_date = now.strftime("%A, %B %d")
print(words_date)

def clear_console():  
    if os.name == 'nt':
        _ = os.system('cls')

def slowprint(a, delay=0.01):
    for word in a:
        print(word, end='', flush=True)
        time.sleep(delay)
def rollnumber(xRand, yRand):
    xRand = random.randint(50,200)
    yRand = random.randint(50,200)
    return xRand, yRand
def Consolestartup():
    Startup = '''







        
                                                ██╗██████╗ ███████╗
                                                ██║██╔══██╗██╔════╝
                                                ██║██████╔╝███████╗
                                           ██   ██║██╔═══╝ ╚════██║
                                           ╚█████╔╝██║     ███████║
                                            ╚════╝ ╚═╝     ╚══════╝
                                                           Operating System 2025
        '''
    slowprint(Startup,delay=0.001)
    time.sleep(3)
    print('''
                                        Starting please wait....''')
    loader = '''                                        ████████████████████████>'''
    time.sleep(2)
    slowprint(loader, delay=0.09)
    clear_console()
    
    desktopFunc()

class MyDragManager: #Source: Youtube
    def __init__(self):  
        self.widget = None
        self.root = None
        self.offset_x = 0 
        self.offset_y = 0

    def add_draggable_widget(self, widget):
        self.widget = widget
        self.root = widget.winfo_toplevel()
        self.widget.bind("<Button-1>", self.on_start) 
        self.widget.bind("<B1-Motion>", self.on_drag)     
        self.widget.bind("<ButtonRelease>", self.on_drop)  
        self.widget.configure(cursor="hand1")

    def on_start(self, event):   
        self.offset_x = event.x
        self.offset_y = event.y

    def on_drag(self, event):
       
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        self.widget.place(x=x - self.offset_x, y=y - self.offset_y)
        return True

    def on_drop(self, event):
     
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        self.widget.place(x=x - self.offset_x, y=y - self.offset_y)

taskbar_buttons = {}
open_app_frames = {}


def liftclickedapp(event):
    widget = event.widget
    while widget is not None:
        for app_frame in open_app_frames.values():
            if widget == app_frame:
                app_frame.lift()
                return
        widget = widget.master

def set_desktop_wallpaper(image_path=None):
    global Wallp
    if Wallp is not None and Wallp.winfo_exists():
        Wallp.destroy()
    MotherFrame.configure(bg="white")
    if image_path is None:
        Taskbar.lift()
        return

    imaged = Image.open(image_path)
    imaged = imaged.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
    photo = ImageTk.PhotoImage(master=root,  image=imaged)
    Wallp = tk.Label(MotherFrame, image=photo, borderwidth=0)
    Wallp.image = photo
    Wallp.place(x=0, y=0, relwidth=1, relheight=1)
    Wallp.lower()
    Taskbar.lift()

def closed(b, app_id=None):
    b.place_forget()
    if app_id in open_app_frames:
        del open_app_frames[app_id]
    if app_id and app_id in taskbar_buttons:
        taskbar_buttons[app_id].destroy()
        del taskbar_buttons[app_id]

def minimize(app_id, app_frame):
    app_frame.place_forget()
def restore_or_focus(app_id, app_frame):
    if app_frame.winfo_ismapped():
        app_frame.lift()
    else:
        app_frame.place(x=100, y=200) 
        app_frame.lift()
def create_taskbar_button(app_id, app_frame, display_name):
    open_app_frames[app_id] = app_frame
    app_frame.lift()
    if app_id not in taskbar_buttons:
        btn = tk.Button(Taskbar, text=display_name, width=10, 
                       command=lambda: restore_or_focus(app_id, app_frame), bg="Light blue")
        btn.pack(side="left", padx=3)
        taskbar_buttons[app_id] = btn
def startFunc(): #Source: StackOverflow
    global St_toggle
    if St_toggle:
        Start.place_forget()
        St_toggle = False
        root.unbind_all("<Button-1>")
    else:
 
       

        Start.place(x=0, y=root.winfo_height() - 40 - Start.winfo_reqheight())
        Start.lift()
        St_toggle = True
        root.bind_all("<Button-1>", check_click_outside, add="+")
def Shutdown():
    global Sd_toggle
    print("Shuttt")
    if Sd_toggle:
        ShutMenu.place_forget()
        Sd_toggle = False
        root.unbind("<Button-1>")
        return

    root.update_idletasks()

    if shut and shut.winfo_exists():
        menu_w = ShutMenu.winfo_reqwidth()
        menu_h = ShutMenu.winfo_reqheight()
        button_x = shut.winfo_rootx() - root.winfo_rootx() + shut.winfo_width() - 30
        button_y = shut.winfo_rooty() - root.winfo_rooty() - menu_h - 8
        if button_y < 0:
            button_y = 0
        ShutMenu.place(x=button_x, y=button_y)
    else:
        ShutMenu.place(x=720, y=root.winfo_height() - 40 - Calend.winfo_reqheight())

    ShutMenu.lift()
    Sd_toggle = True
    root.after(100, lambda: root.bind("<Button-1>", check_click_outside3))
'''def Calender():
    global cl_toggle
    print("hello")
    if cl_toggle:
        Calend.place_forget()
        cl_toggle = False
        root.unbind("<Button-1>")  
    else:
        Calend.place(x=670, y=root.winfo_height() - 40 - Calend.winfo_reqheight())
        Calend.lift()
        cl_toggle = True
        root.after(100, lambda: root.bind("<Button-1>", check_click_outside2))'''
def check_click_outside(event):#Source: StackOverflow
    global St_toggle
    clicked_widget = event.widget
    if clicked_widget == StartButton:
        return
    widget = clicked_widget
    while widget:
        if widget == Start:
            return 
        widget = widget.master
    if St_toggle:
        Start.place_forget()
        St_toggle = False
        root.unbind_all("<Button-1>")

def check_click_outside3(event):#Source: StackOverflow
    global Sd_toggle
    clicked_widget = event.widget
    if clicked_widget == shut:
        return
    widget = clicked_widget
    while widget:
        if widget == ShutMenu:
            return 
        widget = widget.master
    if Sd_toggle:
        ShutMenu.place_forget()
        Sd_toggle = False
        root.unbind("<Button-1>")

def Calculator():
    app_id = f"Calc_{random.randint(1000, 9999)}"
    xRand = 0
    yRand = 0
    xRand , yRand = rollnumber(xRand, yRand)
    CalcAppframe = tk.Frame(root, width=520, height=320, bg="#3f8099", borderwidth=3, relief=tk.RIDGE)
    CalcAppframe.place(x=xRand, y=yRand)
   
    CalcAppframe.pack_propagate(False)
    
    
    create_taskbar_button(app_id, CalcAppframe, "Calc")
    
    CalcAppBarUp = tk.Frame(CalcAppframe, height=220, bg="Light blue",borderwidth=1, relief=tk.RIDGE)
    CalcAppBarUp.pack(side="bottom", fill="x")

    CalcClosebtn = tk.Button(CalcAppframe,
                        text="X",
                        fg="Black", 
                        activebackground="red",
                        width=3, 
                        height=30,
                        command=lambda: closed(CalcAppframe, app_id))
    CalcClosebtn.pack(side="right", anchor="ne", padx=1, pady=1)

    NoteApp_label = tk.Label(CalcAppframe, text="Calculator", bg="#3f8099", font="Arial 10 bold")
    NoteApp_label.pack(side="left", padx=10)
   
    Calc = MyDragManager()
    Calc.add_draggable_widget(CalcAppframe)
    
    
    
    minimizebtn = tk.Button(CalcAppframe, text="_", width=3, height=30, 
                           command=lambda: minimize(app_id, CalcAppframe))  
    minimizebtn.pack(side="top", anchor="ne", padx=1, pady=1)
       
    Calc = MyDragManager()
    Calc.add_draggable_widget(CalcAppframe)
    #-----------------------------------------------------------------------Source: StackOverflow--------------------------------------------------------------------------#
    Expression = tk.StringVar()
    Entry = tk.Entry(CalcAppBarUp, textvar=Expression, width=30, font=('Arial', 14), bg="Light grey", fg="Black", justify='right') 
    Entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
    Entry.bind("<Return>", lambda:on_button_click('='))
    
    def on_button_click(value):
        if value == '=':
            try:
                result = eval(Expression.get())
                Expression.set(result)
            except:
                Expression.set('Error')
        elif value == 'C':
            Expression.set('')
        else:
            Expression.set(Expression.get() + value)
    
    buttons_layout = [
        ('7', '8', '9', '/'),
        ('4', '5', '6', '*'),
        ('1', '2', '3', '-'),
        ('0', '.', '=', '+'),
        ('C',)
    ]
    
    row_offset = 1
    for row_index, row in enumerate(buttons_layout):

        CalcAppBarUp.grid_rowconfigure(row_offset + row_index, weight=1)
        for col_index, button_text in enumerate(row):

            CalcAppBarUp.grid_columnconfigure(col_index, weight=1)
            btn = tk.Button(CalcAppBarUp, text=button_text, font=('Arial', 14),
                        command=lambda val=button_text: on_button_click(val), bg="White", fg="black", relief=tk.RAISED)
            btn.grid(row=row_offset + row_index, column=col_index, padx=5, pady=5, sticky='nsew')
    
     #----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def Settings():
    app_id = f"Settings_{random.randint(1000, 9999)}"
    
    SettingsAppFrame = tk.Frame(root, width=520, height=355, bg="#3f8099",borderwidth=1, relief=tk.RIDGE)
    xRand = 0
    yRand = 0
    xRand , yRand = rollnumber(xRand, yRand)
    SettingsAppFrame.place(x=xRand, y=yRand)
    SettingsAppFrame.propagate(False)

    create_taskbar_button(app_id, SettingsAppFrame, "Sttngs")

    SettingsAppBarUp = tk.Frame(SettingsAppFrame, height=320, bg="Light blue", highlightthickness=0, borderwidth=5, relief=tk.RIDGE)
    SettingsAppBarUp.propagate(False)
    SettingsAppBarUp.pack(side="bottom", fill="x")

    SettingsClosebtn = tk.Button(SettingsAppFrame,
                    text="X",
                    fg="Black", 
                    activebackground="red",
                    width=3, 
                    height=30,
                    command=lambda: closed(SettingsAppFrame, app_id))
    SettingsClosebtn.pack(side="right", anchor="ne", padx=1, pady=1)
    
    SettingsminiBtn = tk.Button(SettingsAppFrame,
                    text="_",
                    fg="Black", 
                    width=3, 
                    height=30,
                    command=lambda: minimize(app_id, SettingsAppFrame))  
    SettingsminiBtn.pack(side="right", anchor="ne", padx=1, pady=1)

    Stngs = MyDragManager()
    Stngs.add_draggable_widget(SettingsAppFrame)

    SettingsApp_label = tk.Label(SettingsAppFrame, text= "Settings", bg="#3f8099", font="Arial 10 bold")
    SettingsApp_label.place(x=5, y=5)


    def credits():
        global Settings_frame2
        Settings_frame1.destroy()
        Settings_frame2 = tk.Frame(SettingsAppBarUp, width=500, height=300, bg="Light blue")
        Settings_frame2.propagate(False)
        Settings_frame2.pack(side="left",padx=5, pady=10)
        credits_label = tk.Label(Settings_frame2, text="JPS Operating System\nVersion 2026\n\nDeveloped by: \n\nC.T.Pranav\nP.Sricharan\nT.Jaidev", font=("Arial", 14), bg="Light blue")
        credits_label.pack(pady=20)
        back_btn = tk.Button(Settings_frame2, text="Back", width=10, height=2, command=lambda: settingsapp())
        back_btn.pack(pady=10)

    def ChangeWallpaper():
        global Settings_frame2
        img1 = os.path.join(os.path.dirname(__file__), "ImageAssets", "DeathStrading1.png")
        img2 = os.path.join(os.path.dirname(__file__), "ImageAssets", "DeathStranding2.png")
        img3 = os.path.join(os.path.dirname(__file__), "ImageAssets", "HorizonZero1.png")
        img4 = os.path.join(os.path.dirname(__file__), "ImageAssets", "HorizonZero2.png")
        img5 = os.path.join(os.path.dirname(__file__), "ImageAssets", "ResidentEvil1.png")
        img6 = os.path.join(os.path.dirname(__file__), "ImageAssets", "Uncharted1.png")
        img7 = os.path.join(os.path.dirname(__file__), "ImageAssets", "Uncharted2.png")
        img8 = os.path.join(os.path.dirname(__file__), "ImageAssets", "Uncharted3.png")
        def ChangedWallp(img):
                set_desktop_wallpaper(img)


            

        


        Settings_frame1.destroy()
        Settings_frame2 = tk.Frame(SettingsAppBarUp, width=500, height=300, bg="Light blue")
        Settings_frame2.propagate(False)
        Label = tk.Label(Settings_frame2, text="Give your desktop some character", font=("Arial", 14, "underline"), bg="Light blue")
        
        Settings_frame2.pack(side="left",padx=5, pady=10,fill="both", expand=True)
        Label.pack(side = "top",pady=10)
        BackBtn = tk.Button(Settings_frame2, text="Back", width=15, height=1, font=("Arial", 10), command=lambda: settingsapp())
        BackBtn.pack(side="bottom", pady=5)
        button_frame = ctk.CTkScrollableFrame(Settings_frame2, width=460, height=100, fg_color="white")
        button_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        

        WallPList = ["DS1", "DS2", "HZ1", "UN1", "White", "RE1", "UN2", "UN3", "UN4"]
        WallpListBtn = []
        
        for j,button_N in enumerate(WallPList):
            btn = tk.Button(button_frame, text=button_N, height=2, font=("Arial", 18), borderwidth=5, relief=tk.RIDGE)

            btn.pack(side="top", padx=5, pady=5, fill="x")
            WallpListBtn.append(btn)

        WallpListBtn[4].config(command= lambda: set_desktop_wallpaper())
        WallpListBtn[0].config(command= lambda: ChangedWallp(img1))
        WallpListBtn[1].config(command= lambda: ChangedWallp(img2))
        WallpListBtn[2].config(command= lambda: ChangedWallp(img7))
        WallpListBtn[3].config(command= lambda: ChangedWallp(img8))
        WallpListBtn[5].config(command= lambda: ChangedWallp(img3))
        WallpListBtn[6].config(command= lambda: ChangedWallp(img4))
        WallpListBtn[7].config(command= lambda: ChangedWallp(img5))
        WallpListBtn[8].config(command= lambda: ChangedWallp(img6))
    def Security():
        def write(Entry):
            framelol.destroy()
            print(Entry)
            f1 = open("cred.dat","wb+")
            pickle.dump(Entry, f1)
            f1.close()
       
        def changed(Entry):
            f1 = open("cred.dat", "rb+")
            try:
                while True:
                    j = pickle.load(f1)
                    if j == Entry:
                        headerpass.configure(text="Enter new password")
                        entery.configure(command=lambda: write(Enter.get()))
                        f1.close()



                    else:
                        headerpass.configure(text="Wrong")
                        f1.close()
                    
            except:pass

        def askpass():
            global headerpass, Enter, entery, framelol
            framelol = tk.Frame(cpass, height=200,width=300, bg="Light blue", borderwidth=3,relief=tk.RIDGE)
            framelol.place(relx=0.5,rely=0.5,anchor="center")
            headerpass = tk.Label(framelol, text="Enter current password", font=("Arial",12,"underline"), bg="Light blue")
            headerpass.pack(side="top",padx=10,pady=10)
            Enter = tk.Entry(framelol, width=30, show="*")
            Enter.pack(side="top",padx=10,pady=10)
            farm = tk.Frame(framelol, height=100,bg="Light blue")
            farm.pack(side="top",padx=3,pady=3,fill="x")
            back = tk.Button(farm,text="<",command=lambda:framelol.destroy())
            entery = tk.Button(farm, text="Enter",height=1,width=5,command=lambda: changed(Enter.get()))
            
            entery.place(relx=0.5,rely=0.5,anchor="center")
            back.pack(side="left",padx=3,pady=3,anchor="w")
            
            

        def changepass():
            global cpass
            Settings_frame2.destroy()
            cpass = tk.Frame(SettingsAppBarUp, width=500, height=300, bg="Light blue")
            cpass.propagate(False)
            cpass.pack(side="left",padx=5, pady=10)
            Header = tk.Label(cpass, text="Change password",font=("Arial",15,"underline"),bg="Light blue")
            Header2 = tk.Label(cpass, text="Select User",font=("Arial",13,"underline"),anchor="w",bg="Light blue")
            Button1 = tk.Button(cpass, text="Pranav",font=("Arial",14),width=10,height=2, command=askpass)
            bac = tk.Button(cpass,text='<',command=Security)

            Header.pack(fill="x",side="top",padx=10,pady=10)
            Header2.pack(fill="x",side="top",padx=10,pady=10)
            Button1.pack(side="left",padx=10,pady=10,anchor="n")
            bac.pack(side="bottom")


        try:cpass.destroy()
        except:pass

        global Settings_frame2
        Settings_frame1.destroy()
        Settings_frame2 = tk.Frame(SettingsAppBarUp, width=500, height=300, bg="Light blue")
        Settings_frame2.propagate(False)
        Settings_frame2.pack(side="left",padx=5, pady=10)
        Header = tk.Label(Settings_frame2, text="Security",font=("Arial",15,"underline"),bg="Light blue")
        Button1 = tk.Button(Settings_frame2, text="Change password",command=changepass)
        bac = tk.Button(Settings_frame2, text="<",command=settingsapp)

        Header.pack(side="top",padx=10,pady=10)
        Button1.pack(side="top",padx=10,pady=5)
        bac.pack(side="bottom")

    def settingsapp():
        global Settings_frame1
        try:
            Settings_frame2.destroy()
        except:
            NameError
            print("WallPaperNotOpenedYet")
            
        Settings_frame1 = tk.Frame(SettingsAppBarUp, width=500, height=300, bg="Light blue")
        Settings_frame1.propagate(False)
        Settings_frame1.pack(side="left",fill="both", expand=True, padx=10, pady=10)
        SettingsListList = ["Wallpaper", "Security", "Credits"]
        SettingsListBtn = []
        header = tk.Label(Settings_frame1, text="Settings", font=("Arial", 14, "bold", "underline"), bg="Light blue")
        desc = tk.Label(Settings_frame1, text="Make changes to your system settings", font=("Arial", 10), bg="Light blue")

        header.pack(side="top", pady=10)
        desc.pack(side="top", pady=5)      
        optionsFrame = tk.Frame(Settings_frame1, bg="Light blue")
        optionsFrame.pack(side="top", pady=10)
        for j,button_N in enumerate(SettingsListList):
            btn = tk.Button(optionsFrame, text="♠", width=3, height=1, font=("Arial", 14), relief=tk.RIDGE)
            label = tk.Label(optionsFrame, text= button_N, width=7, height=1, font=("Arial", 10),bg="Light blue")
            label.grid(row=1, column=j, padx=20, pady=5)
            btn.grid(row=0, column=j, padx=20, pady=5)
            SettingsListBtn.append(btn)
        SettingsListBtn[0].config(command= lambda: ChangeWallpaper())
        SettingsListBtn[2].config(command= lambda: credits())
        SettingsListBtn[1].config(command= lambda: Security())

       
    settingsapp()

def mp3():

    app_id = f"mp3_{random.randint(1000, 9999)}"
    xRand = 0
    yRand = 0
    xRand , yRand = rollnumber(xRand, yRand)
    
    mp3_frame = tk.Frame(root, width=320, height=450, bg="#878a8b",borderwidth=1, relief=tk.RIDGE)
    mp3_frame.place(x=xRand, y=yRand)
    mp3_frame.pack_propagate(False)

    create_taskbar_button(app_id, mp3_frame, "JpsVinyl")
    frm = tk.Frame(mp3_frame, height=30, width=100)
    frm.pack(side="top",anchor="ne")

    mp3AppBarUp = tk.Frame(mp3_frame,width=350, height=450, bg="#3f3f3f", highlightthickness=0,borderwidth=3, relief=tk.RIDGE)
    mp3AppBarUp.propagate(False)
    mp3AppBarUp.pack(side="top", fill="x")

    def close_mp3():
        pysound.music.pause()
        closed(mp3_frame, app_id)



    mp3Closebtn = tk.Button(frm,
                    text="X",
                    fg="Black", 
                    activebackground="red",
                    width=3, 
                    height=1,
                    command=close_mp3)
    mp3Closebtn.pack(side="right", anchor="ne", padx=1, pady=1)
    
    mp3miniBtn = tk.Button(frm,
                    text="_",
                    fg="Black", 
                    width=3, 
                    height=1,
                    command=lambda: minimize(app_id, mp3_frame))  
    mp3miniBtn.pack(side="right", anchor="ne", padx=1, pady=1)
    Label = tk.Label(mp3_frame, text="Jps Vinyl", bg="#878a8b", font="Arial 10 bold")
    Label.place(x=5, y=5)

    drag = MyDragManager()
    drag.add_draggable_widget(mp3_frame)
    MusicTheme = "#3f3f3f"
    audio_dir = os.path.join(os.path.dirname(__file__), "AudioAssets")
    songpaths = [
        os.path.join(audio_dir, filename)
        for filename in sorted(os.listdir(audio_dir))
        if filename.lower().endswith(".mp3")
    ]
    song_metadata = {
        "here comes the sun": {"artist": "The Beatles", "theme": "#d8b45b"},
        "duvet": {"artist": "boa", "theme": "#78909c"},
        "bohemian rhapsody": {"artist": "Queen", "theme": "#9C4CA3"},
    }
    current_song_length = 0.0
    current_song_index = None

    def darker_color(color, factor=0.8):
        color = color.lstrip("#")
        red, green, blue = (
            int(color[index:index + 2], 16)
            for index in (0, 2, 4)
        )
        return "#{:02x}{:02x}{:02x}".format(
            int(red * factor),
            int(green * factor),
            int(blue * factor),
        )

    def app():
        
        global playlist_s, playing

        playlist_s = False
        playlistframe = None

        def playlist():
            global playlist_s
            if not playlist_s:
                if playlistframe is None or not playlistframe.winfo_exists():
                    build_playlist_frame()
                playlistframe.place(relx=0.5,y=200, anchor="center")
                playlistframe.lift()
                playlist_s = True
            else:
                if playlistframe is not None and playlistframe.winfo_exists():
                    playlistframe.place_forget()
                playlist_s = False

        plylist_button = tk.Button(mp3AppBarUp,height=1,text="My playlist", bg="#878a8b", command=playlist)
        plylist_button.pack(side="top",fill="x",padx=1,pady=1)
        VinlyFrame = tk.Frame(mp3AppBarUp, height=300, bg=MusicTheme, borderwidth=3, relief=tk.RIDGE)
        VinlyFrame.pack_propagate(False)
        VinlyFrame.pack(side="top", fill="x", padx=2, pady=1)




        Album = Image.new("RGB", (150, 150), "black")
        Album = Album.resize((150, 150), Image.LANCZOS)
        albumphoto = ImageTk.PhotoImage(master=root,  image=Album)






        vinyl_path = os.path.join(os.path.dirname(__file__), "ImageAssets", "Vinyl.png")
        vinyl_image = Image.open(vinyl_path).convert("RGBA")
        vinyl_image_frame = tk.Frame(VinlyFrame, width=140, height=140, bg=MusicTheme)
        vinyl_image_frame.pack_propagate(False)
        vinyl_image_frame.place(x=190, y=120, anchor="center")
        vinyl_image = vinyl_image.resize((140, 140), Image.LANCZOS)
        base_vinyl_image = vinyl_image.copy()
        vinyl_photo = ImageTk.PhotoImage(master=root,  image=vinyl_image)
        vinyl_label = tk.Label(vinyl_image_frame, image=vinyl_photo, bg=MusicTheme)
        vinyl_label.image = vinyl_photo
        vinyl_label.pack(fill="both", expand=True)

        Albumphotoframe = tk.Frame(VinlyFrame, height=155,width=155, borderwidth=5,relief=tk.RIDGE)
        Albumphotoframe.pack_propagate(False)
        Labl = tk.Label(Albumphotoframe,image=albumphoto,height=300,width=300)
        Labl.image = albumphoto
        Albumphotoframe.place(x=100, y=120, anchor="center")
        Labl.pack(fill="both", expand=True)

        def load_song(song_index):
            global playing, playlist_s
            nonlocal MusicTheme, vinyl_image, current_song_length, current_song_index
            current_song_index = song_index
            songpath = songpaths[song_index]
            song_name = os.path.splitext(os.path.basename(songpath))[0].casefold()
            metadata = song_metadata.get(
                song_name,
                {"artist": "Unknown artist", "theme": "#3f3f3f"},
            )
            pysound.music.load(songpath)
            current_song_length = pygame.mixer.Sound(songpath).get_length()
            pysound.music.play()

            albums_dir = os.path.join(os.path.dirname(__file__), "ImageAssets2", "Albums")
            cover_names = {
                "here comes the sun": "B1.png",
                "duvet": "Duvet.png",
                "bohemian rhapsody": "BR.png",
            }
            coverpath = next(
                (
                    os.path.join(albums_dir, filename)
                    for filename in os.listdir(albums_dir)
                    if os.path.splitext(filename)[0].casefold() == song_name
                    and os.path.splitext(filename)[1].lower() in (".png", ".jpg", ".jpeg")
                ),
                None,
            )
            if coverpath is None and song_name in cover_names:
                mapped_coverpath = os.path.join(albums_dir, cover_names[song_name])
                if os.path.exists(mapped_coverpath):
                    coverpath = mapped_coverpath
            if coverpath is not None:
                cover = Image.open(coverpath).resize((150, 150), Image.LANCZOS)
                selected_album_photo = ImageTk.PhotoImage(master=root,  image=cover)
                Labl.configure(image=selected_album_photo)
                Labl.image = selected_album_photo

                vinyl_image = base_vinyl_image.copy()
                vinyl_cover = cover.resize((45, 45), Image.LANCZOS).convert("RGBA")
                vinyl_cover_mask = Image.new("L", (45, 45), 0)
                ImageDraw.Draw(vinyl_cover_mask).ellipse((0, 0, 44, 44), fill=255)
                vinyl_cover.putalpha(vinyl_cover_mask)
                vinyl_image.alpha_composite(vinyl_cover, (47, 47))
            else:
                blank_album = Image.new("RGB", (150, 150), "black")
                blank_album_photo = ImageTk.PhotoImage(master=root,  image=blank_album)
                Labl.configure(image=blank_album_photo)
                Labl.image = blank_album_photo
                vinyl_image = base_vinyl_image.copy()

            MusicTheme = metadata["theme"]
            mp3AppBarUp.configure(bg=MusicTheme)
            VinlyFrame.configure(bg=MusicTheme)
            ControlFrame.configure(bg=MusicTheme)
            Framed.configure(fg_color=darker_color(MusicTheme))
            vinyl_image_frame.configure(bg=MusicTheme)
            vinyl_label.configure(bg=MusicTheme)
            time_remaining_label.configure(bg=MusicTheme)
            musiclabel.configure(text=os.path.splitext(os.path.basename(songpath))[0], bg=MusicTheme)
            artistlabel.configure(text=metadata["artist"], bg=MusicTheme)
            volumeslide.configure(bg=MusicTheme, troughcolor=metadata["theme"])
            time_remaining_slider.configure(from_=current_song_length, to=0)
            time_remaining_slider.set(current_song_length)
            duration_seconds = int(current_song_length)
            time_remaining_label.configure(
                text=f"{duration_seconds // 60}:{duration_seconds % 60:02d}"
            )
            playing = True
            Stastop.config(text="II")
            if playlistframe is not None and playlistframe.winfo_exists():
                playlistframe.destroy()
            playlist_s = False

        def build_playlist_frame():
            nonlocal playlistframe
            playlistframe = tk.Frame(
                mp3AppBarUp,
                height=300,
                width=300,
                bg=MusicTheme,
                relief=tk.RIDGE,
                borderwidth=2,
            )
            playlistframe.pack_propagate(False)
            playlistbox = tk.Listbox(playlistframe, bg=MusicTheme, fg="white")
            playlistbox.pack(fill="both", expand=True, padx=8, pady=8)
            for songpath in songpaths:
                playlistbox.insert(tk.END, os.path.splitext(os.path.basename(songpath))[0])

            def select_song(event):
                global playlist_s
                selection = playlistbox.curselection()
                if selection:
                    playlistframe.place_forget()
                    playlist_s = False
                    load_song(selection[0])

            playlistbox.bind(
                "<<ListboxSelect>>",
                select_song,
            )

        build_playlist_frame()

        volumeslide = tk.Scale(
            VinlyFrame,
            orient="vertical",
            from_=0,
            to=100,
            tickinterval=0,
            showvalue=0,
            width=10,
            length=250,
            bg=MusicTheme,
            troughcolor="#878a8b",
            highlightthickness=0,
            borderwidth=0
        )
        volumeslide.set(50)
        volumeslide.pack(side="right", padx=5, pady=5)

        def spin(angle=0):
            rotated_image = vinyl_image.rotate(
                angle,
                resample=Image.Resampling.BICUBIC,
                expand=False,
            )
            rotated_photo = ImageTk.PhotoImage(master=root, image=rotated_image)
            vinyl_label.configure(image=rotated_photo)
            vinyl_label.image = rotated_photo
            vinyl_label.after(16, spin, (angle + 0.8) % 360)



        spin()
        playing = False
        def playpause():
            global playing
            if playing:
                pysound.music.pause()
                Stastop.configure(text=">")
                playing = False
            else: 
                pysound.music.unpause()
                Stastop.configure(text="II")
                playing = True


        musictitle = "..."
        artist = "..."

        musiclabel = tk.Label(VinlyFrame,text=musictitle,bg=MusicTheme,font=("Arial",10,"bold"),relief=tk.RIDGE,width=30)
        artistlabel = tk.Label(VinlyFrame,text=artist,bg=MusicTheme)

        musiclabel.place(x=150,y=220,anchor="center")
        artistlabel.place(x=150,y=245,anchor="center")

        ControlFrame = tk.Frame(mp3AppBarUp,height=300,bg=f"{MusicTheme}",borderwidth=3,relief=tk.RIDGE)
        ControlFrame.pack_propagate(False)
        ControlFrame.pack(side="top",fill="x",padx=2,pady=1)

        time_remaining_slider = tk.Scale(
            VinlyFrame,
            orient="horizontal",
            from_=0,
            to=0,
            showvalue=0,
            resolution=1,
            width=5,
            sliderlength=12,
            state="disabled",
            bg=MusicTheme,
            troughcolor="#878a8b",
            highlightthickness=0,
            borderwidth=0,
        )
        time_remaining_label = tk.Label(VinlyFrame, text="0:00", bg=MusicTheme)
        time_remaining_label.pack(side="bottom",pady=(0,2))
        time_remaining_slider.pack(side="bottom", fill="x", padx=20, pady=(10,10))


        def update_time_remaining():
            if current_song_length > 0:
                elapsed_time = max(pysound.music.get_pos(), 0) / 1000
                remaining_time = max(current_song_length - elapsed_time, 0)
                remaining_seconds = int(remaining_time)
                time_remaining_slider.configure(state="normal")
                time_remaining_slider.set(remaining_time)
                time_remaining_slider.configure(state="disabled")
                time_remaining_label.configure(
                    text=f"{remaining_seconds // 60}:{remaining_seconds % 60:02d}"
                )
            vinyl_label.after(1000, update_time_remaining)

        update_time_remaining()

        def advance_playlist():
            if playing and current_song_index is not None and not pysound.music.get_busy():
                next_song_index = current_song_index + 1
                if next_song_index < len(songpaths):
                    load_song(next_song_index)
            vinyl_label.after(250, advance_playlist)

        advance_playlist()

        Framed = ctk.CTkFrame(
            ControlFrame,
            height=100,
            width=250,
            fg_color=darker_color(MusicTheme),
            corner_radius=10,
        )
        nextR=tk.Button(Framed,height=2,width=3,text="<")
        nextL=tk.Button(Framed,height=2,width=3,text=">")
        FastR=tk.Button(Framed,height=2,width=3,text="<<")
        FastL=tk.Button(Framed,height=2,width=3,text=">>")
        Stastop=ctk.CTkButton(Framed,height=50,width=50,text="ll", command=playpause,corner_radius=100,fg_color="Light grey",text_color="Black",
                              border_width=2, )
        Framed.place(relx=0.5,rely=0.5,anchor="center")
        nextL.pack(side="right",padx=3)
        FastL.pack(side="right",padx=3)
        Stastop.pack(side="right",padx=3)
        FastR.pack(side="right",padx=3)
        nextR.pack(side="right",padx=3)
    

    app() 

def RockPaperScissors():

    app_id = f"RPS_{random.randint(1000, 9999)}"
    xRand = 0
    yRand = 0
    xRand , yRand = rollnumber(xRand, yRand)
    
    RPS_frame = tk.Frame(root, width=520, height=355, bg="#3f8099",borderwidth=1, relief=tk.RIDGE)
    RPS_frame.place(x=xRand, y=yRand)
    RPS_frame.pack_propagate(False)

    create_taskbar_button(app_id, RPS_frame, "RPS")

    RPSAppBarUp = tk.Frame(RPS_frame, height=320, bg="Light blue", highlightthickness=0,borderwidth=5, relief=tk.RIDGE)
    RPSAppBarUp.propagate(False)
    RPSAppBarUp.pack(side="bottom", fill="x")

    RPSClosebtn = tk.Button(RPS_frame,
                    text="X",
                    fg="Black", 
                    activebackground="red",
                    width=3, 
                    height=30,
                    command=lambda: closed(RPS_frame, app_id))
    RPSClosebtn.pack(side="right", anchor="ne", padx=1, pady=1)
    
    RPSminiBtn = tk.Button(RPS_frame,
                    text="_",
                    fg="Black", 
                    width=3, 
                    height=30,
                    command=lambda: minimize(app_id, RPS_frame))  
    RPSminiBtn.pack(side="right", anchor="ne", padx=1, pady=1)
    Label = tk.Label(RPS_frame, text="Rock Paper Scissors", bg="#3f8099", font="Arial 10 bold")
    Label.place(x=5, y=5)

    drag = MyDragManager()
    drag.add_draggable_widget(RPS_frame)

    high_score_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rps_high_score.dat")
    try:
        with open(high_score_file, "rb") as file:
            high_score_value = pickle.load(file)
            if not isinstance(high_score_value, int) or high_score_value < 0:
                high_score_value = 0
    except (FileNotFoundError, EOFError, pickle.PickleError, TypeError, ValueError):
        high_score_value = 0

    choices = ("Rock", "Paper", "Scissors")

    def save_high_score():
        with open(high_score_file, "wb") as file:
            pickle.dump(high_score_value, file)

    def game():
        global Frame_2
        nonlocal high_score_value
        Frame_1.destroy()
        Frame_2 = tk.Frame(RPSAppBarUp, width=500, height=300, bg="Light blue")
        Left_frame = tk.Frame(Frame_2, width=250, height=300, bg="Light blue")
        Right_frame = tk.Frame(Frame_2, width=250, height=300, bg="Light blue")
        Left_frame.pack(side="left", fill="both", expand=True)
        Right_frame.pack(side="right", fill="both", expand=True)
        Frame_2.propagate(False)

        ComputerChoiceLabel = tk.Label(Right_frame, text="Computer's Choice: ", font=("Arial", 12, "underline"), bg="Light blue")
        ComputerChoiceLabel.pack(side="top", pady=10)
        Cchoice = tk.Label(Right_frame, text="", font=("Arial", 12), bg="Light blue", borderwidth=2, relief=tk.SOLID)
        Cchoice.pack(side="top", pady=10)

        ResultLabel = tk.Label(Right_frame, text="Result: ", font=("Arial", 12, "underline"), bg="Light blue")
        ResultLabel.pack(side="top", pady=10)
        Result = tk.Label(Right_frame, text="", font=("Arial", 12, "bold"), bg="Light blue", borderwidth=2, relief=tk.SOLID)
        Result.pack(side="top", pady=10)

        PlayerChoiceLabel = tk.Label(Right_frame, text="Your Choice: ", font=("Arial", 12, "underline"), bg="Light blue")
        PlayerChoiceLabel.pack(side="top", pady=10)
        Pchoice = tk.Label(Right_frame, text="", font=("Arial", 12), bg="Light blue", borderwidth=2, relief=tk.SOLID)
        Pchoice.pack(side="top", pady=10)

        Rock=tk.Button(Left_frame, text="Rock", width=20, height=1, borderwidth=5, relief=tk.RIDGE)
        Paper=tk.Button(Left_frame, text="Paper", width=20, height=1, borderwidth=5, relief=tk.RIDGE)
        Scissors=tk.Button(Left_frame, text="Scissors", width=20, height=1, borderwidth=5, relief=tk.RIDGE)

        high_scorelabel = tk.Label(Left_frame, text="High Score", font=("Arial", 12,"underline"), bg="Light blue")
        high_score = tk.Label(Left_frame, text=f"{high_score_value}", font=("Arial", 12, "bold"), bg="Light blue")
        high_scorelabel.pack(side="top", pady=10)
        high_score.pack(side="top", pady=5)

        current_scorelabel = tk.Label(Left_frame, text="Current Score", font=("Arial", 12,"underline"), bg="Light blue")
        current_score = tk.Label(Left_frame, text="0", font=("Arial", 12), bg="Light blue")
        current_scorelabel.pack(side="top", pady=10)
        current_score.pack(side="top", pady=5)
        current_score_value = 0
                                                             

        def play_round(player_choice):
            nonlocal high_score_value, current_score_value
            computer_choice = random.choice(choices)
            Pchoice.config(text=player_choice)
            Cchoice.config(text=computer_choice)

            if player_choice == computer_choice:
                Result.config(text="Tie",bg="#D6CE5B")
            elif ((player_choice == "Rock" and computer_choice == "Scissors") or
                  (player_choice == "Paper" and computer_choice == "Rock") or
                  (player_choice == "Scissors" and computer_choice == "Paper")):
                current_score_value += 1
                current_score.config(text=f"{current_score_value}")
                if current_score_value > high_score_value:
                    high_score_value = current_score_value
                    save_high_score()
                    high_score.config(text=f"{high_score_value}")
                Result.config(text="You win",bg="Green")
            else:
                current_score_value = 0
                current_score.config(text="0")
                Result.config(text="You lose",bg="Red")

        Rock.config(command=lambda: play_round("Rock"))
        Paper.config(command=lambda: play_round("Paper"))
        Scissors.config(command=lambda: play_round("Scissors"))

        BackBtn = tk.Button(Left_frame, text="Back", width=10, height=2, command=lambda: menu())

        
        Frame_2.pack(fill="both")
       
        Rock.pack(side="top", padx=2, pady=2)
        Paper.pack(side="top", padx=2, pady=2)
        Scissors.pack(side="top", padx=2, pady=2)
        BackBtn.pack(side="top", pady=10)

    def menu():
        global Frame_1, Frame_2, Label_1, Button_1, High_score
        try:
            Frame_2.destroy()
        except:
            NameError
            print("GameNotOpenedYet")

        Frame_1 = tk.Frame(RPSAppBarUp, width=500, height=300, bg="Light blue", borderwidth=10, relief=tk.RIDGE)
        Frame_1.propagate(False)
        Label_1 = tk.Label(Frame_1, text="Rock Paper Scissors", font=("Arial", 14, "bold", "underline"), bg="Light Blue")
        desc = tk.Label(Frame_1, text='''Play a game of Rock Paper Scissors, 
        against the computer''', font=("Arial", 10), bg="Light Blue")
        Button_1 = tk.Button(Frame_1, text="Play", width=20, height=2, command=game, relief=tk.RIDGE)
        High_score = tk.Label(Frame_1, text=f"High Score: {high_score_value}", font=("Arial", 12,"underline"), bg="Light blue")
        
        Frame_1.pack(fill="both",padx=10, pady=10, expand=True)
        Label_1.pack(side="top",pady=10)
        desc.pack(side="top", pady=5)
        Button_1.pack(side="top", pady=20,padx=20)
        High_score.pack(side="top", pady=10)
    menu()

def NumGuessGame():
    appId = f"NumGuess_{random.randint(1000, 9999)}"
    xRand = 0
    yRand = 0
    xRand , yRand = rollnumber(xRand, yRand)
    
    NumGuessFrame = tk.Frame(root, width=520, height=355, bg="#3f8099",borderwidth=1, relief=tk.RIDGE)
    NumGuessFrame.place(x=xRand, y=yRand)
    NumGuessFrame.pack_propagate(False)

    create_taskbar_button(appId, NumGuessFrame, "NumGuess")

    NumGuessAppBarUp = tk.Frame(NumGuessFrame, height=320, bg="Light blue", highlightthickness=0,borderwidth=5, relief=tk.RIDGE)
    NumGuessAppBarUp.propagate(False)
    NumGuessAppBarUp.pack(side="bottom", fill="x")

    NumGuessClosebtn = tk.Button(NumGuessFrame,
                    text="X",
                    fg="Black", 
                    activebackground="red",
                    width=3, 
                    height=30,
                    command=lambda: closed(NumGuessFrame, appId))
    NumGuessClosebtn.pack(side="right", anchor="ne", padx=1, pady=1)
    
    NumGuessminiBtn = tk.Button(NumGuessFrame,
                    text="_",
                    fg="Black", 
                    width=3, 
                    height=30,
                    command=lambda: minimize(appId, NumGuessFrame))  
    NumGuessminiBtn.pack(side="right", anchor="ne", padx=1, pady=1)

    drag = MyDragManager()
    drag.add_draggable_widget(NumGuessFrame)

    highScoreFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "num_guess_high_score.dat")
    try:
        with open(highScoreFile, "rb") as file:
            highScoreValue = pickle.load(file)
            if not isinstance(highScoreValue, int) or highScoreValue < 0:
                highScoreValue = 0
    except (FileNotFoundError, EOFError, pickle.PickleError, TypeError, ValueError):
        highScoreValue = 0

    def saveHighScore():
        with open(highScoreFile, "wb") as file:
            pickle.dump(highScoreValue, file)

    def game():
        global gameFrame
        nonlocal highScoreValue
        target = random.randint(1, 10)
        attempts = 0
        score = 0
        MenuFrame.destroy()
        gameFrame = tk.Frame(NumGuessAppBarUp, width=500, height=300, bg="Light blue", borderwidth=10, relief=tk.RIDGE)
        gameFrame.propagate(False)
        gameFrame.pack(side="top",padx=10, pady=10)
        lolframe = tk.Frame(gameFrame, width=500, height=100, bg="Light blue")
        funnyframe = tk.Frame(gameFrame, width=500, height=300, bg="Light blue")
        lolframe.pack(side="top", pady=5, fill="x")
        funnyframe.pack(side="top", pady=5, fill="x")
        aframe = tk.Frame(lolframe, width=500, height=100, bg="Light blue")
        aframe.pack(side="right", pady=5,padx=20)
        bframe = tk.Frame(lolframe, width=500, height=100, bg="Light blue")
        bframe.pack(side="left", pady=5,padx=20)

        optionframe = tk.Frame(funnyframe, width=200, height=300, bg="Light blue")
        optionframe.pack(side="left", pady=5,padx=20)

        jojoframe = tk.Frame(funnyframe, width=300, height=300, bg="Light blue")
        jojoframe.pack(side="right", pady=5,padx=5)

        cochoice = tk.Label(aframe, text="Computer's Thought: ", font=("Arial", 12, "underline"), bg="Light blue")
        cochoice.pack(side="top", pady=10)
        c = tk.Label(aframe, text="( ╹ -╹)?", font=("Arial", 15, "bold"), bg="Light blue", borderwidth=2, relief=tk.SOLID)
        c.pack(side="top", pady=5)

        plchoice = tk.Label(bframe, text="Your Guess: ", font=("Arial", 12, "underline"), bg="Light blue")
        plchoice.pack(side="top", pady=10)
        p = tk.Label(bframe, text="(╭ರ_•́)", font=("Arial", 15, "bold"), bg="Light blue", borderwidth=2, relief=tk.SOLID)
        p.pack(side="top", pady=5)

        resultLabel = tk.Label(lolframe, text="Choose a number",font=("Arial", 12), bg="Light blue", wraplength=180)
        resultLabel.pack(side="top", pady=20)
        scoreLabel = tk.Label(jojoframe, text="Current Score:",font=("Arial", 10,"underline"), bg="Light blue")
        s = tk.Label(jojoframe, text=f"{score}",font=("Arial", 10,"bold"), bg="Light blue")
        scoreLabel.pack(side="top", pady=5)
        s.pack(side="top", pady=2)
        highScoreLabel = tk.Label(jojoframe, text=f"High Score:",font=("Arial", 10,"underline"), bg="Light blue")
        h =tk.Label(jojoframe, text=f"{highScoreValue}",font=("Arial", 10,"bold"), bg="Light blue")
        highScoreLabel.pack(side="top", pady=5)
        h.pack(side="top", pady=2)

        def check_guess(guess):
            nonlocal target, attempts, score, highScoreValue
            attempts += 1
            
            
            if guess == target:
                score += 1
                if score > highScoreValue:
                    highScoreValue = score
                    saveHighScore()
                    h.config(text=f"High Score: {highScoreValue}")
                resultLabel.config(text="WIN!.", fg="green")
                p.config(text=f"{str(guess)}     ٩(ˊᗜˋ )و")
                c.config(text=f"{str(target)}    ( ･_･ ) ")
            else:
                p.config(text=f"{str(guess)}    ( ･_･ )")
                c.config(text=f"{str(target)}   ٩(ˊᗜˋ )و")
                resultLabel.config(text="LOSE...", fg="red")
            s.config(text=f"{score}")
            target = random.randint(1, 10)

        numberFrame = tk.Frame(optionframe, bg="Light blue")
        numberFrame.pack(side="top", pady=5)
        for number in range(1, 11):
            guessButton = tk.Button(numberFrame, text=str(number), width=6, height=2,
                                     command=lambda value=number: check_guess(value))
            guessButton.grid(row=(number - 1) // 5, column=(number - 1) % 5, padx=2, pady=2)

        backButton = tk.Button(gameFrame, text="Back", width=12, command=menu)
        backButton.pack(side="top", pady=5)

    def menu():
        try:
            gameFrame.destroy()
        except:
            NameError
            print("GameNotOpenedYet")
        global MenuFrame
        Label = tk.Label(NumGuessFrame, text="NumGUESS", bg="#3f8099", font="Arial 10 bold")
        Label.place(x=5, y=5)

        MenuFrame = tk.Frame(NumGuessAppBarUp, bg="Light blue", borderwidth=10, relief=tk.RIDGE)
        Header = tk.Label(MenuFrame, text="NumGUESS", font=("Arial", 14, "bold", "underline"), bg="Light blue")
        desc = tk.Label(MenuFrame, text='''Guess the number between 1 to 10, 
        that the computer has chosen.''', font=("Arial", 10), bg="Light blue")
        highScore = tk.Label(MenuFrame, text=f"High Score: {highScoreValue}", font=("Arial", 12, "underline"), bg="Light blue")

        play = tk.Button(MenuFrame, text="Play", width=20, height=2, relief=tk.RIDGE, command=game)

        MenuFrame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        Header.pack(side="top", pady=10)
        desc.pack(side="top", pady=5)
        play.pack(side="top", pady=20)
        highScore.pack(side="top", pady=5)

    menu()
def File_Explorer():
    app_id = f"FileExplorer_{random.randint(1000, 9999)}"
    xRand = 0
    yRand = 0
    xRand , yRand = rollnumber(xRand, yRand)
    
    FileExplorer_frame = tk.Frame(root, width=520, height=355, bg="#3f8099",borderwidth=1, relief=tk.RIDGE)
    FileExplorer_frame.place(x=xRand, y=yRand)
    FileExplorer_frame.pack_propagate(False)

    create_taskbar_button(app_id, FileExplorer_frame, "File Explorer")

    FileExplorerAppBarUp = tk.Frame(FileExplorer_frame, height=320, bg="Light blue", highlightthickness=0,borderwidth=5, relief=tk.RIDGE)
    FileExplorerAppBarUp.propagate(False)
    FileExplorerAppBarUp.pack(side="bottom", fill="x")

    FileExplorerClosebtn = tk.Button(FileExplorer_frame,
                    text="X",
                    fg="Black", 
                    activebackground="red",
                    width=3, 
                    height=30,
                    command=lambda: closed(FileExplorer_frame, app_id))
    FileExplorerClosebtn.pack(side="right", anchor="ne", padx=1, pady=1)
    
    FileExplorerminiBtn = tk.Button(FileExplorer_frame,
                    text="_",
                    fg="Black", 
                    width=3, 
                    height=30,
                    command=lambda: minimize(app_id, FileExplorer_frame))  
    FileExplorerminiBtn.pack(side="right", anchor="ne", padx=1, pady=1)

    drag = MyDragManager()
    drag.add_draggable_widget(FileExplorer_frame)

    label = tk.Label(FileExplorer_frame, text="File Explorer", bg="#3f8099", font="Arial 10 bold")
    label.place(x=5, y=5)

    style = ttk.Style()
    style.configure("Mainframe.TFrame", background="Light blue", borderwidth=10, relief=tk.RIDGE)
    Mainframe = ttk.Frame(FileExplorerAppBarUp, width=500, height=300, style="Mainframe.TFrame")
    Mainframe.pack_propagate(False)
    Mainframe.pack(side="top",fill="both", padx=2, pady=2)

    TreeFrame = ttk.Frame(Mainframe, width=150, height=300, style="Mainframe.TFrame")
    TreeFrame.pack(side="left", fill="y", padx=2, pady=2)

    Tree = ttk.Treeview(TreeFrame)
    Tree.heading("#0", text="Directories", anchor="w")
    ParentNode = Tree.insert("", "end", text="Documents", open=True)
    doc1 = Tree.insert(ParentNode, "end", text="Document 1.txt")
    doc2 = Tree.insert(ParentNode, "end", text="Document 2.txt")

    ParentNode2 = Tree.insert("", "end", text="Pictures", open=True)
    pic1 = Tree.insert(ParentNode2, "end", text="Picture 1.png")
    pic2 = Tree.insert(ParentNode2, "end", text="Picture 2.jpg")
    Tree.pack(side="left", fill="y", padx=2, pady=2)


    Frame1 = ttk.Frame(Mainframe, width=350, height=300, style="Mainframe.TFrame")
    Frame1.pack_propagate(False)
    Frame1.pack(side="right", fill="both", expand=True, padx=2, pady=2)

    def show_parent(event):
        selected_item = Tree.selection()
        if not selected_item:
            return

        for widget in Frame1.winfo_children():
            widget.destroy()

        if selected_item[0] == ParentNode:
            tk.Label(Frame1, text="Documents Folder", font=("Arial", 14), bg="Light blue").pack(pady=10)
            tk.Frame(Frame1, bg="Light blue").pack(fill="both", expand=True, padx=10, pady=10)

            


        elif selected_item[0] == ParentNode2:
            tk.Label(Frame1, text="Pictures Folder", font=("Arial", 14), bg="Light blue").pack(pady=10)
            tk.Frame(Frame1, bg="Light blue").pack(fill="both", expand=True, padx=10, pady=10)


    Tree.bind("<<TreeviewSelect>>", show_parent)

def Imageview():
    appId = f"ImgView_{random.randint(1000, 9999)}"
    xRand = 0
    yRand = 0
    xRand , yRand = rollnumber(xRand, yRand)
    
    imgViewFrame = tk.Frame(root, width=520, height=355, bg="#3f8099",borderwidth=1, relief=tk.RIDGE)
    imgViewFrame.place(x=xRand, y=yRand)
    imgViewFrame.pack_propagate(False)

    create_taskbar_button(appId, imgViewFrame, "JPSPhotos")

    imgViewAppBar = tk.Frame(imgViewFrame, height=320, bg="Light blue", highlightthickness=0,borderwidth=5, relief=tk.RIDGE)
    imgViewAppBar.pack_propagate(False)
    imgViewAppBar.pack(side="bottom", fill="both", expand=True)

    fileExplorerCloseBtn = tk.Button(imgViewFrame,
                    text="X",
                    fg="Black", 
                    activebackground="red",
                    width=3, 
                    height=30,
                    command=lambda: closed(imgViewFrame, appId))
    fileExplorerCloseBtn.pack(side="right", anchor="ne", padx=1, pady=1)
    
    fileExplorerMiniBtn = tk.Button(imgViewFrame,
                    text="_",
                    fg="Black", 
                    width=3, 
                    height=30,
                    command=lambda: minimize(appId, imgViewFrame))  
    fileExplorerMiniBtn.pack(side="right", anchor="ne", padx=1, pady=1)

    drag = MyDragManager()
    drag.add_draggable_widget(imgViewFrame)

    label = tk.Label(imgViewFrame, text="Image Viewer", bg="#3f8099", font="Arial 10 bold")
    label.place(x=5, y=5) 
    img1 = os.path.join(os.path.dirname(__file__), "ImageAssets2", "1.jpeg")
    img2 = os.path.join(os.path.dirname(__file__), "ImageAssets2", "2.jpeg")
    img3 = os.path.join(os.path.dirname(__file__), "ImageAssets2", "3.jpeg")
    imagePaths = [img1, img2, img3]

    frame1 = tk.Frame(imgViewAppBar, width=100, height=310, bg="Light blue",borderwidth=2, relief=tk.RIDGE)
    frame1.pack_propagate(False)
    frame2 = tk.Frame(imgViewAppBar, bg="Light blue")

    thumbnailImages = []
    previewImages = []
    for imagePath in imagePaths:
        image = Image.open(imagePath)
        thumbnailImage = image.copy()
        thumbnailImage.thumbnail((110, 80), Image.LANCZOS)
        previewImage = image.copy()
        previewImage.thumbnail((370, 255), Image.LANCZOS)
        thumbnailImages.append(ImageTk.PhotoImage(master=root,  image=thumbnailImage))
        previewImages.append(ImageTk.PhotoImage(master=root,  image=previewImage))

    currentIndex = 0

    def buildGallery():
        frame1.pack_forget()
        frame2.pack_forget()
        for widget in frame1.winfo_children():
            widget.destroy()
        for widget in frame2.winfo_children():
            widget.destroy()
        frame1.pack(side="left", fill="y", padx=5, pady=5)
        frame2.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        galleryFrame = tk.Frame(frame2, width=200, height=300, bg="Light blue", borderwidth=2, relief=tk.RIDGE)
        galleryFrame.pack_propagate(False)
        header = tk.Label(galleryFrame, text="Gallery", font=("Arial", 15, "underline"), bg="Light Blue")
        galleryFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        header.pack(side="top", padx=10, pady=10, anchor="w")

        for index, thumbnail in enumerate(thumbnailImages):
            thumbnailButton = tk.Button(
                galleryFrame,
                image=thumbnail,
                borderwidth=2,
                relief=tk.RIDGE,
                command=lambda index=index: showImage(index),
            )
            thumbnailButton.pack(side="top", padx=8, pady=8)

    def showImage(index):
        nonlocal currentIndex
        currentIndex = index % len(previewImages)

        frame1.pack_forget()
        frame2.pack_forget()
        for widget in frame2.winfo_children():
            widget.destroy()
        frame2.pack(fill="both", expand=True)

        enlargedFrame = tk.Frame(frame2, bg="Light blue", borderwidth=2, relief=tk.RIDGE)
        enlargedFrame.pack(fill="both", expand=True)
        backButton = tk.Button(enlargedFrame, text="Back", command=buildGallery)
        backButton.pack(side="bottom", pady=5)
        previousButton = tk.Button(enlargedFrame,width=1,text="<",font=("Arial", 16, "bold"),command=lambda: showImage(currentIndex - 1))
        previousButton.pack(side="left", padx=2)
        nextButton = tk.Button(enlargedFrame,width=1,text=">",font=("Arial", 16, "bold"),command=lambda: showImage(currentIndex + 1))
        nextButton.pack(side="right", padx=2)
        previewLabel = tk.Label(enlargedFrame, image=previewImages[currentIndex], bg="Light blue")
        previewLabel.pack(side="top",fill="both", expand=True)

        enlargedFrame.image = previewImages[currentIndex]

    buildGallery()
    
    
def JPSPaint():
    global e, p, l, BrustColor, BrushSize
    appId = f"Paint_{random.randint(1000, 9999)}"
    paint_color = "#000000"

    def choose_preset(color):
        nonlocal paint_color
        paint_color = color
        global BrustColor
        BrustColor = color
        selected_color.configure(bg=paint_color)

    xRand = 0
    yRand = 0
    xRand , yRand = rollnumber(xRand, yRand)
    
    PaintFrame = tk.Frame(root, width=520, height=355, bg="#3f8099",borderwidth=1, relief=tk.RIDGE)
    PaintFrame.place(x=xRand, y=yRand)
    PaintFrame.pack_propagate(False)

    create_taskbar_button(appId, PaintFrame, "JPSPaint")

    PaintAppBar = tk.Frame(PaintFrame, height=320, bg="Light blue", highlightthickness=0,borderwidth=5, relief=tk.RIDGE)
    PaintAppBar.pack_propagate(False)
    PaintAppBar.pack(side="bottom", fill="both", expand=True)

    PaintCloseBtn = tk.Button(PaintFrame,
                    text="X",
                    fg="Black", 
                    activebackground="red",
                    width=3, 
                    height=30,
                    command=lambda: closed(PaintFrame, appId))
    PaintCloseBtn.pack(side="right", anchor="ne", padx=1, pady=1)
    
    PaintMiniBtn = tk.Button(PaintFrame,
                    text="_",
                    fg="Black", 
                    width=3, 
                    height=30,
                    command=lambda: minimize(appId, PaintFrame))  
    PaintMiniBtn.pack(side="right", anchor="ne", padx=1, pady=1)

    drag = MyDragManager()
    drag.add_draggable_widget(PaintFrame)

    label = tk.Label(PaintFrame, text="JPSPaint", bg="#3f8099", font="Arial 10 bold")
    label.place(x=5, y=5) 

    p = True
    e = False
    l = False

    BrushSize = tk.IntVar(value=4)
    BrustColor = "#000000"

    def lastpos(event):
        global lastpos
        Canvaslol.focus_set()
        lastpos = (event.x,event.y)
        draw(event)

    def draw(event):
        label.config(text=f"x:{event.x},\ny:{event.y}")
        global e
        global lastpos
        x,y = lastpos
        Color = "White" if e else paint_color
        Canvaslol.create_line(x,y,event.x,event.y,smooth=True, fill=Color, width=BrushSize.get(),capstyle=tk.ROUND,joinstyle=tk.ROUND)
        if not l:
            lastpos=(event.x,event.y)
        else:
            return        

    def eraser(_event=None):
        global e,l
        Canvaslol.configure(cursor="dotbox")
        l = False
        e = True

    def pen(_event=None):
        global e,l
        Canvaslol.configure(cursor="pencil")
        l = False
        e = False
    def lasso_fill(_event=None):
        global l,e,p
        Canvaslol.configure(cursor="hand1")
        e = False
        p = False
        l = True

    def updatexy(event):
        label.config(text=f"x:{event.x},\ny:{event.y}")
        

    def release(event):
        global lastpos
        lastpos=None
    Mframe = tk.Frame(PaintAppBar, bg="Light Blue",relief=tk.RIDGE)
    Mframe.pack(fill="both",padx=5,pady=5)
    TopBarFrame = tk.Frame(Mframe, bg='Light blue',height=30,borderwidth=2, relief=tk.RIDGE)
    Pen = tk.Button(TopBarFrame,width=3,text='P', command=pen, bg='Light blue')
    Eraser = tk.Button(TopBarFrame,width=3,text="E", command=eraser,bg='Light blue')
    LassoFill = tk.Button(TopBarFrame,width=3,text="L", command=lasso_fill,bg='Light blue')
    #Back=tk.Button(TopBarFrame,width=6,text="Back",bg='Light blue')
    #Save = tk.Button(TopBarFrame,width=6,text="Save",bg='Light blue')
    Pen.pack(side="left",padx=1,pady=1)
    Eraser.pack(side="left",padx=1,pady=1)
    LassoFill.pack(side="left",padx=1,pady=1)
    #Save.pack(side="right",padx=1,pady=1)
    #Back.pack(side="right",padx=1,pady=1)
    BottomFramw = tk.Frame(Mframe, bg="Light blue",height=300)
    midframe = tk.Frame(BottomFramw, bg="Light blue",height=300)
    scaleframe = tk.Frame(midframe, borderwidth=2, relief=tk.RIDGE,bg='Light blue')
    scale = tk.Scale(scaleframe, from_=1, to=40, variable=BrushSize, orient="vertical", length=120,bg='Light blue')
    label = tk.Label(midframe, borderwidth=2,relief=tk.RIDGE,text="x:_,\ny:_",width=10,height=5,bg='Light blue')
    CanvasFrame = tk.Frame(BottomFramw, bg="Light blue",width=500, borderwidth=2,relief=tk.RIDGE)
    Canvaslol = tk.Canvas(CanvasFrame, background="White", cursor="pencil")
    ColorsFrame = tk.Frame(BottomFramw,bg='Light blue', width=88, height=250, borderwidth=2,relief=tk.RIDGE)
    ColorsFrame.pack_propagate(False)
    color_presets = [
        "#000000", "#FFFFFF", "#808080", "#C0C0C0", "#800000", "#FF0000",
        "#808000", "#FFFF00", "#008000", "#00FF00", "#008080", "#00FFFF",
        "#000080", "#0000FF", "#800080", "#FF00FF", "#A52A2A", "#FFA500",
    ]
    selected_color = tk.Label(ColorsFrame, bg=paint_color, width=4, height=2, relief=tk.SUNKEN)

    for index, color in enumerate(color_presets):
        color_button = tk.Button(
            ColorsFrame,
            bg=color,
            activebackground=color,
            width=2,
            height=1,
            font=("Arial", 7),
            padx=0,
            pady=0,
            relief=tk.RAISED,
            command=lambda preset=color: choose_preset(preset),
        )
        color_button.grid(row=index % 9, column=index // 9, padx=2, pady=1)
    

    
    TopBarFrame.pack(side="top",fill="x", padx=1,pady=1)
    BottomFramw.pack(side="top", fill="both")
    CanvasFrame.pack(side="left",padx=1,pady=1)
    ColorsFrame.pack(side="right",padx=1,pady=1,fill="both")
    midframe.pack(side="right",padx=1,pady=1,fill="both")
    label.pack(side="bottom",padx=1,pady=1)
    scaleframe.pack(side="top",padx=0.5,pady=0.5)
    scale.pack()
    Canvaslol.pack(fill="both")
    selected_color.grid(row=9, column=0, columnspan=2, padx=2, pady=(5, 2))

    Canvaslol.bind("<Motion>", updatexy)
    Canvaslol.bind("<Button-1>", lastpos)
    Canvaslol.bind("<B1-Motion>", draw)
    Canvaslol.bind("<ButtonRelease-1>", release)
    Canvaslol.bind("<KeyPress-e>", eraser)
    Canvaslol.bind("<KeyPress-E>", eraser)
    Canvaslol.bind("<KeyPress-p>", pen)
    Canvaslol.bind("<KeyPress-P>", pen)


def JPS_Notes():
    app_id = f"Notes_{random.randint(1000, 9999)}"
    xRand = 0
    yRand = 0
    xRand , yRand = rollnumber(xRand, yRand)
    
    Notes_frame = tk.Frame(root, width=520, height=355, bg="#3f8099",borderwidth=1, relief=tk.RIDGE)
    Notes_frame.place(x=xRand, y=yRand)
    Notes_frame.pack_propagate(False)

    create_taskbar_button(app_id, Notes_frame, "Notes")

    NotesAppBarUp = tk.Frame(Notes_frame, height=320, bg="Light blue", highlightthickness=0,borderwidth=5, relief=tk.RIDGE)
    NotesAppBarUp.propagate(False)
    NotesAppBarUp.pack(side="bottom", fill="x")

    NotesClosebtn = tk.Button(Notes_frame,
                    text="X",
                    fg="Black", 
                    activebackground="red",
                    width=3, 
                    height=30,
                    command=lambda: closed(Notes_frame, app_id))
    NotesClosebtn.pack(side="right", anchor="ne", padx=1, pady=1)
    
    NotesminiBtn = tk.Button(Notes_frame,
                    text="_",
                    fg="Black", 
                    width=3, 
                    height=30,
                    command=lambda: minimize(app_id, Notes_frame))  
    NotesminiBtn.pack(side="right", anchor="ne", padx=1, pady=1)




    

    Notes = MyDragManager()
    Notes.add_draggable_widget(Notes_frame)

    Note_1_path = os.path.join(os.path.dirname(__file__), "JPS Notes", "Note1.txt") 
    Note_2_path = os.path.join(os.path.dirname(__file__), "JPS Notes", "Note2.txt") 
    Note_3_path = os.path.join(os.path.dirname(__file__), "JPS Notes", "Note3.txt") 
    Note_4_path = os.path.join(os.path.dirname(__file__), "JPS Notes", "Note4.txt") 
    Note_5_path =  os.path.join(os.path.dirname(__file__), "JPS Notes", "Note5.txt")  
    note_names_path = os.path.join(os.path.dirname(__file__), "JPS Notes", "note_names.txt")
    default_note_names = ["Note 1", "Note 2", "Note 3", "Note 4", "Note 5"]
    try:
        with open(note_names_path, "r", encoding="utf-8") as names_file:
            note_names = [line.rstrip("\n") for line in names_file]
        if len(note_names) != len(default_note_names):
            note_names = default_note_names.copy()
    except FileNotFoundError:
        note_names = default_note_names.copy()
    def tempAction():
        NoteOpenFrame.destroy()
        NotesApp()
    def Note_Open(Notee, note_index):
        global NotesOpenEntry, NoteOpenFrame, WriteBtn, BackBtn, NoteNameEntry
        with open(Notee,"r") as nt:
            a = nt.read()
            Notes_frame1.destroy()
            NotesTitle.destroy()


        NoteOpenFrame = tk.Frame(NotesAppBarUp, width=500, height=300, bg="Light blue")
        NoteOpenFrame.pack(side="left",padx=10, pady=10)
        NoteOpenFrame.propagate(False)
        NotesOpenEntry = tk.Text(NoteOpenFrame, bg = "Light Blue", width=400, height=200)
        NotesOpenEntry.insert(1.0,a)
        NotesOpenEntry.propagate(False)
        NotesOpenEntry.place(x=0, y=5, width=400, height=250)
        NoteNameEntry = tk.Entry(NoteOpenFrame, bg = "Light Blue", width = 20)
        NoteNameEntry.insert(1, note_names[note_index])
        NoteNameEntry.place(x=0,y=270)
        WriteBtn = tk.Button(NoteOpenFrame, text="Save", height=2, width=10,
                 command=lambda: Note_Write(Notee, note_index))
        WriteBtn.place(x=406, y=0)
        BackBtn = tk.Button(NoteOpenFrame, text="Back", height=2, width = 10, command=tempAction)
        BackBtn.place(x=406, y= 50)

    def Note_Write(Note, note_index):
        with open(Note,"w") as nt1:
            nt1.write(NotesOpenEntry.get("1.0","end"))
        note_names[note_index] = NoteNameEntry.get()
        with open(note_names_path, "w", encoding="utf-8") as names_file:
            names_file.write("\n".join(note_names) + "\n")
        if note_index < len(NotesListBtn) and NotesListBtn[note_index].winfo_exists():
            NotesListBtn[note_index].config(text=NoteNameEntry.get())


        
    def NotesApp():
        global Notes_frame1, NotesTitle,NotesList,NotesListBtn
        NoteApp_label = tk.Label(Notes_frame, text= "JPS Notes", bg="#3f8099", font="Arial 10 bold")
        NoteApp_label.place(x=5, y=5)
        Notes_frame1 = tk.Frame(NotesAppBarUp, width=500, height=300, bg="Light blue")
        Notes_frame1.propagate(False)
        Notes_frame1.pack(side="left",padx=10, pady=10)
        NotesTitle = tk.Label(NotesAppBarUp, text= "JPS Notes", font= "Roman 18 bold underline",width=10, height=2, bg="Light blue")
        desc1 = tk.Label(NotesAppBarUp, text="Write and save notes,", font=("Arial", 10), bg="Light blue")
        desc2 = tk.Label(NotesAppBarUp, text="Click on a note to open it", font=("Arial", 10), bg="Light blue")

        NotesTitle.pack(side = "right", anchor="ne", padx=60)
        desc1.place(relx=0.8, y=50, anchor="n")
        desc2.place(relx=0.8, y=70, anchor="n")
        NotesList = note_names
        NotesListBtn = []
        
        
        for j,button_N in enumerate(NotesList):
            btn = tk.Button(Notes_frame1, text=button_N, width=20, height=1, font=("Arial", 14), relief=tk.RIDGE)
            btn.grid(row=j, column=0, padx=5, pady=5)
            NotesListBtn.append(btn)
        note_paths = [Note_1_path, Note_2_path, Note_3_path, Note_4_path, Note_5_path]
        for note_index, (note_button, note_path) in enumerate(zip(NotesListBtn, note_paths)):
            note_button.config(command=lambda path=note_path, index=note_index: Note_Open(path, index))





    NotesApp()
def DesktopApps():
    app1= tk.Button(MotherFrame, text = "JPS\nNotes", height=3,width=7, bg="Light blue", borderwidth=5, relief=tk.RIDGE, command=JPS_Notes)
    app2= tk.Button(MotherFrame, text = "Calcu\nlator", height=3,width=7, bg="Light blue", borderwidth=5, relief=tk.RIDGE, command=Calculator)
    app3= tk.Button(MotherFrame, text = "Settings", height=3,width=7, bg="Light blue", borderwidth=5, relief=tk.RIDGE, command=Settings)
    app4= tk.Button(MotherFrame, text = "RPS", height=3,width=7, bg="Light blue", borderwidth=5, relief=tk.RIDGE, command=RockPaperScissors)
    app5= tk.Button(MotherFrame, text = "Num\nGUESS", height=3,width=7, bg="Light blue", borderwidth=5, relief=tk.RIDGE, command=NumGuessGame)
    app5.propagate(False)
    app6= tk.Button(MotherFrame, text = "JPS\nPaint", height=3,width=7, bg="Light blue", borderwidth=5, relief=tk.RIDGE, command=JPSPaint)
    app7= tk.Button(MotherFrame, text = "JPS\n PHOTOS", height=3,width=7, bg="Light blue", borderwidth=5, relief=tk.RIDGE, command=Imageview)
    app8= tk.Button(MotherFrame, text = "JPS\n Vinyl", height=3,width=7, bg="Light blue", borderwidth=5, relief=tk.RIDGE, command=mp3)
    app1.place(x=10,y=30)

    app2.place(x=10, y=110)
    app3.place(x=10,  y=190)
    app4.place(x=90, y=30)
    app5.place(x=90,y=110)
    app6.place(x=90,y=190)
    app7.place(x=10,y=270)
    app8.place(x=10,y=350)

def desktopFunc():
    global Start, St_toggle, root, Taskbar, StartButton, taskbar_buttons,Calend , cl_toggle, Time,Wallp, MotherFrame, LoginSwitch, GrandmaFrame, Sd_toggle, ShutMenu, shut
    if LoginSwitch:
        GrandmaFrame.destroy()
        LoginSwitch = False    
        if "MotherFrame" in globals() and MotherFrame.winfo_exists():
            MotherFrame.lift()
            for child in root.winfo_children():
                if child != MotherFrame:
                    child.lift()
            return
    St_toggle = False
    cl_toggle = False
    Sd_toggle = False
    Wallp = None

    taskbar_buttons = {}
    
   
    MotherFrame = tk.Frame(root)
    MotherFrame.pack(fill="both", expand=True)

    label = tk.Label(MotherFrame, 
                     text = '''JPS''',
                     font = "ROMAN 50 bold",
                     bg = "white")
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    DesktopApps()
    Start = tk.Frame(MotherFrame, 
                     bg="#24456F",
                     width=238, 
                     height=int(720/2))
    Start.propagate(False)
    Calend = tk.Frame(root, 
            bg="#24456F",
            width=int(1020/4), 
            height=int(720/2))

    ShutMenu = tk.Frame(root, height=110, width=100, bg="#24456F", borderwidth=4, relief=tk.RIDGE)
    ShutMenu.pack_propagate(False)
    ShutMenu.place_forget()

    Lock = tk.Button(ShutMenu, text="Lock", width=20, height=2, command=lambda: Startup())
    Sdown = tk.Button(ShutMenu, text="Shutdown", width=20, height=2, command=sys.exit)

    Lock.pack(side="top", padx=5, pady=5)
    Sdown.pack(side="top", padx=5, pady=5)
    shut_frame = tk.Frame(Start, bg="#24456F", borderwidth=1, relief=tk.RIDGE)
    shut_frame.pack(side="left", fill="y",padx=2,pady=2)
    apps_frame = tk.Frame(Start, bg="#24456F",borderwidth=1, relief=tk.RIDGE, height= 200, width= 600)
    apps_frame.pack_propagate(False)
    apps_frame.pack(side="left", fill="y",padx=1,pady=2)

    apps = ["JPS Notes", "Calculator", "RPS", "NumGUESS","Settings","JPSPaint"]
    app_buttons = []
    for i,button_T in enumerate(apps):
        btn = tk.Button(apps_frame, text=button_T, width=15, height=1, font=("Arial", 14), borderwidth=5, relief=tk.RIDGE)
        btn.grid(row=i, column=0, padx=5, pady=5)
        app_buttons.append(btn)

    


    shut = tk.Button(shut_frame, text='S',width = 2, height =2,command=Shutdown)
    shut.pack(side="bottom", padx=5, pady=5)

  
    app_buttons[1].config(command=Calculator)
    app_buttons[0].config(command=JPS_Notes)
    app_buttons[2].config(command=RockPaperScissors)
    app_buttons[3].config(command=NumGuessGame)
    app_buttons[4].config(command=Settings)
    app_buttons[5].config(command=JPSPaint)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    '''YEAR = 2026
    MONTH_NAME = "February"
    DAYS_IN_MONTH = 28
    START_DAY_COL = 6  
    tk.Label(Calend, text=f"{MONTH_NAME} {YEAR}", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=7, pady=10)
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(weekdays):
        tk.Label(Calend, text=day, font=("Arial", 10, "bold"), width=5).grid(row=1, column=i)
    current_row = 2
    current_col = START_DAY_COL
    for day in range(1, DAYS_IN_MONTH + 1):
    
        tk.Button(Calend, text=str(day), relief="raised", width=5, height=2).grid(row=current_row, column=current_col, padx=2, pady=2)
        current_col += 1
        if current_col > 6: 
            current_col = 0
            current_row += 1'''
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------#        
    
    Taskbar = tk.Frame(MotherFrame, bg="#24456F", height=40)
    Taskbar.propagate(False)
    Taskbar.pack(side="bottom", fill="x")

    Time = tk.Button(Taskbar, bg ="#24456F", text=f'''{dt} 
 {number_date}''', fg="White")
    Time.pack(side="right", padx=5, fill="y")
    
    StartButton = tk.Button(Taskbar, text="JPS", width=10, font="Arial 10 bold", command=startFunc)
    StartButton.pack(side="left", padx=10, pady=5)

    SettingsBtn = tk.Button(Taskbar, text="⚙", width=2, height=1,fg="#24456F",command=lambda: Settings())
    SettingsBtn.pack(side="right")

    default_wallpaper = os.path.join(os.path.dirname(__file__), "ImageAssets", "DeathStranding2.png")
    set_desktop_wallpaper(default_wallpaper)

    

#Consolestartup()

def Startup():
    global root, LoginBut, LoginSwitch, GrandmaFrame
    LoginSwitch = True
    existing_root = "root" in globals() and root.winfo_exists()
    if not existing_root:
        main = tk.Tk()
        main.configure(background="black")
        main.attributes("-fullscreen", True)
        main.update()
        root = tk.Tk()
    root.title("Desktop")
    root.geometry(f"1020x{root.winfo_screenheight()-40}+{(root.winfo_screenwidth()//2)-510}+0") #510 = 1020/2
    root.resizable(False, False)
    
    def logincred(event):
        def j(event):
            LoginBUT.configure(relief=tk.SUNKEN)
            checkcred()
        def statusupdate(event):
            status.configure(text="")
        def checkcred():
            entered_password = passw.get()
            with open("cred.dat", "rb") as credential_file:
                stored_password = pickle.load(credential_file)
            if entered_password == stored_password:
                desktopFunc()
            else:
                status.configure(text="Wrong password", fg="red")

        mat = tk.Frame(Login_frame, bg="Light blue",height=300,width=400)
        mat.pack()
        Logincred = tk.Frame(mat, height=300,width=400, bg="Light Blue",borderwidth=5, relief=tk.RIDGE)
        Logincred.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        Logincred.pack_propagate(False)
        Userlabel = tk.Label(Logincred, image=photog,height=100,width=100,borderwidth=4,relief=tk.RIDGE)
        Userlabel2 = tk.Label(Logincred, text="Pranav",font=("Arial", 13,"bold"), bg="Light blue")
        Userlabel.pack(side="top",padx=10,pady=10)
        Userlabel2.pack(side="top",padx=3,pady=3)
        passw = tk.Entry(Logincred,width=30,show="*",font=("Arial", 12),borderwidth=3, relief=tk.SUNKEN)
        passwl = tk.Label(Logincred, text="Enter password",bg="Light blue")
        passw.pack(side="top")
        passwl.pack(side="top")
        LoginBUT = tk.Button(Logincred, text="Login", width=15, height=1,command=checkcred, relief=tk.RAISED)
        loluframe = tk.Frame(Logincred, width=500,height=100,bg="Light blue")
        loluframe.pack_propagate(False)
        LoginBUT.pack(side="top", padx=10,pady=10)
        loluframe.pack(side="top",padx=3,pady=3)
        status = tk.Label(loluframe,text="",bg="Light blue")
        status.place(relx=0.5, rely=0.5, anchor="center")
        Logincred.lift()
        
        bac = tk.Button(loluframe, text="<",height=2, command=lambda: mat.destroy())
        bac.pack(side="left", anchor="sw", padx=10,pady=10)

        passw.bind("<Key>", statusupdate)
        passw.bind("<Return>", j)
        return "break"

        

    def users():
        global Login_frame, photog
        Time.place_forget()
        DayDate.place_forget()
        Login_frame = tk.Frame(GrandmaFrame, width=800, height=600, bg="#24456F", borderwidth=10, relief=tk.RIDGE)
        Users_frame = tk.Frame(Login_frame, width=700, height=400, bg="white", borderwidth=5, relief=tk.RIDGE)
        Users_frame.pack_propagate(False)
        labe = tk.Label(Login_frame, text="Default password: password123",borderwidth=5,relief=tk.RIDGE,font=("Arial",10))
        labe.place(x=520,y=500)
        img = os.path.join(os.path.dirname(__file__), "ImageAssets", "user1.png")
        imaged = Image.open(img)
        imaged = imaged.resize((100, 100), Image.LANCZOS)
        photog = ImageTk.PhotoImage(master=root,  image=imaged)
        user_cards_frame = tk.Frame(Users_frame, bg="white")
        user_cards_frame.pack(expand=True)
        User1_frame = tk.Frame(user_cards_frame, width=120, height=150, bg="white")
        User1_frame.pack_propagate(False)
        User1_frame.pack(side="left", padx=5, pady=5)
        userlabel = tk.Label(User1_frame, image=photog,text="Pranav", borderwidth=5, relief=tk.RIDGE)
        userlabel.image = photog

        img2 = os.path.join(os.path.dirname(__file__), "ImageAssets", "23.jpg")
        imaged2 = Image.open(img2)
        imaged2 = imaged2.resize((100, 100), Image.LANCZOS)
        photo2 = ImageTk.PhotoImage(master=root,  image=imaged2)

        for widget in (User1_frame, userlabel):
            widget.bind("<Button-1>", logincred)

        User2_frame = tk.Frame(user_cards_frame, width=120, height=150, bg="white")
        User2_frame.pack_propagate(False)
        User2_frame.pack(side="left", padx=5, pady=5)
        userlabel2 = tk.Label(User2_frame, image=photo2,text="Guest", borderwidth=5, relief=tk.RIDGE)
        userlabel2.image = photo2
        for widget in (User2_frame, userlabel2):
            widget.bind("<Button-1>", lambda event: desktopFunc())

        
        userlabel.pack(side="top", pady=5)
        name = tk.Label(User1_frame, text="Pranav", font="Arial 15", bg="white", fg="black")
        name.pack(side="bottom", pady=5)
        userlabel2.pack(side="top", pady=5)
        name2 = tk.Label(User2_frame, text="Guest", font="Arial 15", bg="white", fg="black")
        name2.pack(side="bottom", pady=5)
        Login_frame.propagate(False)

        def Dateinfo():
            Login_frame.destroy()
            DayDate.place(x=40, y=580)
            Time.place(x=40, y=500)

        Label = tk.Label(Login_frame, text="Select User", font="Comfortaa 20 underline", bg="White")
        BackBtn = tk.Button(Login_frame, text="<", width=5, height=2,bg="Light blue", command=Dateinfo)
        
        Login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        Users_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        Label.pack(side="top", pady=20)
        BackBtn.pack(side="bottom",anchor="sw", pady=10,padx=10)
        Login_frame.lift()
   
    GrandmaFrame = tk.Frame(root, bg="Light blue")
    GrandmaFrame.place(x=0, y=0, relwidth=1, relheight=1)
    GrandmaFrame.lift()

    img = os.path.join(os.path.dirname(__file__), "ImageAssets", "Login.jpg")

    Imaged = Image.open(img)
    Imaged = Imaged.resize((1020, 720), Image.LANCZOS)

    photo = ImageTk.PhotoImage(master=root,  image=Imaged)
    Wallp = tk.Label(GrandmaFrame, image=photo)
    Wallp.place(x=0, y=0, relwidth=1, relheight=1)
    Wallp.lower()


    Time = tk.Label(GrandmaFrame, text=f"{dt}", font="Comfortaa 50", bg= "Black", fg="White")
    DayDate = tk.Label(GrandmaFrame, text=f"{words_date}", font="Comfortaa 20", bg= "Black", fg="White")

    LoginBut = tk.Button(GrandmaFrame, text="Login", command=desktopFunc)

    DayDate.place(x=40,y=580)
    Time.place(x=40,y=500)
    #LoginBut.pack(side="bottom", anchor="se", padx=10, pady=10)
    for widget in (GrandmaFrame, Wallp, Time, DayDate):
        widget.bind("<Button-1>", lambda event: users())


    root.mainloop()

Startup()