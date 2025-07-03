from tkinter import *
from tkinter import messagebox
from random import randint,shuffle,choice
import pyperclip,json,pandas
FONT = ("Google sans", 10, "normal")
HEADER_FONT = ("Google sans", 15, "bold")

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
    shuffle(password_list)
    # python string join method will allow us to join all the elements in the iterable with a separator.
    password = "".join(password_list)
    pyperclip.copy(password)
    password_entry.delete(0, END)
    password_entry.insert(0,password)

# ---------------------------- SEARCH FOR PASSWORD ------------------------------- #

# Setting up the UI for search button, and some pop up windows and its functionality.
def search_password():
    global website_entry
    website_name = website_entry.get().capitalize()
    try :
        with open("data.json","r") as data:
            search_info = json.load(data)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops!", message="No saved data found")
    else:
        if website_name in search_info:
            messagebox.showinfo(title="Found a match", message = f"Website    : {website_name}\n"
                                                                 f"Email         : {search_info[website_name]['email']}\n"
                                                                 f"password : {search_info[website_name]['password']}")
        else:
            messagebox.showinfo(title="Oops!", message=f"No details for {website_name} exist.")

# ---------------------------- DISPLAY SAVED DATA ------------------------------- #

# Setting up UI for the new window that displays the saved passwords and data.
def show_saved_data():
        # Handling the exception here if the file was not yet created. In other words, a file is not found.
        try:
            with open("data.json", "r") as data:
                saved_info = json.load(data)
        except FileNotFoundError:
            messagebox.showinfo(title="Oops!", message="No saved data found")
        else:
            saved_window = Tk()
            saved_window.title("Saved Credentials")
            saved_window.config(padx=20, pady=20)
            df = pandas.DataFrame(saved_info)
            transposed_df =df.T
            disp_emails = transposed_df["email"].values
            disp_passwords = transposed_df["password"].values
            disp_websites = transposed_df.index.values
            with open("emails.txt","w") as emails_data:
                for email in disp_emails:
                    emails_data.write(f"{email}\n")
            with open("passwords.txt","w") as passwords_data:
                for password in disp_passwords:
                    passwords_data.write(f"{password}\n")
            with open("websites.txt","w") as websites_data:
                for website in disp_websites:
                    websites_data.write(f"{website}\n")
            with open("emails.txt","r") as emails_data:
                emails = emails_data.read()
            with open("passwords.txt","r") as passwords_data:
                passwords = passwords_data.read()
            with open("websites.txt","r") as websites_data:
                websites = websites_data.read()

            saved_label = Label(saved_window, text=f"Websites",font= HEADER_FONT,padx=10,pady=10)
            saved_label.grid(row=0,column=0)
            saved_label = Label(saved_window, text=f"Emails",font= HEADER_FONT,padx=10,pady=10)
            saved_label.grid(row=0,column=1)
            saved_label = Label(saved_window, text=f"Passwords",font= HEADER_FONT,padx=10,pady=10)
            saved_label.grid(row=0,column=2)
            saved_label = Label(saved_window, text=f"{websites}",font=FONT,padx=10,pady=10)
            saved_label.grid(row=1,column=0)
            saved_label = Label(saved_window, text=f"{emails}",font=FONT,padx=10,pady=10)
            saved_label.grid(row=1,column=1)
            saved_label = Label(saved_window, text=f"{passwords}",font=FONT,padx=10,pady=10)
            saved_label.grid(row=1,column=2)
            saved_window.mainloop()

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_data():
    website=website_entry.get().capitalize()
    credential = credential_entry.get()
    password = password_entry.get()

    data_dict = {
        website:{
            "email": credential,
            "password": password,
        }
    }

    if len(website)==0 or len(credential)==0 or len(password)==0:
        messagebox.showerror(title="Error", message="Please fill all fields")
    else:
        # handling the exception here, when there is no Existence of the file when read, it may lead to a FileNotFoundError.
        # hence, we create the file if such exception is met.
        try:
            with open("data.json","r") as data:
                # reading the old data.
                json_dict = json.load(data)
                # updating old data with new data.
                json_dict.update(data_dict)
        except FileNotFoundError:
            with open("data.json", "w") as data:
                # saving updated data.
                json.dump(data_dict, data, indent=4)
        else:
            with open ("data.json","w") as data:
                json.dump(json_dict,data,indent=4)
        finally:
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


#creating labels.
website_label = Create_labels("Website:",0,1)
credential_label = Create_labels("Email/Username:",0,2)
password_label = Create_labels("Password:",0,3)

#creating entries.
website_entry = Create_entries(28,1,1,1)
website_entry.focus()
credential_entry = Create_entries(46,1,2,2)
password_entry = Create_entries(28,1,3)

# the insert allows use to insert into the entry, and we can also use END in place of 0 as index to enter at the end of
# already written input.
credential_entry.insert(0,"janken.rock@gmail.com")

#Creating buttons.
generate_password_button = Button(text="Generate Password",command=generate_password,font=FONT)
generate_password_button.grid(row=3,column=2)
add_details_button = Button(text="Add", command=save_data, font=FONT, width=40)
add_details_button.grid(row=4,column=1,columnspan=2)
show_saved_button = Button(text="View saved data",command=show_saved_data,font=FONT,width=40)
show_saved_button.grid(row=5,column=1,columnspan=2)
search_button = Button(text="Search",command=search_password,font=FONT,width=14)
search_button.grid(row=1,column=2)

window.mainloop()