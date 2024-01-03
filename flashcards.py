import tkinter as tk
import customtkinter as ctk
import json
from functools import partial

main_color = '#FAA916'
hover_color = '#C47C18'

class Flashcards(tk.Frame):
    def __init__(self, title, root, return_cmd):
        super().__init__(root, bg='white')

        with open("vocabulary.json", "r+") as f:
            self.vocab = [*json.load(f)[title].items()]

        self.return_cmd = return_cmd
        self.index = 0
        self.state = 0
        self.root = root
        self.title = title

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
                    command=self.go_home)
        self.back_btn.place(x=50, y=40)

        self.arrow_left=ctk.CTkButton(
             master=self,
             text="⇦",
             width=30,
             height=30,
             corner_radius=20,
             text_color="white",
             fg_color=main_color,
             hover_color=hover_color,
             anchor='center',
             font=('Lato', 30, 'bold'),
             command=self.prev_word
        )
        self.arrow_left.pack(side=tk.LEFT)

        self.arrow_right=ctk.CTkButton(
             master=self,
             text="⇨",
             width=30,
             height=30,
             corner_radius=20,
             text_color="white",
             fg_color=main_color,
             hover_color=hover_color,
             anchor='center',
             font=('Lato', 30, 'bold'),
             command=self.next_word
        )
        self.arrow_right.pack(side=tk.RIGHT)

        self.card = ctk.CTkButton(
            master=self,
            text="",
            width=600,
            height=400,
            corner_radius=15,
            border_width=3,
            border_color=main_color,
            text_color='black',
            fg_color='white',
            hover_color='#f7f0e9',
            anchor='center',
            font=('Lato', 20, 'bold'),
            command=self.reveal_card
        )
        self.card.pack(side=tk.LEFT, padx=50, pady=100)

        self.card.configure(text=self.vocab[0][0])
        self.pack()

    def next_word(self):
         if self.index + 1 >= 0 and self.index + 1 < len(self.vocab):
            self.card.configure(text=self.vocab[self.index + 1][0])
            self.index += 1
            self.state = 0
    def prev_word(self):
         if self.index - 1 >= 0 and self.index - 1 < len(self.vocab):
            self.card.configure(text=self.vocab[self.index - 1][0])
            self.index -= 1
            self.state = 0

    def reveal_card(self):
        self.card.configure(text=self.vocab[self.index][(self.state+1)%2])        
        self.state = (self.state+1)%2

    def go_home(self):
        self.back_btn.destroy()
        self.destroy()

        self.return_cmd(self.title)
        

