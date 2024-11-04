import tkinter as tk
from tkinter import messagebox
import mysql.connector as mc
from home import *

con = mc.connect(user = "root", host = "localhost", password = "isreal", database = "library")
cursor = con.cursor()

def login():
    username = entry_username.get()
    password = entry_password.get()
    try:
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        con.commit()
        if result:
            messagebox.showinfo("Login Success", "Welcome!")
            root.destroy()
            Library()

        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.geometry("600x500+500+150")
root.title("Login Page")
root.config(bg="#f4f4f4")
back_img_ok = tk.PhotoImage(file="image/login.png")
        
lab1= tk.Label(root, image=back_img_ok)
lab1.pack()

label_title = tk.Label(root, text="Login", font=("Arial", 30, "bold"), fg="#333", bg="#f4f4f4")
label_title.place(x=220,y=50)


label_username = tk.Label(root, text="Username:", font=("Arial", 12), bg="#f4f4f4")
label_username.place(x=120,y=200)
entry_username = tk.Entry(root, width=25, font=("Arial", 12))
entry_username.place(x=210,y=200)

label_password = tk.Label(root, text="Password:", font=("Arial", 12), bg="#f4f4f4")
label_password.place(x=120,y=280)
entry_password = tk.Entry(root, width=25, font=("Arial", 12), show="*")
entry_password.place(x=210,y=280)

btn_login = tk.Button(root, text="Login", font=("Arial", 12), bg="green", fg="white", width=10, height=1, command=login)
btn_login.place(x=230,y=350)

root.mainloop()
