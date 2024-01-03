import tkinter as tk
import customtkinter as ctk
import json
from functools import partial
import random
from time import sleep

main_color = '#FAA916'
hover_color = '#C47C18'

class Exam(tk.Frame):
    def __init__(self, title, root, return_cmd):
        super().__init__(root, bg='white')

        with open("vocabulary.json", "r+") as f:
            self.vocab = json.load(f)[title]

        self.return_cmd = return_cmd
        self.index = 0
        self.state = 0
        self.root = root
        self.title = title
        self.score = [0, 0] # Score: [correct, total]

        self.back_btn = ctk.CTkButton(
            master=root, 
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

        self.new_q()

        self.pack()

    def writing_q(self):
        self.word = random.choices(list(self.vocab.keys()))[0]
        
        self.word_label = tk.Label(self.root, text=self.word, bg='white', font=('Lato', 30, 'bold'))
        self.word_label.place(x=800, y=600)
        self.word_entry = ctk.CTkEntry(
            self.root,
            width=700, 
            height=60, 
            border_color=main_color, 
            bg_color='white', 
            font=('Lato', 20, 'bold'))
        self.word_entry.place(x=520, y=450)
        self.word_entry.bind('<Return>', self.check_q)

    def check_q(self, e):
        if self.word_entry.get() == self.vocab[self.word]:
            self.score[0] += 1
            self.checkmark = tk.Label(self.root, text='✅', bg='white', fg='green', font=('Lato', 30, 'bold'))
            self.checkmark.place(x=300, y=200)
            self.pack()
            self.checkmark.after(500, lambda: self.checkmark.destroy())

        else:
            self.x_mark = tk.Label(self.root, text='❌', fg='red', bg='white', font=('Lato', 30, 'bold'))
            self.x_mark.place(x=300, y=200)
            self.x_mark.after(500, lambda: self.x_mark.destroy())

        self.score[1] += 1
        self.word_label.destroy()
        self.word_entry.destroy()

        if self.score[1] >= 11:
            self.result()
        else:
            self.new_q()

    def mult_choice_q(self):
        self.word = random.choices(list(self.vocab.keys()))[0]
        self.options = [self.word, *random.choices(list(set(self.vocab.keys())-set(self.word)), k=3)]
        random.shuffle(self.options)

        self.word_label = tk.Label(self, text=self.word.title(), bg='white', font=('Lato', 50, 'bold'))
        self.word_label.grid(row=0, column=0, columnspan=2, pady=20)

        self.card_upper_r = ctk.CTkButton(
            master=self,
            text=self.vocab[self.options[0]],
            width=600,
            height=300,
            corner_radius=15,
            border_width=3,
            border_color=main_color,
            text_color='black',
            fg_color='white',
            hover_color='#f7f0e9',
            anchor='center',
            font=('Lato', 20, 'bold'),
            command=lambda: self.mult_choice_check_q(self.options[0], self.card_lower_r)
        )
        self.card_upper_r.grid(row=1, column=1, padx=10, pady=10)

        self.card_upper_l = ctk.CTkButton(
            master=self,
            text=self.vocab[self.options[1]],
            width=600,
            height=300,
            corner_radius=15,
            border_width=3,
            border_color=main_color,
            text_color='black',
            fg_color='white',
            hover_color='#f7f0e9',
            anchor='center',
            font=('Lato', 20, 'bold'),
            command=lambda: self.mult_choice_check_q(self.options[1], self.card_upper_l)
        )
        self.card_upper_l.grid(row=1, column=0, padx=10, pady=10)

        self.card_lower_r = ctk.CTkButton(
            master=self,
            text=self.vocab[self.options[2]],
            width=600,
            height=300,
            corner_radius=15,
            border_width=3,
            border_color=main_color,
            text_color='black',
            fg_color='white',
            hover_color='#f7f0e9',
            anchor='center',
            font=('Lato', 20, 'bold'),
            command=lambda: self.mult_choice_check_q(self.options[2], self.card_lower_r)
        )
        self.card_lower_r.grid(row=2, column=1, padx=10, pady=10)

        self.card_lower_l = ctk.CTkButton(
            master=self,
            text=self.vocab[self.options[3]],
            width=600,
            height=300,
            corner_radius=15,
            border_width=3,
            border_color=main_color,
            text_color='black',
            fg_color='white',
            hover_color='#f7f0e9',
            anchor='center',
            font=('Lato', 20, 'bold'),
            command=lambda: self.mult_choice_check_q(self.options[3], self.card_lower_l)
        )
        self.card_lower_l.grid(row=2, column=0, padx=10, pady=10)

    def mult_choice_check_q(self, word_choice, card):
        if word_choice == self.word:
            card.configure(fg_color="#66de8a")
            self.score[0] += 1

            self.checkmark = tk.Label(self.root, text='✅', bg='white', fg='green', font=('Lato', 30, 'bold'))
            self.checkmark.place(x=300, y=200)
            self.pack()
            self.checkmark.after(500, lambda: self.checkmark.destroy())
        else:
            card.configure(fg_color='#ff8a92')

            self.x_mark = tk.Label(self.root, text='❌', fg='red', bg='white', font=('Lato', 30, 'bold'))
            self.x_mark.place(x=300, y=200)
            self.x_mark.after(500, lambda: self.x_mark.destroy())

        self.card_upper_r.destroy()
        self.card_upper_l.destroy()
        self.card_lower_l.destroy()
        self.card_lower_r.destroy()

        self.score[1] += 1
        if self.score[1] >= 11:
            self.result()
        else:
            self.new_q()

    # Future question type (To-be-added)
    #def match_q(self):
    #    self.word = random.choices(list(self.vocab.keys()))[0]

    def new_q(self):
        random.choice([self.writing_q, self.mult_choice_q])()

    def result(self):
        self.score_label = tk.Label(self.root, text=f'{self.score[0]} / {self.score[1]}', bg='white', font=('Lato', 60, 'bold'))
        self.score_label.place(x=1200, y=600)

    def go_home(self):
        self.back_btn.destroy()
        self.destroy()

        self.return_cmd(self.title)