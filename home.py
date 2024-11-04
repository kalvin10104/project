import tkinter as tk
from tkinter import messagebox
import mysql.connector as mc
from tkinter import ttk

con = mc.connect(user = "root", host = "localhost", password = "isreal", database = "library")
cursor = con.cursor()

class Library:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Library Management System - Home Page")
        self.root.geometry("600x500+500+150")
        self.root.configure(bg="#f0f0f0")
        try:
            self.root.attributes('-toolwindow', True)
        except tk.TclError:
            print('Not supported on your platform')

        self.back_img_ok = tk.PhotoImage(file="image/image.png")
        
        __ = tk.Label(self.root, image=self.back_img_ok)
        __.pack()

        btn_student_register = tk.Button(self.root, text="Student Register", width=20, height=2, command=self.student_register, bg="#4CAF50", fg="white")
        btn_student_register.place(x = 220, y = 100)

        btn_books = tk.Button(self.root, text="Books", width=20, height=2, command=self.books, bg="#2196F3", fg="white")
        btn_books.place(x = 220, y = 200)

        btn_issue_books = tk.Button(self.root, text="Issue Books", width=20, height=2, command=self.issue_books, bg="#FF9800", fg="white")
        btn_issue_books.place(x = 220, y = 300)

        self.root.mainloop()
        
    def student_register(self):
        self.root1 = tk.Toplevel(self.root)
        self.root1.title("Student Register Page")  
        self.root1.geometry("600x500+500+150")
        self.root1.configure(background="skyblue")
        
        self.sid_label=tk.Label(self.root1, text="Enter StudentName",font=("Arial", 12), bg="#f4f4f4")
        self.sid_label.place(x=50,y=100)
        self.name_entry = tk.Entry(self.root1, width=30)
        self.name_entry.place(x=200,y=100)
        
        self.name_label=tk.Label(self.root1, text="Enter StudentID",font=("Arial", 12), bg="#f4f4f4")
        self.name_label.place(x=80,y=150)
        self.sid_entry = tk.Entry(self.root1, width=30)
        self.sid_entry.place(x=200,y=150)
        
        self.btn_insert = tk.Button(self.root1, text="Register",bg="green", command=self.register_student)
        self.btn_insert.place(x=250,y=200)
        
    # Add student to database
    def register_student(self):
        student_id = self.sid_entry.get()
        student_name = self.name_entry.get()
        query = "INSERT INTO student(SID, Name) VALUES (%s, %s)"
        try:
            cursor.execute(query, (student_id, student_name))
            messagebox.showinfo("Success","Student Name Register")
        except mc.Error as err:
            messagebox.showerror("Error", "Please Insert the correct Value")
        finally:
            con.commit()
            
    def books(self):
        self.root2 = tk.Toplevel(self.root)
        self.root2.title("Library Management System - Available Books")
        self.root2.geometry("600x500+500+150")
        self.root2.configure(background="skyblue")

        self.tree = ttk.Treeview(self.root2, columns=("BID", "Name", "Status"), show='headings')
        self.tree.heading("BID", text="Book ID")
        self.tree.heading("Name", text="Book Name")
        self.tree.heading("Status", text="Status")

        self.scrollbar = ttk.Scrollbar(self.root2, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.display_available_books()

        self.book_name = tk.Entry(self.root2, width=30)
        self.book_name.place(x = 100, y = 350)
        self.book_name.insert(0, "Enter Book Name")
        
        self.status = ttk.Combobox(self.root2, values=['Available','Checked Out','Reserved'])
        self.status.place(x = 300, y = 345)
        
        self.btn_insert_book = tk.Button(self.root2, text="Register", command=self.insert_book)
        self.btn_insert_book.place(x = 300, y = 375)
        
    def insert_book(self):
        name = self.book_name.get()
        statue = self.status.get()
        value = (name, statue)
        query = "INSERT INTO Books (Name, Status) VALUES (%s,%s)"
        try:
            cursor.execute(query, value)
            messagebox.showinfo("Success","Books Saved")
            self.display_available_books()
        except mc.Error as err:
            messagebox.showerror("Error", "Please Insert the correct Value")
        finally:
            con.commit()
    
    def display_available_books(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor.execute("SELECT BID, Name, Status FROM Books WHERE Status = 'Available'")
        available_books = cursor.fetchall()

        for book in available_books:
            self.tree.insert("", tk.END, values=book)

    def issue_books(self):
        self.root3 = tk.Toplevel(self.root)
        self.root3.geometry("600x500+500+150")
        self.root3.configure(background="skyblue")
        
        self.book_id_issue=tk.Label(self.root3, text="Enter BookID",font=("Arial", 12), bg="#f4f4f4")
        self.book_id_issue.place(x=90,y=100)
        self.book_id_issue= tk.Entry(self.root3, width=30)
        self.book_id_issue.place(x=200,y=100)
        
        self.borrow_name=tk.Label(self.root3, text="Enter StudentID",font=("Arial", 12), bg="#f4f4f4")
        self.borrow_name.place(x=80,y=150)
        self.borrow_name= tk.Entry(self.root3, width=30)
        self.borrow_name.place(x=200,y=150)
        
        self.issue_status = ttk.Combobox(self.root3, values = ['Issued','Returned','Overdue'])
        self.issue_status.place(x=200,y=190)
        
        self.btn_issue = tk.Button(self.root3, text = "Confirm", bg="green", command=self.final)
        self.btn_issue.place(x=220,y=220)
        
    def final(self):
        bid = self.book_id_issue.get()
        std_id = self.borrow_name.get()
        status = self.issue_status.get()
        value_query = (bid, std_id, status)
            
        try:
            cursor.execute("INSERT INTO issue (BID, Student_ID, Status) VALUES (%s, %s, %s)", value_query)
            print(1)
            # cursor.execute("UPDATE Books SET Status = %s wHERE BID = %s", update_val)
            messagebox.showinfo("Success","Data Save Successfully")
            
        except mc.Error as err:
            # print(update_val)
            messagebox.showerror("Error", "Please Insert the correct Value")
        finally:
            con.commit()
            
if __name__ == "__main__":
    Library()
