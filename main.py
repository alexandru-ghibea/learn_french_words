import random
import pandas
from tkinter import *
from tkinter import messagebox
BACKGROUND_COLOR = "#B1DDC6"
TEXT_COLOR = "#000000"
WHITE_COLOR = "#FFFFFF"
current_card = {}
to_learn = {}

#TODO 2 Create New Flash Cards
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
except pandas.errors.EmptyDataError:
    messagebox.showerror(message="End of list. All words are know. Please provide other list")

else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, timer_flip
    window.after_cancel(timer_flip)
    try:
        current_card = random.choice(to_learn)
    except IndexError:
        print("End of cards to flip. Reset data")
    canvas.itemconfig(card_title, tex="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_front, image=card_front)
    timer_flip = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, tex="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_front, image=card_back)


#TODO 3 Save known words
def is_known():
    try:
        to_learn.remove(current_card)
    except ValueError:
        messagebox.showinfo(title="You know all words",
                            message="You've checked all the words as known. Please change list")
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv",index=FALSE)
    next_card()


#TODO 1 UI setup

window = Tk()
window.title("Learn with Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer_flip = window.after(3000, func=flip_card)

card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
right_button = PhotoImage(file='images/right.png')
wrong_button = PhotoImage(file='images/wrong.png')

canvas = Canvas(width=800, height=526)
canvas_front = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 40, "bold"), fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)


x_button = Button(image=wrong_button, highlightthickness=0, command=next_card)
x_button.config(highlightbackground=BACKGROUND_COLOR)
x_button.grid(row=1, column=0)

check_button = Button(image=right_button, highlightthickness=0, command=is_known)
check_button.config(highlightbackground=BACKGROUND_COLOR)
check_button.grid(row=1, column=1)
next_card()

window.mainloop()
