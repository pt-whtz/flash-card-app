from tkinter import *
import pandas
import json
import shutil
from random import choice

BG_COLOR = "#b1ddc6"
FONT = "Courier"


# -------------------------Flash Card Mechanism ------------------------


def build_dictionary():

    global words_dictionary

    try:
        words = pandas.read_csv("./data/1000_spanish_words_TO_LEARN.csv")

    except FileNotFoundError:
        origin = "./data/1000_spanish_words.csv"
        destination = "./data/1000_spanish_words_TO_LEARN.csv"
        shutil.copy(origin, destination)
        words = pandas.read_csv("./data/1000_spanish_words_TO_LEARN.csv")

    words_dictionary = words.to_dict(orient="records")


def flip_card():

    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=en_word, fill="white")
    canvas.itemconfig(card_side, image=card_back)


def generate_card():

    global timer, es_word, en_word, random_words_pair

    random_words_pair = choice(words_dictionary)
    es_word = random_words_pair['Spanish']
    en_word = random_words_pair['English']

    canvas.itemconfig(card_side, image=card_front)
    canvas.itemconfig(language, text="Spanish", fill="black")
    canvas.itemconfig(word, text=es_word, fill="black")

    timer = window.after(3000, flip_card)


def learn_word():
    window.after_cancel(timer)

    words_dictionary.remove(random_words_pair)
    data = pandas.DataFrame(words_dictionary)
    data.to_csv("./data/1000_spanish_words_TO_LEARN.csv")

    generate_card()


def skip_word():
    window.after_cancel(timer)
    generate_card()


# ------------------------- GUI preparation -------------------------
# window setup
window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BG_COLOR)
window.wm_resizable(height=False, width=False)

# adding canvas
canvas = Canvas(width=800, height=520, bg=BG_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
card_side = canvas.create_image(400, 260, image=card_front)
language = canvas.create_text(400, 100, font=(FONT, 20, "italic"))
word = canvas.create_text(400, 250, font=(FONT, 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# adding buttons
check_image = PhotoImage(file="images/learn_word.png")
check_button = Button(image=check_image, highlightthickness=0, bd=0, command=learn_word)
check_button.grid(row=1, column=1)

unknown_image = PhotoImage(file="images/skip_word.png")
unknown_button = Button(image=unknown_image, highlightthickness=0, bd=0, command=skip_word)
unknown_button.grid(row=1, column=0)

# ------------------------------ Processing -----------------------------
build_dictionary()
generate_card()

window.wm_iconbitmap("./images/flash-cards-icon.ico")
window.mainloop()
