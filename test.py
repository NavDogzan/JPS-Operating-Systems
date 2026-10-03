'''def mp3():

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



    mp3Closebtn = tk.Button(frm,
                    text="X",
                    fg="Black", 
                    activebackground="red",
                    width=3, 
                    height=1,
                    )
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
    

    app() '''