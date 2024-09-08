import tkinter as tk
from tkinter import ttk
import sqlite3

def execute_query():
    # Get values from entry widgets and comboboxes
    conditions = []
    for label, widget in entry_widgets.items():
        if label in ["accno", "isbn", "price"]:
            value = widget.get()
            if value:
                conditions.append(f"{label} = '{value}'")
        elif label in ["Author", "Author2", "Publisher"]:
            value = widget.get()
            if value:
                conditions.append(f'{label} LIKE "{value}%"')
        else:
            value = widget.get()
            if value:
                conditions.append(f'{label} LIKE "%{value}%"')

    query = "SELECT * FROM booksfile"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Execute the query and update the treeview
    cursor.execute(query)
    rows = cursor.fetchall()
    update_treeview(rows)

def update_treeview(rows):
    # Clear existing items in the treeview
    for item in tree.get_children():
        tree.delete(item)

    for idx, details in enumerate(rows, start=1):
        tree.insert("", "end", values=details)
    displaylabel.config(text="Records found = "+str(idx))


# Connect to SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create the main window
root = tk.Tk()
root.title("Book Search")

# Create a canvas
canvas = tk.Canvas(root, scrollregion=(0, 0, 1600, 600))
canvas.pack(fill="both", expand=True)

# Create a frame inside the canvas
frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Create and place widgets
labels = ["accno", "callno", "title", "subtitle", "author", "author2", "year", "publisher",
          "pageno", "price", "isbn", "Location", "status", "subject", "remarks"]

entry_widgets = {}
for i, label_text in enumerate(labels):
    tk.Label(frame, text=label_text).grid(row=0, column=i, padx=2, pady=2)
    if label_text == "Location":
        # Create a combobox for Location
        locations = [row[0] for row in cursor.execute("SELECT DISTINCT Location FROM booksfile")]
        entry_var = tk.StringVar()
        entry_widgets[label_text] = ttk.Combobox(frame, values=locations, textvariable=entry_var)
    elif label_text == "status":
        # Create a combobox for Status
        entry_var = tk.StringVar()
        entry_widgets[label_text] = ttk.Combobox(frame, values=["issued", "available"], textvariable=entry_var)
    else:
        # Create an entry widget
        entry_var = tk.StringVar()
        entry_widgets[label_text] = tk.Entry(frame, textvariable=entry_var, width=20)

    entry_widgets[label_text].grid(row=1, column=i, padx=2, pady=2)

# Create search button
search_button = tk.Button(frame, text="Search", command=execute_query)
search_button.grid(row=6, column=3, padx=5, pady=5)

displaylabel = tk.Label(root , text="")
displaylabel.pack(side=tk.BOTTOM, padx=5, pady=5)

# Create treeview
tree = ttk.Treeview(frame, columns=labels, show="headings")
tree.grid(row=2, column=0, columnspan=len(labels[1:]), pady=5)

# Set column headings
for col in labels:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=360)

# Create horizontal scrollbar for the canvas
horizontal_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
horizontal_scrollbar.pack(side="bottom", fill="x")

# Configure the canvas to use the scrollbar
canvas.configure(xscrollcommand=horizontal_scrollbar.set)

# Bind the canvas scrolling to the frame
def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas.bind("<Configure>", on_canvas_configure)


root.mainloop()
