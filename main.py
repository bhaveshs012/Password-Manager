from tkinter import *
from tkinter import messagebox
import pyperclip
import json
# ---------------------------- FIND PASSWORD ------------------------------- #
def find_pass():
    website = website_input.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)  
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:        
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Account Details", message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"Details for {website} is not added")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    import random
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)    # Gets the generated password on the clipboard to paste directly

    
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pass():
    website = website_input.get()
    email=email_input.get()
    password=password_input.get()

    new_dict={
        website:{
            "email":email,
            "password":password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="Make sure you haven't left any fields Empty")
    else:
        is_ok = messagebox.askokcancel(title="Details Entered", message=f"Website:{website}\nEmail:{email}\nPassword:{password}\nIs it okay to save?")
        if is_ok:
            try:
                with open(file="data.json", mode="r") as data_file:
                    data = json.load(data_file) # Reading the old data
            except FileNotFoundError:
                with open(file="data.json", mode="w") as data_file:
                    json.dump(new_dict,data_file, indent=4)       
            else:        
                data.update(new_dict) # updating the data
                with open(file="data.json", mode="w") as data_file:
                    json.dump(data,data_file,indent=4) # adding the updated data to the file
            finally:
                website_input.delete(0, 'end')
                password_input.delete(0, 'end')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)

# Creating The Canvas
canvas = Canvas(width=200,height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100,100,image=logo)
canvas.grid(row=1,column=2)


# Creating Labels
website_label = Label(text="Website:")
website_label.grid(column=1,row=2)
email_label = Label(text="Email/Username:")
email_label.grid(column=1,row=3)
password = Label(text="Password:")
password.grid(column=1,row=4)

# Creating Input Fields

website_input = Entry()
website_input.focus()
website_input.config(width=20)
website_input.grid(column=2,row=2)

email_input = Entry()
email_input.insert(0, "your_email@email.com") # replace this with your email address
email_input.config(width=39)
email_input.grid(column=2,row=3,columnspan=2)

password_input = Entry()
password_input.config(width=20)
password_input.grid(column=2,row=4)


# Buttons
but1 = Button(text="Generate Password", command=generate_password)
but1.grid(column=3,row=4)

but2 = Button(text = "Add", command=save_pass)
but2.config(width=33)
but2.grid(column=2,row=5,columnspan=2)

search_button = Button(text="Search", width=15, command=find_pass)
search_button.grid(column=3,row=2)

window.mainloop()