
from tkinter import *
import customtkinter as ctk
import ast
import os

path = Note_1_path = os.path.join(os.path.dirname(__file__), "User","JPS Notes", "Note.txt") 
lb = "light blue"

class Notes(Frame):
    def __init__(self,parent): #parent
        super().__init__(parent) 

        self.config(width=520,height=320)

        self.Mainframe = Frame(self, bg='Light blue')
        self.rightframe = Frame(self.Mainframe, width=160,relief=SUNKEN,borderwidth=2,bg='light blue')
        self.leftframe = Frame(self.Mainframe, width=340, relief=SUNKEN,borderwidth=2,bg='light blue')
        
        self.header = Label(self.rightframe, text="JPS NOTES",font="Roman 18 bold underline",bg=lb)
        self.desc1 = Label(self.rightframe, text="Write and save notes,", font=("Arial", 10), bg="Light blue")
        self.desc2 = Label(self.rightframe, text="Click on a note to open it", font=("Arial", 10), bg="Light blue")
        self.scroll = ctk.CTkScrollableFrame(self.leftframe, fg_color="Light blue",height=200,scrollbar_button_color='#66abc7')
        self.testTEXT = Text(self.rightframe)
        self.AddBTN = Button(self.rightframe,text="+",font="Arial",width=2,bg=lb,command=self.add_note)
          
        propagation = [self.Mainframe,self.rightframe,self.leftframe]
        for widgets in propagation:
            widgets.propagate(False)

        self.Notes = {}

        self.Mainframe.pack(fill='both',expand=True)
        self.leftframe.pack(side='left',fill='y',padx=5,pady=5)
        self.rightframe.pack(side='right',fill='y',padx=5,pady=5)
        self.AddBTN.pack(side='bottom',anchor="e",padx=5,pady=5)

        self.header.pack(side='top',pady=5)
        self.desc1.pack(side='top')
        self.desc2.pack(side='top')
        self.scroll.pack(side='top',fill='both',padx=0,pady=0,expand=True)
        #self.testTEXT.pack(side='top',fill='both',padx=5,pady=5,expand=True)

        self.load_notes()
        #self.testTEXT.insert(1.0,self.Notes['Reminder'][0])
        
        self.Notebtns = []
        for name,data in self.Notes.items():
            button = Button(self.scroll,text=name,height=3,command=lambda n=name: self.open_note(n),borderwidth=5,relief=RIDGE)
            button.pack(side='top',fill='x',padx=5,pady=2)
            self.Notebtns.append(button)
    def add_note(self):
        self.gaaa = Frame(self.Mainframe,width=200,height=100,bg=lb,borderwidth=2,relief=RIDGE)
        self.header = Label(self.gaaa, text='New note name',bg=lb)
        self.newnotename = Entry(self.gaaa)
        self.crt_btn = Button(self.gaaa,text='Create',command=self.create_note)
        self.cancel_btn = Button(self.gaaa,text='<',command=self.gaaa.destroy)
        self.gaaa.propagate(False)

        self.header.pack(side='top',pady=5)
        self.newnotename.pack(side="top",pady=5)
        self.crt_btn.place(relx=0.5,y=80,anchor='center')
        self.cancel_btn.pack(side='left',padx=5,pady=5)
        self.gaaa.place(relx=0.5,rely=0.5,anchor='center')
        self.newnotename.bind('<Return>',lambda event: self.create_note())
        self.newnotename.focus_set()

    def create_note(self):
        name = self.newnotename.get().strip()
        if not name:
            print("empty")
            return
        if name in self.Notes:
            print("Already exists")
            return

        self.Notes = {name: ["", lb], **self.Notes}
        with open(path, 'w', encoding='utf-8') as note_file:
            note_file.write(repr(self.Notes))

        self.gaaa.destroy()
        self.refresh_note_buttons()
        self.open_note(name)

    def refresh_note_buttons(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()
        self.Notebtns = []
        for name in self.Notes:
            button = Button(self.scroll, text=name, height=3, command=lambda n=name: self.open_note(n))
            button.pack(side='top', fill='x', padx=5, pady=2)
            self.Notebtns.append(button)

        
    def load_notes(self):
        with open(path, 'r', encoding='utf-8') as note_file:
            note_data = note_file.read().strip()
        self.Notes = ast.literal_eval(note_data) if note_data else {}

    def open_note(self,notename):
        self.content = self.Notes[notename][0]
        self.theme = self.Notes[notename][1]

        self.oldname = notename
        self.newName = ''
        self.newtheme = ''
        
        self.NoteFrame = Frame(self.Mainframe,bg=self.theme,height=320,width=520,)

        self.HeaderFrame = Frame(self.NoteFrame,height=40,bg=self.theme,relief=SUNKEN,borderwidth=2)
        self.CotentFrame = Frame(self.NoteFrame,width=520,bg=self.theme,relief=SUNKEN,borderwidth=2)

        self.ControlsFrame = Frame(self.CotentFrame,width=80,bg=self.theme,relief=SUNKEN,borderwidth=2)
        
        self.NoteFrame.propagate(False)
        self.CotentFrame.propagate(False)
        self.ControlsFrame.propagate(False)

        self.Header = Entry(self.HeaderFrame,bg=self.theme,font=("Arial",12,"underline"),relief=FLAT,width=100)
        self.Header.insert(END,f"{notename}")
        
        self.SaveBtn = Button(self.ControlsFrame,text="Save",bg=self.theme,height=2,command=lambda: self.save_Note(self.Header.get(),
                                                                                                                   self.Text.get("1.0","end-1c"),
                                                                                                                   self.newtheme))
        self.BackBtn = Button(self.ControlsFrame,text="Back",bg=self.theme,height=2,command=lambda: self.NoteFrame.destroy())
        self.DeleteBtn = Button(self.ControlsFrame,text="Delete",bg=self.theme,height=2,command=self.delete_note)

        self.color_pallet = Frame(self.ControlsFrame,height=120)

        self.row1=Frame(self.color_pallet,width=80,height=40)
        self.color1=Button(self.row1,bg="#6059ee",width=3,relief=SUNKEN,borderwidth=1,command=lambda c="#6059ee":self.changecolor(c))
        self.color2=Button(self.row1,bg="#b99624",width=3,relief=SUNKEN,borderwidth=1,command=lambda c="#b99624":self.changecolor(c))
        
        self.row2=Frame(self.color_pallet,width=80,height=40)
        self.color3=Button(self.row2,bg="#ec7b4e",width=3,relief=SUNKEN,borderwidth=1,command=lambda c="#ec7b4e":self.changecolor(c))
        self.color4=Button(self.row2,bg="#cc4986",width=3,relief=SUNKEN,borderwidth=1,command=lambda c="#cc4986":self.changecolor(c))
        
        self.row3=Frame(self.color_pallet,width=80,height=40)
        self.color5=Button(self.row3,bg="#a4db4c",width=3,relief=SUNKEN,borderwidth=1,command=lambda c="#a4db4c":self.changecolor(c))
        self.color6=Button(self.row3,bg="#2cc0b9",width=3,relief=SUNKEN,borderwidth=1,command=lambda c="#2cc0b9":self.changecolor(c))
        
        self.Text = Text(self.CotentFrame,width=60,bg="#e9e8e8",font=("Arial",10))
        self.NoteFrame.place(relx=0.5,rely=0.5,anchor='center')
        
        self.HeaderFrame.pack(side='top',fill='x',padx=5,pady=(5,2))
        self.CotentFrame.pack(side='top',fill='y',padx=5,pady=(2,5),expand=True)
        self.Header.pack(side='top',pady=5,padx=5)
        #self.Savebutton.pack(side='top',pady=5,anchor='e')
        self.NoteFrame.lift()
        self.Text.pack(side='right',fill='y',padx=5,pady=5)
        self.ControlsFrame.pack(side='left',fill='y',padx=5,pady=5)

        self.SaveBtn.pack(side='top',padx=1,pady=1,fill='x')
        self.BackBtn.pack(side='top',padx=1,pady=1,fill='x')
        self.DeleteBtn.pack(side='bottom',padx=1,pady=2,fill='x')

        self.color_pallet.pack(side='bottom',fill='x')
        
        self.row1.pack(side='top')
        self.color1.pack(side='left')
        self.color2.pack(side="right")
        
        self.row2.pack(side='top')
        self.color3.pack(side='left')
        self.color4.pack(side="right")

        self.row3.pack(side='top')
        self.color5.pack(side='left')
        self.color6.pack(side="right")

        self.Text.insert(1.0, self.content)
        self.Header.bind("<Return>",lambda event: self.changename(self.Header.get()))
    
    def changename(self,Newname):
        self.newName = Newname
        print(self.newName)
    
    def save_Note(self,NoteName,Content,Color):
        new_name = NoteName.strip()
        if not new_name:
            print("Empty Name")
            return
        if new_name != self.oldname and new_name in self.Notes:
            print("Name already exists")
            return
          
        color = Color or self.theme
        self.Notes.pop(self.oldname)
        self.Notes = {new_name: [Content, color], **self.Notes}

        with open(path, 'w', encoding='utf-8') as note_file:
            note_file.write(repr(self.Notes))

        self.oldname = new_name
        self.theme = color
        self.newtheme = ""
        self.refresh_note_buttons()

    def delete_note(self):
        self.DeleteConfirm = Frame(self.Mainframe, width=240, height=110, bg=lb,
                                   borderwidth=2, relief=RIDGE)
        self.DeleteConfirm.propagate(False)
        Label(self.DeleteConfirm, text=f'Delete "{self.oldname}"?', bg=lb).pack(pady=(18, 10))

        buttons = Frame(self.DeleteConfirm, bg=lb)
        buttons.pack()
        Button(buttons, text="Yes", width=8, command=self.confirm_delete).pack(side='left', padx=5)
        Button(buttons, text="No", width=8, command=self.cancel_delete).pack(side='left', padx=5)

        self.DeleteConfirm.place(relx=0.5, rely=0.5, anchor='center')
        self.DeleteConfirm.lift()
        self.DeleteConfirm.grab_set()

    def cancel_delete(self):
        self.DeleteConfirm.grab_release()
        self.DeleteConfirm.destroy()

    def confirm_delete(self):
        self.DeleteConfirm.grab_release()
        self.DeleteConfirm.destroy()

        self.Notes.pop(self.oldname, None)
        with open(path, 'w', encoding='utf-8') as note_file:
            note_file.write(repr(self.Notes))

        self.NoteFrame.destroy()
        self.refresh_note_buttons()

    def changecolor(self,c):
        self.widgets=[self.SaveBtn, self.BackBtn, self.DeleteBtn, self.ControlsFrame,self.Header,self.CotentFrame,self.HeaderFrame, self.NoteFrame]
        self.newtheme = c
        for i in self.widgets:
            i.config(bg=c)


