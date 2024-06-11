import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def setup_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL,
        isbn TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def add_book(title, author, year, isbn):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO books (title, author, year, isbn)
    VALUES (?, ?, ?, ?)
    ''', (title, author, year, isbn))
    conn.commit()
    conn.close()
    display_books()

def view_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_book(book_id, title, author, year, isbn):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE books
    SET title = ?, author = ?, year = ?, isbn = ?
    WHERE id = ?
    ''', (title, author, year, isbn, book_id))
    conn.commit()
    conn.close()
    display_books()

def delete_book(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    display_books()

def display_books():
    for row in tree.get_children():
        tree.delete(row)
    books = view_books()
    for book in books:
        tree.insert('', tk.END, values=book)

def add_book_callback():
    if title_entry.get() and author_entry.get() and year_entry.get() and isbn_entry.get():
        add_book(title_entry.get(), author_entry.get(), year_entry.get(), isbn_entry.get())
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "All fields must be filled")

def update_book_callback():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Update Error", "No book selected")
        return
    book_id = tree.item(selected, 'values')[0]
    if title_entry.get() and author_entry.get() and year_entry.get() and isbn_entry.get():
        update_book(book_id, title_entry.get(), author_entry.get(), year_entry.get(), isbn_entry.get())
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "All fields must be filled")

def delete_book_callback():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Delete Error", "No book selected")
        return
    book_id = tree.item(selected, 'values')[0]
    delete_book(book_id)
    clear_entries()

def clear_entries():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)

def select_book(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, 'values')
        title_entry.delete(0, tk.END)
        title_entry.insert(0, values[1])
        author_entry.delete(0, tk.END)
        author_entry.insert(0, values[2])
        year_entry.delete(0, tk.END)
        year_entry.insert(0, values[3])
        isbn_entry.delete(0, tk.END)
        isbn_entry.insert(0, values[4])

setup_db()

root = tk.Tk()
root.title("Library Book Management")
root.geometry("600x400")

style = ttk.Style()
style.theme_use('default')

style.configure("TLabel", font=('Arial', 10), padding=5, foreground="#2e3440")
style.configure("TButton", font=('Arial', 10), padding=5, foreground="#2e3440")
style.configure("TEntry", padding=5, font=('Arial', 10))
style.configure("Treeview", font=('Arial', 10), rowheight=25, fieldbackground="#d8dee9")
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

input_frame = ttk.Frame(root, padding="10 10 10 10", relief=tk.GROOVE)
input_frame.pack(pady=10, fill=tk.X)

ttk.Label(input_frame, text="Title").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
title_entry = ttk.Entry(input_frame, width=30)
title_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

ttk.Label(input_frame, text="Author").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
author_entry = ttk.Entry(input_frame, width=30)
author_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

ttk.Label(input_frame, text="Year").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
year_entry = ttk.Entry(input_frame, width=30)
year_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

ttk.Label(input_frame, text="ISBN").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
isbn_entry = ttk.Entry(input_frame, width=30)
isbn_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

button_frame = ttk.Frame(root, padding="10 10 10 10")
button_frame.pack(pady=10, fill=tk.X)

ttk.Button(button_frame, text="Add Book", command=add_book_callback).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="Update Book", command=update_book_callback).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(button_frame, text="Delete Book", command=delete_book_callback).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(button_frame, text="Clear Fields", command=clear_entries).grid(row=0, column=3, padx=5, pady=5)

tree_frame = ttk.Frame(root, padding="10 10 10 10")
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

tree = ttk.Treeview(tree_frame, columns=("ID", "Title", "Author", "Year", "ISBN"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Title", text="Title")
tree.heading("Author", text="Author")
tree.heading("Year", text="Year")
tree.heading("ISBN", text="ISBN")
tree.column("ID", width=30, anchor=tk.CENTER)
tree.column("Title", width=150)
tree.column("Author", width=100)
tree.column("Year", width=50, anchor=tk.CENTER)
tree.column("ISBN", width=100)
tree.pack(fill=tk.BOTH, expand=True)

tree.bind("<ButtonRelease-1>", select_book)

display_books()


root.configure(bg="#4c566a")

style.map('Treeview', background=[('selected', '#81a1c1')])
style.map('Treeview.Heading', background=[('active', '#5e81ac')], foreground=[('active', 'white')])


scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()
