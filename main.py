import os
import tkinter as tk
from tkinter import Tk, Canvas, PhotoImage
import pandas as pd
import random

# CONSTANTS
COLOR_BACKGROUND = '#B1DDC6'

PATH_CSV_WORDS = 'data/french_words.csv'
PATH_CSV_PROGRESS = 'data/french_words_progress.csv'

try:
    DATA_CSV_WORDS = pd.read_csv(PATH_CSV_PROGRESS)
except FileNotFoundError:
    DATA_CSV_WORDS = pd.read_csv(PATH_CSV_WORDS)
DATAFRAME_WORDS = pd.DataFrame(DATA_CSV_WORDS)

directory_words = DATAFRAME_WORDS.to_dict(orient="records")
word_current = {}

# Functions
def next_card():
    global word_current, timer_flip
    win.after_cancel(timer_flip)
    word_current = random.choice(directory_words)
    canvas.itemconfig(text_title, text="SOLVE MY FRENCH MAZE!")
    canvas.itemconfig(text_word, text=word_current['French'], fill='black')
    canvas.itemconfig(graphic_card, image=IMG_CARD_FRONT)
    timer_flip = win.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(text_title, text="TOO LATE, ENGLISHMAN!")
    canvas.itemconfig(text_word, text=word_current['English'], fill='white')
    canvas.itemconfig(graphic_card, image=IMG_CARD_BACK)

def answer_yes():
    directory_words.remove(word_current)
    df = pd.DataFrame(directory_words)
    df.to_CSV(PATH_CSV_WORDS,index=False)
    next_card()

# Screen
win = Tk()
win.title("Flash Cards")
win.config(padx=50, pady=50, bg=COLOR_BACKGROUND)

timer_flip = win.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
IMG_CARD_FRONT = PhotoImage(file="images/card_front.png")
IMG_CARD_BACK = PhotoImage(file="images/card_back.png")
graphic_card=canvas.create_image(400, 263, image=IMG_CARD_FRONT)
text_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
text_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.config(bg=COLOR_BACKGROUND, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

IMG_BUTTON_WRONG = PhotoImage(file="images/wrong.png")
button_no = tk.Button(image=IMG_BUTTON_WRONG, highlightthickness=0, command=next_card)
button_no.grid(row=1, column = 0)

IMG_BUTTON_RIGHT = PhotoImage(file="images/right.png")
button_yes = tk.Button(image=IMG_BUTTON_RIGHT, highlightthickness=0, command=next_card)
button_yes.grid(row=1, column = 1)

next_card()

win.mainloop()

