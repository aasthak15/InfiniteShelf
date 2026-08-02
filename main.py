'''
Library Management System
this program allows users to manage a library of books.
Users can add, delete, sort, and search for books. 
The program also allows users to generate random book entries 
using the Faker library.
the program uses a JSON file to store the library data.
The status structure has also been implemented.
'''
import os
import json
import threading
import tkinter as tk
from faker import Faker
import random
from tkinter import ttk, messagebox
from tkinter.font import Font

# Main window setup
window = tk.Tk()
window.title("Library Management")
window.geometry("1250x650")
window.configure(bg="#e6f2ff")  # pastel blue bg

# Global variable of library data
library_data = {}
# Default file
main_file = "lib_default.json"
stop_generation = False

# Color scheme
colors = {
    "background": "#e6f2ff",  # pastel blue
    "button": "#d1e0ff",      # light pastel blue
    "button_active": "#b3c6ff", 
    "text_display": "#f5f5ff", # pale lavender
    "header": "#ccd9ff",       # soft lavender
    "text_highlight": "#809fff" # Blue
}

# Fonts
main_font = Font(family="Helvetica", size=11)
title_font = Font(family="Helvetica", size=12, weight="bold")

# Style configuration
style = ttk.Style()
style.theme_use('clam')

style.configure("TFrame", background=colors["background"])
style.configure("TButton", 
               font=("Helvetica", 11),
               background="#d1e0ff",  # Light pastel blue
               borderwidth=1,
               relief="raised",
               foreground="black")  # Text color

style.map("TButton",
         background=[('active', "#b3c6ff")],  # Button color when clicked
         bordercolor=[('!disabled', "#003366")])  # Dark blue border

style.configure("TLabel", 
               font=main_font, 
               background=colors["background"])
style.configure("TEntry", font=main_font)
style.configure("TCombobox", font=main_font)

# Create a frame for buttons and controls
frame_controls = ttk.Frame(window, padding=10)
frame_controls.pack(pady=10)

frame_display = ttk.Frame(window)
frame_display.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

def load_library():
    global library_data
    global main_file
    try:
        with open(main_file, "r") as file:
            library_data = json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        library_data = {}

def save_library(data):
    global main_file
    with open(main_file, "w") as file:
        json.dump(data, file, indent=4)
    list_books()

# Function to print number of books in the library
def print_number_of_books():
    global library_data
    number_of_books = len(library_data)
    text = f"Number of books in the library: {number_of_books}"
    label = ttk.Label(frame_display, text=text, font=main_font, background=colors["background"])
    label.pack(pady=10)
    # Clear previous labels
    for widget in frame_display.winfo_children():
        if isinstance(widget, ttk.Label) and widget != label:
            widget.destroy()

# Function to list books
def list_books():
    global library_data
    books = library_data
    for item in tree.get_children():
        tree.delete(item)
    # check if library data is empty
    if not library_data:
        tree.insert("", "end", values=("No", "books found", "", ""))
    else:
        for book_id, book in books.items():
            tree.insert("", "end", iid=book_id, values=(book_id, book["title"], book['author'], book["year"], book["status"]))
    print_number_of_books()  # Call the function to print number of books

# Function for adding books
def add_book():
    global library_data
    books = library_data
    add_win = tk.Toplevel(window)
    add_win.title("Add Book")
    add_win.geometry("400x300")
    add_win.configure(bg=colors["background"])

    ttk.Label(add_win, text="Enter Book Title").pack(pady=10)
    title_entry = ttk.Entry(add_win)  
    title_entry.pack(pady=5)

    ttk.Label(add_win, text="Enter Book Author").pack(pady=10)
    author_entry = ttk.Entry(add_win)  
    author_entry.pack(pady=5)

    ttk.Label(add_win, text="Enter Book Year").pack(pady=10)
    year_entry = ttk.Entry(add_win)  
    year_entry.pack(pady=5)

    # Define confirm_add function here
    def confirm_add():
        global library_data
        number = len(books)
        books[f"{number + 1}"] = {
            "title": title_entry.get(),  
            "author": author_entry.get(),  
            "year": year_entry.get(),
            "status": "available"
        }
        library_data = books
        save_library(library_data)  
        list_books()  
        add_win.destroy()  

    submit_button = ttk.Button(add_win, text="Submit", command=confirm_add)
    submit_button.pack(pady=5)

# Function for deleting books
def delete_book():
    global library_data
    del_win = tk.Toplevel(window)
    del_win.title("Delete Book")
    del_win.geometry("300x150")
    del_win.configure(bg=colors["background"])

    ttk.Label(del_win, text="Enter Book ID to delete:").pack(pady=10)
    id_entry = ttk.Entry(del_win)
    id_entry.pack(pady=5)

    def confirm_delete():
        global library_data
        book_id = id_entry.get()
        books = library_data

        if book_id in books:
            library_data[book_id]['status'] = 'deleted'
            save_library(library_data)  
            list_books()  
            del_win.destroy() 
        else:
            messagebox.showerror("Error", "Book ID not found")

    ttk.Button(del_win, text="Delete", command=confirm_delete).pack(pady=10)

# Function for sorting books
def sort_books():
    global library_data
    sort_win = tk.Toplevel(window)
    sort_win.title("Sort Books")
    sort_win.geometry("300x150")
    sort_win.configure(bg=colors["background"])

    ttk.Label(sort_win, text="Sort by:").pack(pady=10)

    sort_var = tk.StringVar()
    sort_box = ttk.Combobox(sort_win, textvariable=sort_var, state="readonly")
    sort_box['values'] = ('Title', 'Author', 'Year')
    sort_box.pack(pady=5)

    def apply_sort():
        global library_data
        books = library_data
        if not books:
            sort_win.destroy()
            return

        key = sort_var.get().lower()

        if key == 'title':
            sorted_books = dict(sorted(books.items(), key=lambda item: item[1]['title']))
        elif key == 'author':
            sorted_books = dict(sorted(books.items(), key=lambda item: item[1]['author']))
        elif key == 'year':
            sorted_books = dict(sorted(books.items(), key=lambda item: item[1]['year']))
        
        # Update the library data with the sorted books
        library_data = sorted_books
        
        # Close the sort window after applying sort
        sort_win.destroy()
        
        # Call list_books to refresh the display
        list_books()

    submit_button = ttk.Button(sort_win, text="Submit", command=apply_sort)
    submit_button.pack()
   
# Function for searching books
def search_books():
    global library_data
    search_win = tk.Toplevel(window)
    search_win.title("Search Books")
    search_win.geometry("350x200")
    search_win.configure(bg=colors["background"])
    
    ttk.Label(search_win, text="Search by:").pack(pady=5)
    
    search_var = tk.StringVar()
    search_box = ttk.Combobox(search_win, textvariable=search_var, state="readonly")
    search_box['values'] = ('Title', 'Author', 'Year', 'ID')
    search_box.pack(pady=5)
    
    ttk.Label(search_win, text="Search term:").pack(pady=5)
    term_entry = ttk.Entry(search_win)
    term_entry.pack(pady=5)
    
    def perform_search():
        global library_data
        books = library_data
        if not books:
            search_win.destroy()
            return
            
        field = search_var.get().lower()
        term = term_entry.get().lower()
        
        results = []
        for book_id, book in books.items():
            if field == 'id':
                if term in book_id.lower():
                    results.append((book_id, book))
            else:
                if term in str(book[field]).lower():
                    results.append((book_id, book))
        
        for item in tree.get_children():
            tree.delete(item)
        if results:
            for book_id, book in results:
                tree.insert("", "end", iid=book_id, values=(book_id, book["title"], book['author'], book["year"], book["status"]))
        else:
            tree.insert("", "end", values=("No", "books", "found", ""))
        
        search_win.destroy()
    
    ttk.Button(search_win, text="Search", command=perform_search).pack(pady=10)

# Function to display information of selected book
def show_book(event):
    global library_data
    selected_item = tree.selection()
    if not selected_item:
        return

    # Getting the values of the selected row
    book_id = tree.item(selected_item, 'values')[0]
    book = library_data.get(book_id)

    if book:
        popup = tk.Toplevel(window)
        popup.title(f"Book Information: {book['title']}")
        popup.geometry("400x350")
        
        book_info = f"Book ID: {book_id}\nTitle: {book['title']}\nAuthor: {book['author']}\nStatus: {book['status']}"
        info_text = tk.Text(popup, height=10, width=40, wrap=tk.WORD, font=main_font)
        info_text.insert(tk.END, book_info)
        info_text.insert(tk.END, "\n\nWhat action would you like to take?")
        info_text.config(state=tk.DISABLED) 
        option_var = tk.StringVar()
        option_box = ttk.Combobox(popup, textvariable=option_var, state="readonly")
        option_box['values'] = ('Rent', 'Return')
        

        def option_result():
            info_text.config(state=tk.NORMAL)
            if option_var.get() == "Rent":
                if book['status'] == 'available':
                    info_text.insert(tk.END, "\nBook lent to you")
                    book['status'] = "lent out"
                elif book['status'] == 'lent out':
                    info_text.insert(tk.END, "\nBook is already lent out")
                else:
                    info_text.insert(tk.END, "Book is missing")
            elif option_var.get() == 'Return':
                if book['status'] == 'missing' or book['status'] == 'lent out':
                    info_text.insert(tk.END, "\n Book returned successfully!")
                    book['status'] = "available"
                elif book['status'] == 'available':
                    info_text.insert(tk.END, "\n Book is already present, it cannot be returned!")
            library_data[book_id] = book
            save_library(library_data)
            info_text.config(state=tk.DISABLED)

        info_text.pack(pady=10)
        option_box.pack(side=tk.LEFT, pady=5)
        result_button = ttk.Button(popup, text="Submit", command=option_result)
        result_button.pack(side=tk.LEFT, padx=5)

# Function to generate 1 million entries
def generate_books():
    global library_data, stop_generation
    fake = Faker()
    statuses = ["available", "lent out", "missing"]
    number = len(library_data)
    
    def generate_batch():
        nonlocal number
        if stop_generation or len(library_data) >= 1000000:
            save_library(library_data) 
            list_books()
            messagebox.showinfo("Generation Complete", "Book generation has been completed.")
            return
        
        for _ in range(5):  
            library_data[f"{number + 1}"] = {
                "title": f"The {fake.word().capitalize()}",
                "author": f"{fake.first_name()} {fake.last_name()}",
                "year": random.randint(1800, 2025),
                "status": random.choice(statuses),
            }
            number += 1
        
        # Save periodically to avoid data loss
        if number % 100 == 0:
            save_library(library_data)
        
        list_books()  
        window.after(10, generate_batch)  

    generate_batch()

# Function to start book generation
def start_generation():
    global stop_generation
    stop_generation = False # Ensure the stop flag is reset
    threading.Thread(target=generate_books, daemon=True).start()

# Function to stop book generation
def stop_book_generation():
    global stop_generation
    stop_generation = True
    messagebox.showinfo("Generation Stopped", "Book generation has been stopped.")
# Table display with scrollbar
scrollbar = ttk.Scrollbar(frame_display)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

style.configure("Treeview",
                font=("Helvetica", 12),  # Larger font size
                background=colors["background"],  # Background color
                foreground="black")  # Text color
style.configure("Treeview.Heading",
                font=("Helvetica", 12, "bold"),  # Heading font style
                background=colors["header"],  # Header background color
                foreground=colors["text_highlight"])  # Header text color
style.configure("Treeview.Row",
                font=("Helvetica", 12),  # Row font style
                background=colors["background"],  # Row background color
                foreground= colors['text_display'])  # Row text color

# Create Treeview widget
tree = ttk.Treeview(frame_display, columns=("ID", "Title", "Author", "Year", "Status"), show="headings", yscrollcommand=scrollbar.set)

# Define column widths
tree.column("ID", width=50, anchor="center")
tree.column("Title", width=200, anchor="w")
tree.column("Author", width=200, anchor="w")
tree.column("Year", width=200, anchor="w")
tree.column("Status", width=200, anchor="w")

# Set column headers
tree.heading("ID", text="ID")
tree.heading("Title", text="Title")
tree.heading("Author", text="Author")
tree.heading("Year", text="Year")
tree.heading("Status", text="Status")

# Bind double-click event to the Treeview rows
tree.bind("<Double-1>", show_book)
tree.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=tree.yview)
'''
display_text = tk.Text(
    frame_display, 
    wrap=tk.WORD, 
    width=85, 
    height=20, 
    font=main_font, 
    bg=colors["text_display"], 
    relief=tk.SOLID, 
    borderwidth=1,
    yscrollcommand=scrollbar.set,
    padx=10,
    pady=10
)
display_text.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=display_text.yview)

# Text tags for formatting
display_text.tag_configure("title", foreground="#3366cc")  # Blue
display_text.tag_configure("author", foreground="#663399")  # Lavender
display_text.tag_configure("id", foreground="#666699")  # Muted purple-blue
'''
# Create buttons inside the frame
buttons = [
    ("List books", list_books),
    ("Add Book", add_book),
    ("Delete Book", delete_book),
    ("Sort Books", sort_books),
    ("Search Books", search_books),
    ("Generate Random Books", start_generation),
    ("Stop Generation", stop_book_generation),
    ("Exit", window.quit)
]

for text, command in buttons:
    ttk.Button(frame_controls, text=text, command=command).pack(side=tk.LEFT, padx=5)

def change_main_file(f):
    global main_file, library_data  
    main_file = f
    load_library()  

def create_new_file():
    global main_file
    popup = tk.Toplevel(window)
    popup.title("New File")
    popup.geometry("350x150")
    popup.configure(bg=colors["background"])
    
    ttk.Label(popup, text="Enter new file name: (without extension)").pack(pady=5)
    term_entry = ttk.Entry(popup)
    term_entry.pack(pady=5)
    
    def execute():
        global main_file
        new_filename = term_entry.get()
        main_file = f"{new_filename}.json"
        with open(f"{new_filename}.json", "w") as file:
            pass
        popup.destroy()
    submit_button = ttk.Button(popup, text="Submit", command=execute)
    submit_button.pack(pady=10)

# Add a Menu bar
json_files = [f for f in os.listdir() if f.endswith(".json")]
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Choose File",font=title_font, menu=file_menu)
file_menu.add_command(label="Create new", command= create_new_file)
for file in json_files:
    file_menu.add_command(label=file, command=lambda f=file: change_main_file(f))

# Load the library data when the program starts 
load_library()
window.mainloop()