from tkinter import *
from tkinter import messagebox
from random import randint,shuffle,choice
import pyperclip

FONT = ("Google sans", 10, "normal")
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():

    # using list comprehension.
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters+password_symbols+password_numbers

    print(password_list)
    shuffle(password_list)
    # python string join method will allow us to join all the elements in the iterable with a separator.
    password = "".join(password_list)
    pyperclip.copy(password)

    password_entry.delete(0, END)
    password_entry.insert(0,password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website=website_entry.get()
    credential = credential_entry.get()
    password = password_entry.get()
    if len(website)==0 or len(credential)==0 or len(password)==0:
        messagebox.showerror(title="Error", message="Please fill all fields")
    else:
        say_ok =messagebox.askokcancel(title = website, message=f"Once have a look at your entries and confirm\n\nEmail/Username : {credential}\nPassword            : {password}")
        if say_ok:
            with open("data.txt","a") as data:
                data.write(f"{website}  |  {credential}  |  {password}\n")
            website_entry.delete(0, END)
            password_entry.delete(0, END)
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200,highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

class Create_labels(Label):
    """this class will create a label with given text at given grid location."""
    def __init__(self,txt,clm_no,row_no):
        super().__init__()
        self.config(text=txt,font = FONT)
        self.grid(row=row_no, column=clm_no)

class Create_entries(Entry):
    """this class will create an entry at given grid location."""
    def __init__(self, width_size, clm_no, row_no, column_span=1):
        super().__init__()
        self.config(width=width_size,font=FONT)
        self.grid(row=row_no, column=clm_no, columnspan=column_span)


# creating all three required labels.
website_label = Create_labels("Website:",0,1)
credential_label = Create_labels("Email/Username:",0,2)
password_label = Create_labels("Password:",0,3)

#creating an entries.
website_entry = Create_entries(46,1,1,2)
website_entry.focus()
credential_entry = Create_entries(46,1,2,2)
password_entry = Create_entries(28,1,3)

# the insert allows use to insert into the entry, and we can also use END in place of 0 as index to enter at the end of
# already written input.
credential_entry.insert(0,"janken.rock@gmail.com")

#Creating two buttons.
generate_password_button = Button(text="Generate Password",command=generate_password,font=FONT)
generate_password_button.grid(row=3,column=2)

add_details_button = Button(text="Add", command=save_data, font=FONT, width=40)
add_details_button.grid(row=4,column=1,columnspan=2)

window.mainloop()