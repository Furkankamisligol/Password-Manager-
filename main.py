from tkinter import *
from tkinter import messagebox
import pyperclip
import json

def generate_password():
    from random import randint, choice, shuffle
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_numbers + password_symbols + password_letters

    shuffle(password_list)

    generated_password = "".join(password_list)
    password_entry.insert(0, f"{generated_password}")
    pyperclip.copy(generated_password)


def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message="You left one of the entries empty!")
    else:
        go_on = messagebox.askokcancel(title=website, message=f"These are the details entered: \nUsername:{username}"
                                                              f" \nPassword:{password} \n Are you sure of details?")
        if go_on:

            website_json = {website: {
                "email": username,
                "password": password

                }
            }
            try:
                with open("passwords.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open("passwords.json", "w") as file:
                    json.dump(website_json, file, indent=4)
            else:
                data.update(website_json)
                with open("passwords.json", "w") as file:
                    json.dump(data, file, indent=4)

        else:
            username_entry.delete(0, END)
            password_entry.delete(0, END)


def search_website():
    website = website_entry.get()
    with open("passwords.json", "r") as file:
        data = json.load(file)
    try:
        username_1 = data[website]["email"]
        password_1 = data[website]["password"]
        messagebox.showinfo(title=f"{website}", message=f"Email: {username_1}\nPassword: {password_1}")
    except KeyError:
        messagebox.showinfo(title="Error", message=f"'{website}' This website is not saved.")



window = Tk()
window.title("Password Manager")
window.geometry("500x500")
window.config(padx=50, pady=50)
#
logo_image = PhotoImage(file="logo.png")
canvas = Canvas(height=200, width=200)
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0, columnspan=2)
#
website_label = Label(text="Website:")
username_label = Label(text="Email/Username:")
password_label = Label(text="Password:")
generate_button = Button(text="Generate Password", command=generate_password)
add_button = Button(text="Add", command=save_password)
search_button = Button(text="Search", command=search_website)
website_entry = Entry()
username_entry = Entry()
password_entry = Entry()
#
generate_button.config()
add_button.config(width=34)
search_button.config(width=14)
website_entry.config(width=21)
username_entry.config(width=40)
password_entry.config(width=21)
#
website_label.grid(row=1, column=0)
password_label.grid(row=3, column=0)
username_label.grid(row=2, column=0)
generate_button.grid(row=3, column=2)
add_button.grid(row=4, column=1, columnspan=2)
website_entry.grid(row=1, column=1, )
username_entry.grid(row=2, column=1, columnspan=2)
password_entry.grid(row=3, column=1)
search_button.grid(row=1, column=2)
#
website_entry.focus()

username_entry.insert(0, "")


window.mainloop()
