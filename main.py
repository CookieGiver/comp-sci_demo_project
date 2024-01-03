from doctest import master
import tkinter as tk
import customtkinter
import math
from ctypes import windll
import time
from PIL import Image
import json

from flashcards import Flashcards
from exam import Exam

main_color = '#FAA916'
hover_color = '#C47C18'

root = tk.Tk()
windll.shcore.SetProcessDpiAwareness(1)

screen_dim = (root.winfo_screenwidth(), root.winfo_screenheight())
screen_size = f'{int(screen_dim[0])}x{int(screen_dim[1])}'
root.geometry(screen_size)
root.configure(background='white')

class Pack(customtkinter.CTkButton):
    def __init__(self, master, home, title, vocab):
        super().__init__(
            master, 
            width=430, 
            height=250, 
            corner_radius=15, 
            text=title, 
            text_color='white', 
            fg_color=main_color, 
            hover_color=hover_color, 
            font=('Lato', 20, 'bold'), 
            command=self.btn_press
            )
        
        self.home = home
        self.title = title
        self.vocab = vocab

    def btn_press(self):
        self.home.destroy()
        vocab_page = VocabPack(root=root, title=self.title)
        vocab_page.packWords()
        root.update()


class Home(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg='white')

        with open("vocabulary.json",) as f:
            self.vocab = json.load(f)

        self.grid = []
        self.pack_btn_list = []

        # Create rows to pack vocabulary packs into
        for i in range(math.ceil((len(self.vocab.keys())+1)/3)):
            self.grid.append(tk.Frame(self, width=20, height=20, bg='white'))

        # Add vocab packs to corresponding rows 3-wide
        for i, pack in enumerate(self.vocab.keys()):
            self.pack_btn_list.append(Pack(self.grid[int(i/3)], home=self, title=pack, vocab=self.vocab[pack]))

        self.new_pack_btn = customtkinter.CTkButton(
            self.grid[-1], 
            width=430, 
            height=250, 
            corner_radius=15, 
            text="➕", 
            text_color='white', 
            fg_color='#6D676E', 
            hover_color='#2e2e2e', 
            font=('Lato', 80, 'bold'),
            command=self.initialize_pack)
        
        self.pack_btn_list.append(self.new_pack_btn)
        
    def pack_lists(self):
        for i, pack in enumerate(self.pack_btn_list):
            if i%3 == 0:
                pack.pack(side=tk.LEFT, padx=5)
            elif i%3 >= 1:
                pack.pack(side=tk.RIGHT, padx=5)

        for row in self.grid:
            row.pack(pady=8)

        super().pack()

    def initialize_pack(self):
        self.name_label = tk.Label(root, text="Name of New Pack", bg='white', font=('Lato', 30, 'bold'))
        self.name_label.place(x=800, y=600)
        self.name_entry = customtkinter.CTkEntry(
            root, 
            width=700, 
            height=60, 
            border_color=main_color, 
            bg_color='white', 
            font=('Lato', 20, 'bold')
            )
        self.name_entry.place(x=520, y=450)
        self.name_entry.bind('<Return>', self.create_pack)
        self.destroy()

    def create_pack(self, e):
        # e is a blank variable to accept extra information sent by 'bind' method
        self.new_title = self.name_entry.get()
        with open("vocabulary.json", "r+") as f:
            vocab = json.load(f)
            vocab[self.new_title] = {}

        with open("vocabulary.json", "w") as f:
            json.dump(vocab, f)

        vocab_page = VocabPack(root=root, title=self.new_title)
        vocab_page.packWords()

        self.name_label.destroy()
        self.name_entry.destroy()


class VocabWord(customtkinter.CTkButton):
    def __init__(self, row, column, padx, pady, sticky, *args, **kwargs):
        super().__init__(*args, **kwargs, command=self.edit)
        self.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

        self.row = row
        self.column = column

        if column == 0:
            self.del_btn = customtkinter.CTkButton(
                master=self.master,
                text="x",
                width=30,
                height=40,
                fg_color='#f77260',
                hover_color='#e68477',
                border_width=2,
                corner_radius=20,
                font=('Lato', 15, 'bold'),
                command=self.delete
            )
            self.del_btn.grid(row=self.row, column=2, padx=20)
    
    def delete(self):
        self.master.word_btns.remove(self)
        self.master.def_btns.remove(self.master.grid_slaves(row=self.row, column=1)[0])

        self.master.grid_slaves(row=self.row, column=1)[0].destroy()
        self.destroy()
        self.del_btn.destroy()

    def edit(self):
        self.configure(state="disabled")

        self.word_str_var = tk.StringVar()
        self.word_entry = customtkinter.CTkEntry(
            master=self.master,
            textvariable=self.word_str_var, 
            width= 300 if self.cget('width') == 300 else 850,
            height=70,
            corner_radius = 15,
            font=('Lato', 20, 'bold'))
        self.word_entry.grid(row=self.row, column=self.column, padx=60 if self.grid_info()["padx"] > 0 else 0, pady=10, sticky='we')
        print(self.word_entry.grid_info()["padx"])
        self.word_entry.insert(tk.END, self.cget('text'))

        self.word_entry.bind('<Return>', command=self.disableEntry)

    def disableEntry(self, e):
        self.word_entry.destroy()
        self.configure(text=self.word_str_var.get())
        self.configure(state="normal")


class VocabPack(tk.Frame):
    def __init__(self, root, title):
        super().__init__(root, bg='white')

        self.root = root
        self.title = title

        self.back_btn = customtkinter.CTkButton(
            master=self.root, 
            text="🢀",
            width=40,
            height=50,
            text_color='white',
            fg_color=main_color,
            hover_color=hover_color,
            border_width=2,
            border_color='black',
            corner_radius=20,
            font=('Lato', 30, 'bold'),
            anchor='center',
            command=self.go_home
            )
        self.back_btn.place(x=50, y=40)

        self.header = tk.Label(
            master=self,
            text=self.title,
            fg='black',
            bg='white',
            font=('Lato', 50, 'bold')
        )
        self.header.grid(row=0, column=0, padx=80, pady=15, sticky='nw')

        # quizzing options
        self.quiz_options = []

        flashcard_img_PIL = Image.open("icons/flashcards.png")
        flashcard_img = customtkinter.CTkImage(light_image=flashcard_img_PIL, size=(100, 100))

        test_img_PIL = Image.open("icons/test.png")
        test_img = customtkinter.CTkImage(light_image=test_img_PIL, size=(100, 100))

        writing_img_PIL = Image.open("icons/write.png")
        writing_img = customtkinter.CTkImage(light_image=writing_img_PIL, size=(100, 100))

        self.quiz_options = [
            customtkinter.CTkButton(
                master=root, 
                text="",
                image=flashcard_img,
                fg_color=main_color,
                hover_color=hover_color,
                width=200,
                height=200,
                corner_radius=30,
                border_width=4,
                command=self.flashcards
                ),
            customtkinter.CTkButton(
                master=root, 
                text="",
                image=writing_img,
                fg_color=main_color,
                hover_color=hover_color,
                width=200,
                height=200,
                corner_radius=30,
                border_width=4
                ),
            customtkinter.CTkButton(
                master=root, 
                text="",
                image = test_img,
                fg_color=main_color,
                hover_color=hover_color,
                width=200,
                height=200,
                corner_radius=30,
                border_width=4,
                command=self.exam
                )
        ]

        self.quiz_options[0].place(x=1400, y=80)
        self.quiz_options[1].place(x=1400, y=320)
        self.quiz_options[2].place(x=1400, y=560)

        # save vocabulary in 'vocabulary.json' file
        with open("vocabulary.json", "r+") as f:
            self.items = [*json.load(f)[title].items()]

        self.word_btns = []
        self.def_btns = []

        for i, item in enumerate(self.items):
            self.word_btns.append(VocabWord(
                master=self, 
                text=item[0], 
                width=300,
                height=65,
                border_color=main_color, 
                border_width=2, 
                border_spacing = 20,
                corner_radius = 15,
                text_color='black', 
                fg_color='white',
                hover_color='#f7f0e9',
                anchor='w', 
                font=('Lato', 20, 'bold'),
                row=i+1, column=0, padx=60, pady=10, sticky='we'
                ))
            
            self.def_btns.append(VocabWord(
                master=self, 
                text=item[1], 
                width=850,
                height=65,
                text_color='black', 
                border_color='#f2f2f2', 
                border_spacing=20,
                corner_radius=15,
                fg_color='#f2f2f2', 
                hover_color='#dbdbdb',
                anchor='w',
                font=('Lato', 20, 'bold'),
                row=i+1, column=1, padx=0, pady=10, sticky='we'
                ))
            
        self.new_word_btn = customtkinter.CTkButton(
            master=self,
            text="➕",
            height=70,
            corner_radius=15,
            text_color='white',
            fg_color='#f5e5d3',
            hover_color='#ebd0b2',
            font=('Lato', 30, 'bold'),
            command=self.genWord
            )
        self.new_word_btn.grid(row=len(self.items)+1, column=0, padx=60, pady=10, sticky='we')

    def flashcards(self):
        self.save_vocab()

        for quiz in self.quiz_options:
            quiz.destroy()
        self.back_btn.destroy()

        self.destroy()
    
        flashcards_quiz = Flashcards(title=self.title, root=self.root, return_cmd=self.open_vocab)

    def exam(self):
        self.save_vocab()

        for quiz in self.quiz_options:
            quiz.destroy()
        self.back_btn.destroy()

        self.destroy()

        exam = Exam(title=self.title, root=self.root, return_cmd=self.open_vocab)


    def writing(self):
        for quiz in self.quiz_options:
            quiz.destroy()
        self.back_btn.destroy()

        self.destroy()

    def test(self):
        for quiz in self.quiz_options:
            quiz.destroy()
        self.back_btn.destroy()

        self.destroy()


    def genWord(self):
        self.word_btns.append(VocabWord(
            master=self, 
            text='', 
            width=300,
            height=65,
            border_color=main_color, 
            border_width=2, 
            border_spacing = 20,
            corner_radius = 15,
            text_color='black', 
            fg_color='white',
            hover_color='#f7f0e9',
            anchor='w', 
            font=('Lato', 20, 'bold'),

            row=len(self.word_btns)+1, column=0, padx=60, pady=10, sticky='we'))
        self.word_btns[-1].edit()
        
        self.def_btns.append(VocabWord(
            master=self, 
            text='', 
            width=850,
            height=65,
            text_color='black', 
            border_color='#f2f2f2', 
            border_spacing=20,
            corner_radius=15,
            fg_color='#f2f2f2', 
            hover_color='#dbdbdb',
            anchor='w',
            font=('Lato', 20, 'bold'),

            row=len(self.def_btns)+1, column=1, padx=0, pady=10, sticky='we'))
        self.def_btns[-1].edit()

        self.new_word_btn.grid(row=len(self.word_btns)+2, column=0, padx=60, pady=10, sticky='we')

    def packWords(self):
        self.pack(fill='both')

    def go_home(self):
        self.save_vocab()

        return_home()
        
        for button in self.quiz_options:
            button.destroy()
        self.back_btn.destroy()
        self.destroy()

    def open_vocab(self, title):
        vocab_page = VocabPack(root=root, title=title)
        vocab_page.packWords()

    def save_vocab(self):
        words = [i.cget('text') for i in self.word_btns]
        definitions = [j.cget('text') for j in self.def_btns]
        updated_vocab = dict(zip(words, definitions))

        with open("vocabulary.json",) as f:
            vocab = json.load(f)
            vocab[self.title] = updated_vocab

        with open("vocabulary.json", "w") as f:
            json.dump(vocab, f)


def return_home():
    home = Home(root)
    home.pack_lists()


title = tk.Label(root, text="QuizFree", font=('Lato', 50, 'bold'), bg='white', fg='#1B1B1E')
title.pack(pady=50)

return_home()

root.mainloop()

