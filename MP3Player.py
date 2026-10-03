from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import customtkinter as ctk
import pygame as py
from mutagen.mp3 import MP3
from pathlib import Path

py.mixer.init()
pysound  = py.mixer

MusicTheme = "#3f3f3f"
BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "Album_Miscs"
MUSIC_DIR = BASE_DIR / "Music Assets"
USER_DIR = BASE_DIR / "User"



class Player(Frame):
    def __init__(self,parent):
        super().__init__(parent)

        
        
        self.config(width=640,height=420)
        self.propagate(False)


        self.playstate = False

        

        self.globalsongs = ['Bohemian Rhapshody','Here Comes The Sun','Fly Me To The Moon','Duvet','Red Swan', "Hyouriittai","For The First Time","In The Pool"]
        self.userprefernce = {'Bohemian Rhapshody':["#9c4ca3",'BR.png','song1.mp3', 'Queen',0],
                              'Here Comes The Sun':["#d8b45b",'B1.png','Here Comes The Sun.mp3', 'The Beatles',0],
                              'Fly Me To The Moon':["#4CB1A1",'FLM.jfif','FLM.mp3', 'Megumi Hayashibara',0],
                              'Duvet':["#802929",'duvet.png','Duvet.mp3','boa',0],
                              'Red Swan':["#C4BF81",'Aot.jpg','Aot1.mp3', 'YOSHIKI ft. HYDE', 4],
                              'Hyouriittai':["#B9EBFA",'HYU.jfif','Hyouriittai.mp3', 'YUZU', 0],
                              'For The First Time':["#FCE272",'ForFirst.jfif','For the First Time.mp3', 'Mac DeMarco', 0],
                              'In The Pool':["#4E4C57",'inpool.jpg','in the pool.mp3', 'kensuke ushio', 0],
                              }
        self.songqueue = []
        self.songindex = 0

        self.Mainframe = Frame(self, bg=MusicTheme,borderwidth=2,relief=RIDGE)
        self.Mainframe.pack(fill='both',expand=True)

        self.LeftFrame = Frame(self.Mainframe, bg=MusicTheme,width=320)
        self.RightFrame = Frame(self.Mainframe, bg=MusicTheme,width=320)
        self.LeftFrame.propagate(False)
        self.Playlist_button = Button(self.Mainframe, height=1,text="My playlist",bg='#3f3f3f',fg='white',command=self.openplylist)
        self.Playlist_button.pack(side='top',fill='x',padx=2,pady=2)

        self.Music_play_frame = Frame(self.LeftFrame, bg=MusicTheme, height=250,borderwidth=2,relief=SUNKEN,width=320)
        self.Music_play_frame.propagate(False)
        self.Music_play_header = Label(self.LeftFrame, text = f'playing from ...',bg=MusicTheme,font=("Arial", 10, "bold"))
        self.control_frame = Frame(self.LeftFrame, bg=MusicTheme, height=200, borderwidth=2, relief=SUNKEN,width=320)


        self.MiscFrame = Frame(self.RightFrame,bg=MusicTheme, height=420,borderwidth=2,relief=SUNKEN,width=320)
        self.base_vinyl_image = Image.open(IMAGE_DIR / 'Vinyl.png').convert("RGBA")
        self.base_vinyl_image = self.base_vinyl_image.resize((140, 140), Image.Resampling.LANCZOS)

        self.AlbumCoverFrame = Frame(self.Music_play_frame, height=155,width=155,bg='black',borderwidth=5,relief=RIDGE)
        self.AlbumCoverFrame.propagate(False)
        self.AlbumCoverLabel = Label(self.AlbumCoverFrame,bg="#505052")

        self.Vinylimage = self.base_vinyl_image.copy()
        self.Vinylphoto = ImageTk.PhotoImage(self.Vinylimage, master=self)

        self.A1image = Image.open(IMAGE_DIR / 'A1_.png')
        self.A1image = self.A1image.resize((300,300), Image.Resampling.LANCZOS)
        self.A1photo = ImageTk.PhotoImage(self.A1image, master=self)
        self.A2image = Image.open(IMAGE_DIR / 'A2_.png')
        self.A2image = self.A2image.resize((300,300), Image.Resampling.LANCZOS)
        self.A2photo = ImageTk.PhotoImage(self.A2image, master=self)

        #self.TokitoLabel = Label(self.MiscFrame,height=300,width=300,image=self.A1photo,anchor='e',bg=MusicTheme)
        #self.TokitoLabel.propagate(False)
        self.MiscFrame.propagate(False)

        self.VinylFrame = Frame(self.Music_play_frame, width=140,height=140,bg=MusicTheme)
        self.VinylFrame.propagate(False)
        self.VinylLabel = Label(self.VinylFrame, image=self.Vinylphoto,bg=MusicTheme)

        self.infoFrame = Frame(self.Music_play_frame, bg=MusicTheme,width=220,height=58)
        self.infoFrame.propagate(False)
        self.Songname = Label(self.infoFrame, text="...",width=50,height=1, bg=MusicTheme,borderwidth=2,relief=RIDGE,font=("Arial",10,"bold"))
        self.Artistname = Label(self.infoFrame, text="Boa",width=25,bg=MusicTheme)

        self.slider_width = 300
        self.BaseSlider = Frame(self.control_frame, bg="#707070",width=self.slider_width,relief=SUNKEN,height=15,borderwidth=2)
        self.fillerFrame = Frame(self.BaseSlider,height=1)
        self.TimeFrame = Frame(self.control_frame,width=300,height=15,bg=MusicTheme)
        self.TotalTimeLabel = Label(self.TimeFrame,text="00:00",bg=MusicTheme)
        self.CurrentTimeLabel = Label(self.TimeFrame,text='00:00',bg=MusicTheme)

        self.ControlBtnsFrame = Frame(self.control_frame, bg=MusicTheme)

        self.UpcomingFrame = Frame(self.MiscFrame,height=100,)
        
        self.StartBtnimg = Image.open(IMAGE_DIR / 'start.png')
        self.StartBtnimg = self.StartBtnimg.resize((50,50), Image.Resampling.LANCZOS)
        self.StartBtnphto = ImageTk.PhotoImage(self.StartBtnimg, master=self)

        self.PauseBtnimg = Image.open(IMAGE_DIR / 'stop.png')
        self.PauseBtnimg = self.PauseBtnimg.resize((50,50), Image.Resampling.LANCZOS)
        self.PauseBtnphoto = ImageTk.PhotoImage(self.PauseBtnimg, master=self)

        self.StartStopBtn = ctk.CTkButton(self.ControlBtnsFrame,text='II',width=50,height=50,corner_radius=100,fg_color='White',text_color="Black",command = self.Pause_music)
        self.NextR = ctk.CTkButton(self.ControlBtnsFrame,text=">",height=50,width=50,command=lambda:self.next_song(1),fg_color='white', text_color='Black',corner_radius=100)
        self.NextL = ctk.CTkButton(self.ControlBtnsFrame,text="<",height=50,width=50, command=lambda:self.next_song(-1),fg_color='white', text_color='Black',corner_radius=100)

        self.LeftFrame.pack(side="left",fill='y')
        self.RightFrame.pack(side="right",fill='y')
        self.Music_play_frame.pack(side='top',fill='x',padx=3,pady=3)
        #self.Music_play_header.pack(side='top',fill='x',padx=5,pady=5)
        self.control_frame.pack(side='top',fill='x',padx=3,pady=(3,5))
        self.VinylFrame.place(x=200, y=100, anchor='center')
        self.VinylLabel.pack(fill='both', expand=True)
        self.MiscFrame.pack(side='top',fill='y',padx=3,pady=(3,5))
        #self.TokitoLabel.place(x=100,y=100)


        self.AlbumCoverFrame.place(x=110,y=100,anchor='center')
        self.AlbumCoverLabel.pack(fill='both',expand=True)
        self.AlbumCoverFrame.lift()

        self.infoFrame.place(relx=0.5,y=215,anchor='center')
        self.Songname.pack(side='top')
        self.Artistname.pack(side='top')

 
        self.control_frame.propagate(False)
        self.BaseSlider.pack(side='top',pady=10)
        self.fillerFrame.place(x=0,y=0)
        for slider_widget in (self.BaseSlider, self.fillerFrame):
            slider_widget.bind("<Button-1>", self.seek_music)
            slider_widget.bind("<B1-Motion>", self.seek_music)

        self.TimeFrame.propagate(False)
        self.TimeFrame.pack(side='top')
        self.TotalTimeLabel.pack(side='right')
        self.CurrentTimeLabel.pack(side="left")

        self.ControlBtnsFrame.pack(side='bottom',pady=10)
        self.NextR.pack(side='right',pady=5)
        self.StartStopBtn.pack(side='right',padx=10)
        self.NextL.pack(side='right',pady=5)

        self.CurrentLength = 0 
        self.CurrentTime = 0   
        self.playback_offset = 0
        self.slider_after = None
        self._is_closing = False
        self._scheduled_afters = set()
        self.tokito = True

        self.current_theme = MusicTheme
        self.songPlaying = False
        self.angle = 0
        self.spin_speed = 0
        self.spinVinyl()
        #self.animate_mascot()
        self.check_music()
    
    def upcoming_music(self):pass

    def schedule_after(self, delay, callback, *args):
        callback_id = None

        def run_callback():
            self._scheduled_afters.discard(callback_id)
            if not self._is_closing:
                callback(*args)

        callback_id = self.after(delay, run_callback)
        self._scheduled_afters.add(callback_id)
        return callback_id

    def cancel_scheduled_after(self, callback_id):
        if callback_id:
            try:
                self.after_cancel(callback_id)
            except TclError:
                pass
            self._scheduled_afters.discard(callback_id)

    def shutdown(self):
        self._is_closing = True
        for callback_id in tuple(self._scheduled_afters):
            self.cancel_scheduled_after(callback_id)
        pysound.music.stop()

    '''def animate_mascot(self):
        if self.songPlaying:
            if self.tokito:
                self.TokitoLabel.config(image=self.A1photo)
            else:
                self.TokitoLabel.config(image=self.A2photo)

            self.tokito = not self.tokito

        self.after(1000, self.animate_mascot)'''

        
    def update_slider(self):
        if not self.songqueue or self.CurrentLength <= 0:
            return
        position = pysound.music.get_pos() / 1000
        self.CurrentTime = self.playback_offset + position

        if self.CurrentTime > self.CurrentLength:
            self.CurrentTime = self.CurrentLength

        progress = self.CurrentTime / self.CurrentLength
        width = int(self.slider_width * progress)

        self.fillerFrame.config(width=width,height=12,bg=self.current_theme)

        minutes = int(self.CurrentTime // 60)
        seconds = int(self.CurrentTime % 60)

        total_minutes = int(self.CurrentLength // 60)
        total_seconds = int(self.CurrentLength % 60)

        self.TotalTimeLabel.config(text=f"{total_minutes}:{total_seconds:02d}")
        self.CurrentTimeLabel.config(text=f"{minutes}:{seconds:02d}")

        self.slider_after = self.schedule_after(16, self.update_slider)

    def seek_music(self, event):
        if not self.songqueue or self.CurrentLength <= 0:
            return

        slider_x = event.x_root - self.BaseSlider.winfo_rootx()
        progress = max(0, min(1, slider_x / self.slider_width))
        seek_time = min(progress * self.CurrentLength, max(0, self.CurrentLength - 0.1))
        was_playing = self.songPlaying

        self.playback_offset = seek_time
        self.CurrentTime = seek_time
        pysound.music.play(start=seek_time)
        if not was_playing:
            pysound.music.pause()
    
    def animate_color(self, old_color, new_color, step=0):
        steps = 10

        old_rgb = self.winfo_rgb(old_color)
        new_rgb = self.winfo_rgb(new_color)

        old_rgb = tuple(x // 257 for x in old_rgb)
        new_rgb = tuple(x // 257 for x in new_rgb)

        progress = step / steps

        progress = progress * progress * (3 - 2 * progress)

        rgb = tuple(
            int(old_rgb[i] + (new_rgb[i] - old_rgb[i]) * progress)
            for i in range(3)
        )

        color = "#%02x%02x%02x" % rgb
        widgets = [self.Playlist_button,self.Mainframe,self.LeftFrame,self.Music_play_frame,self.Music_play_header,
                   self.VinylLabel,self.control_frame,self.Artistname,self.Songname,
                   self.infoFrame,self.ControlBtnsFrame,self.TimeFrame,self.CurrentTimeLabel,self.TotalTimeLabel,
                   self.RightFrame,self.MiscFrame]#self.TokitoLabel
        pl = getattr(self, 'playlistapp', None)
        if pl:
            widgets += pl.themed_widgets()

        for w in widgets:
            try:
                w.config(bg=color)
            except TclError: 
                pass
        
        self.Playlist_button.config(bg=color,fg="black",relief=RAISED,borderwidth=2)


        if step < steps:
            self.schedule_after(15, self.animate_color, old_color, new_color, step + 1)
    
    def Pause_music(self):
        if not self.songPlaying:
            pysound.music.unpause()
            self.songPlaying = True
            self.StartStopBtn.configure(text='II')
        else:
            pysound.music.pause()
            self.songPlaying = False
            self.StartStopBtn.configure(text=">")

    def load_music(self):
        if not self.songqueue:return
        if self.slider_after:
            self.cancel_scheduled_after(self.slider_after)
            self.slider_after = None



        self.song = self.songqueue[self.songindex]
        self.musicfile = str(MUSIC_DIR / self.userprefernce[self.song][2])
        self.CurrentAlbum = IMAGE_DIR / self.userprefernce[self.song][1]

        self.CurrentLength = MP3(self.musicfile).info.length
        self.playback_offset = self.userprefernce[self.song][4]
        self.CurrentTime = self.playback_offset

        new_theme = self.userprefernce[self.song][0]

        self.animate_color(
            self.current_theme,
            new_theme
        )
        

        self.current_theme = new_theme
        self.Albumimage = Image.open(self.CurrentAlbum)
        self.Albumimage.thumbnail((150, 150), Image.Resampling.LANCZOS)

        self.Albumphoto = ImageTk.PhotoImage(self.Albumimage, master=self)
        self.AlbumCoverLabel.config(image=self.Albumphoto)

        self.Songname.config(text=self.song)
        self.Artistname.config(text=self.userprefernce[self.song][3])

        vinyl_image = self.base_vinyl_image.copy()

        cover_size = 45
        cover = Image.open(self.CurrentAlbum).convert("RGBA")
        vinyl_cover = cover.resize(
            (cover_size, cover_size),
            Image.Resampling.LANCZOS
        )

        vinyl_cover_mask = Image.new("L", (cover_size, cover_size), 0)
        ImageDraw.Draw(vinyl_cover_mask).ellipse(
            (0, 0, cover_size - 1, cover_size - 1),
            fill=255
        )
        vinyl_cover.putalpha(vinyl_cover_mask)

        vinyl_image.alpha_composite(vinyl_cover, (47, 47))
        self.Vinylimage = vinyl_image

        self.Vinylphoto = ImageTk.PhotoImage(self.Vinylimage, master=self)
        self.VinylLabel.config(image=self.Vinylphoto)
        
        
        

        pysound.music.load(self.musicfile)



        pysound.music.play(start=self.playback_offset)
        self.songPlaying = True

        self.update_slider()


       
        print("Playing:", self.song)

    def next_song(self,j):
        if not self.songqueue:return

        self.songindex += j

        if self.songindex >= len(self.songqueue):
            self.songindex = 0

        self.load_music()

    def check_music(self):
        if self.songqueue and not pysound.music.get_busy() and self.songPlaying:
                self.next_song(1)
        self.schedule_after(500, self.check_music)

    def spinVinyl(self):

        if self.songPlaying:
            self.spin_speed += (2 - self.spin_speed) * 0.15
        else:
            self.spin_speed *= 0.90
            if self.spin_speed < 0.05:
                self.spin_speed = 0

        if self.spin_speed > 0:
            rotated = self.Vinylimage.rotate(self.angle,resample=Image.Resampling.BICUBIC,expand=False)

            self.Vinylphoto = ImageTk.PhotoImage(rotated, master=self)
            self.VinylLabel.config(image=self.Vinylphoto)

            self.angle = (self.angle + self.spin_speed) % 360

        self.schedule_after(40, self.spinVinyl)

    def openplylist(self):
        self.playstate = not self.playstate

        if self.playstate:
            self.playlistapp = playlist(self.MiscFrame, self)

        else:
            self.playlistapp.f.destroy()
            self.playlistapp = None

class playlist(Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app 
        self.New_playliststate = False
        self.AllSongState = False

        theme = self.app.current_theme
        self.f = Frame(parent, bg=theme,width=317,height=410,borderwidth=2,relief=RIDGE)
        self.f.propagate(False)
        self.label = Label(self.f, text="Playlist",bg=theme,fg="White")
        self.playlistbox = Listbox(self.f, bg="#CECECE",width=20,height=10,borderwidth=2,relief=SUNKEN)

        self.BtnFrame = Frame(self.f,height=50,bg=theme)
        self.add_playlist_btn = Button(self.BtnFrame, text="+",command=self.New_playlist)
        self.allsongs_btn = Button(self.BtnFrame, text="All songs",command=self.All_songs)
    
         
        self.label.pack(side='top',padx=5,pady=5)
        self.playlistbox.pack(side='top',fill='x',padx=10,pady=5)
        self.BtnFrame.pack(side='top',fill="x")
        self.add_playlist_btn.pack(side='right',padx=5,pady=5)
        self.allsongs_btn.pack(side='left',pady=15,padx=5)
        
        #
        self.f.pack(fill='both',padx=1,pady=1) 
        self.PlaylistDict={}

        self.load_playlist(self.PlaylistDict)

        for songs in self.PlaylistDict:
            self.playlistbox.insert(END,songs)

        self.playlistbox.bind('<<ListboxSelect>>', self.Update_player)    
    
    def All_songs(self):
        theme = self.app.current_theme
        self.f3 = Frame(self.f,height=405,width=310,relief=RIDGE,borderwidth=3,bg=theme)
        self.f3.propagate(False)
        self.f3header = Label(self.f3,text='All Songs',bg=theme)
        self.f3BOX = ctk.CTkScrollableFrame(self.f3,width=300,height=200,fg_color="#e2e2e2")
        #self.f3Box = Listbox(self.f3, width=25,height=5)
        
        self.EditorFrame = Frame(self.f3,height=50,relief=RIDGE,borderwidth=4,bg=theme)
        self.BackBtn = Button(self.f3,text='Back',command=self.Misc)
        self.songLIST = []
        self.song_photos = []
        #'Red Swan':["#C4BF81",'Aot.jpg','Aot1.mp3', 'YOSHIKI ft. HYDE', 100
        
        for name,data in self.app.userprefernce.items():
            self.frame = Frame(self.f3BOX, height=50,bg=data[0])
            self.frame.propagate(False)
            
            self.A1image = Image.open(IMAGE_DIR / data[1])
            self.A1image = self.A1image.resize((50,50), Image.Resampling.LANCZOS)
            self.A1photo = ImageTk.PhotoImage(self.A1image, master=self.app)
            self.song_photos.append(self.A1photo)
            
            self.songlabel = Label(self.frame, text="img",bg=data[0],relief=RAISED,borderwidth=2,width=50,height=50,image=self.A1photo,)
            self.button = Button(self.frame,text=f"{name}\n{data[3]}",bg=data[0],width=80,command=lambda n=name: self.play_single(n))

            self.frame.pack(side='top',fill='x',pady=2)
            self.songlabel.pack(side='left')
            self.button.pack(side='right',fill='both')
            self.songLIST.append(self.frame)


        #for songs in self.app.globalsongs:
            #self.f3Box.insert(END, songs)
      
        self.f3header.pack(side='top',pady=(20,5))
        self.f3BOX.pack(side='top',padx=5,pady=5)
        #self.f3Box.pack(side='top',pady=5,padx=5)
        self.EditorFrame.pack(side='top',pady=5,padx=5,fill='x')
        self.BackBtn.pack(side='top',pady=5,padx=5)

        if not self.AllSongState:
            self.f3.place(relx=0.5,rely=0.5,anchor='center')
            self.AllSongState = True
    
    def play_single(self, name):
        self.app.songqueue = [name]
        self.app.songindex = 0
        self.app.Playlist_button.config(text=name)

        self.app.load_music()     

        self.f.destroy()          
        self.app.playlistapp = None
        self.app.playstate = False
    def Misc(self):
        self.AllSongState= False
        self.f3.destroy()
    def Update_player(self,event):
        self.selecten = self.playlistbox.curselection()

        if self.selecten:
            playlist_name = self.playlistbox.get(self.selecten[0])
            self.app.songqueue = self.PlaylistDict[str(playlist_name)]
            self.app.songindex = 0
            print("Queue:", self.app.songqueue)




            self.app.Playlist_button.config(text=f"{playlist_name}")

            self.app.load_music()
            self.f.destroy()
            self.app.playlistapp = None

            self.app.playstate = False

    def themed_widgets(self):
        ws = [self.f, self.label, self.BtnFrame]
        for name in ('f1', 'f1header', 'f2', 'f2header', 'boxframe', 'f3', 'f3header','BtnFrame','f3'):
            w = getattr(self, name, None)
            try:
                if w is not None and w.winfo_exists():
                    ws.append(w)
            except TclError:
                pass
        return ws  
    
    def load_playlist(self, PlaylistDict):
        self.file = open(USER_DIR / 'j.txt', 'r')
        self.a = self.file.read().strip()
        self.PlaylistDict = eval(self.a) if self.a else {}
        self.file.close()

    def New_playlist(self):
        
        #
        self.f1 = Frame(self.f,width=200,height=100,borderwidth=2,relief=RIDGE)
        self.f1.propagate(False)
        #
        self.f1header = Label(self.f1, text='create new playlist')
        self.Playlist_name = Entry(self.f1, width=30,bg="#b8b7b7")
        self.Save_btn = Button(self.f1,text='create', command=self.select_newsong)

        self.f1header.pack(side='top',padx=5,pady=5)
        self.Playlist_name.pack(side='top',padx=5,pady=5)
        self.Save_btn.pack(side='top',padx=5,pady=5)

        if not self.New_playliststate:
            self.f1.place(relx=0.5,rely=0.5,anchor='center')
            self.New_playliststate = not self.New_playliststate

    def select_newsong(self):

        self.name = self.Playlist_name.get()
        
        try:self.f1.destroy() 
        except:pass

        self.f2 = Frame(self.f,width=500,height=220, borderwidth=2,relief=RIDGE)
        self.f2.propagate(True)
        self.boxframe = Frame(self.f2,height=200,width=300)

        self.f2header = Label(self.f2, text=f"select songs for {self.name}")

        self.songbox = Listbox(self.boxframe, width=20,height=7)
        self.selected = Listbox(self.boxframe,width=20,height=7,bg="#ADADAD",relief=SUNKEN)

        self.createbtn = Button(self.f2, text='create', command = lambda: self.save_playlist(self.name, self.d1),width=8)

        for songs in self.app.globalsongs:
            self.songbox.insert(END, songs)

        self.f2.place(relx=0.5,rely=0.5,anchor='center')
        self.f2header.pack(side='top',padx=5,pady=5)
        self.boxframe.pack(side='top',padx=2,pady=5)
        self.songbox.pack(side='left',padx=5,pady=5)
        self.selected.pack(side='left',padx=5,pady=5)
        self.createbtn.pack(side='top',padx=5,pady=5)

        self.d1 = []

        self.songbox.bind("<<ListboxSelect>>", self.add_selected)
        self.selected.bind("<<ListboxSelect>>", self.remove_selected)

    def add_selected(self,event):
        self.selecten = self.songbox.curselection()
        if self.selecten:
            self.selected.insert(END, self.songbox.get(self.selecten[0]))
            self.d1.append(str(self.songbox.get(self.selecten[0])))
            print(self.d1)
            self.songbox.delete(self.selecten[0])
    def remove_selected(self,event):
        self.selecten = self.selected.curselection()
        if self.selecten:
            song = self.selected.get(self.selecten[0])
            self.songbox.insert(END, song)
            self.d1.remove(song)
            print(self.d1)
            self.selected.delete(self.selecten[0])

    def save_playlist(self,d,d1):

        self.PlaylistDict[d] = d1

        self.file = open(USER_DIR / 'j.txt', 'w')
        self.file.write(str(self.PlaylistDict))
        self.file.close()

        self.playlistbox.delete(0, END)

        for playlist_name in self.PlaylistDict:
            self.playlistbox.insert(END, playlist_name)

        try:
            self.f2.destroy()
        except:
            pass   
        self.New_playliststate=False    
            

