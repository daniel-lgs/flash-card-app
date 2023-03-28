from tkinter import *
import pandas
import random

data = pandas.read_csv("data/french_words.csv")
data = data.to_dict()
french_words = list(data["French"].values())
english_words = list(data["English"].values())
f_words_not_learned = []
e_words_not_learned = []
french_i = 0
english_i = 0


def generate_word_index(language):
    """This function needs to pass 'French' or 'English' exactly to works fine"""
    word = ""
    i = 0
    if language == "French":
        i = random.randint(0, len(french_words) - 1)
        word = french_words[i]
    elif language == "English":
        i = random.randint(0, len(english_words) - 1)
        word = english_words[i]
    return [word, i]


def change_canvas_text(language, word):
    canvas.itemconfig(language_text, text=language)
    canvas.itemconfig(word_text, text=word)


def flip_back():
    canvas.itemconfig(card_canvas, image=img_card_back)
    canvas.itemconfig(language_text, fill="white")
    canvas.itemconfig(word_text, fill="white")


def flip_front():
    canvas.itemconfig(card_canvas, image=img_card_front)
    canvas.itemconfig(language_text, fill="black")
    canvas.itemconfig(word_text, fill="black")


def save_not_learned(index):
    global f_words_not_learned, e_words_not_learned
    f_words_not_learned.append(french_words[index])
    e_words_not_learned.append(english_words[index])
    words_to_learn = {"French": f_words_not_learned, "English": e_words_not_learned}
    user_report = pandas.DataFrame.from_dict(words_to_learn)
    user_report.to_csv("data/words_to_learn.csv", index=False)


def remove_words(index):
    global french_words
    global english_words
    del french_words[index]
    del english_words[index]


def enable_buttons():
    button_right.config(state=NORMAL)
    button_wrong.config(state=NORMAL)


def disable_buttons():
    button_right.config(state=DISABLED)
    button_wrong.config(state=DISABLED)


def check_right():
    if french_i == english_i:
        pass
    else:
        save_not_learned(french_i)
    remove_words(french_i)
    disable_buttons()
    app_management()


def check_wrong():
    if french_i != english_i:
        pass
    else:
        save_not_learned(french_i)
    remove_words(french_i)
    disable_buttons()
    app_management()


def app_management():
    global french_i, english_i

    # Generates a French random word and pass to the screen
    word_and_index = generate_word_index("French")
    word_f = word_and_index[0]
    french_i = word_and_index[1]
    change_canvas_text("French", word_f)

    # Generates a word with a 50% chance of being the translation of the French word and after 3 secs pass to the screen
    word_and_index = generate_word_index("English")
    english_i = random.choice([french_i, word_and_index[1]])
    word_e = english_words[english_i]
    root.after(3000, flip_back)
    root.after(3000, change_canvas_text, "English", word_e)
    root.after(3000, enable_buttons)

    # Flip to the start position (front)
    flip_front()


BACKGROUND_COLOR = "#B1DDC6"

root = Tk()
root.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
root.title("Flashy")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

img_card_front = PhotoImage(file="images/card_front.png")
img_card_back = PhotoImage(file="images/card_back.png")
card_canvas = canvas.create_image(400, 263, image=img_card_front)
language_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

img_wrong = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=img_wrong, highlightthickness=0, command=check_wrong)
button_wrong.grid(row=1, column=0)

img_right = PhotoImage(file="images/right.png")
button_right = Button(image=img_right, highlightthickness=0, command=check_right)
button_right.grid(row=1, column=1)

disable_buttons()
app_management()

root.mainloop()
