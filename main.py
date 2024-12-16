import tkinter as tk
from tkinter import ttk, messagebox
from db import Database  # Assuming this is the database module that handles DB operations.

# Create a database connection
db = Database()

# Create the main application window
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("800x600")
root.config(bg="#2c3e50")

# Define StringVar for input variables
date = tk.StringVar()
category = tk.StringVar()
amount = tk.StringVar()
description = tk.StringVar()

# Create GUI components
frame = ttk.Frame(root, padding="10")
frame.pack(side=tk.TOP, fill=tk.X)

# Labels and Entry fields for expense data
ttk.Label(frame, text="Date (YYYY-MM-DD):", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_date = ttk.Entry(frame, textvariable=date, font=("Arial", 14))
entry_date.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="Category:", font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_category = ttk.Entry(frame, textvariable=category, font=("Arial", 14))
entry_category.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame, text="Amount:", font=("Arial", 14)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_amount = ttk.Entry(frame, textvariable=amount, font=("Arial", 14))
entry_amount.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame, text="Description:", font=("Arial", 14)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_description = ttk.Entry(frame, textvariable=description, font=("Arial", 14))
entry_description.grid(row=3, column=1, padx=5, pady=5)

# Buttons for adding, updating, deleting, and viewing expenses
def add_expense():
    if not date.get() or not category.get() or not amount.get():
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return
    db.insert(date.get(), category.get(), float(amount.get()), description.get())
    messagebox.showinfo("Success", "Expense added successfully!")
    clear_inputs()
    display_expenses()

def clear_inputs():
    date.set("")
    category.set("")
    amount.set("")
    description.set("")

def display_expenses():
    for row in tree.get_children():
        tree.delete(row)
    for expense in db.fetch_all():
        tree.insert("", "end", values=expense)

def delete_expense():
    if not tree.selection():
        messagebox.showerror("Selection Error", "Please select an expense to delete.")
        return
    selected_item = tree.selection()[0]
    expense_id = tree.item(selected_item)["values"][0]
    db.delete(expense_id)
    messagebox.showinfo("Success", "Expense deleted successfully!")
    display_expenses()

def update_expense():
    if not tree.selection():
        messagebox.showerror("Selection Error", "Please select an expense to update.")
        return
    selected_item = tree.selection()[0]
    expense_id = tree.item(selected_item)["values"][0]
    db.update(expense_id, date.get(), category.get(), float(amount.get()), description.get())
    messagebox.showinfo("Success", "Expense updated successfully!")
    display_expenses()

# Function to populate input fields when a row is selected
def on_item_selected(event):
    selected_item = tree.selection()
    if not selected_item:
        return  # No item selected
    
    selected_expense = tree.item(selected_item[0])["values"]
    if selected_expense:
        date.set(selected_expense[1])
        category.set(selected_expense[2])
        amount.set(selected_expense[3])
        description.set(selected_expense[4])

# Treeview for displaying expenses
tree = ttk.Treeview(root, columns=("ID", "Date", "Category", "Amount", "Description"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Date", text="Date")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")
tree.heading("Description", text="Description")
tree.pack(fill=tk.BOTH, expand=True)

# Bind the Treeview selection event to the on_item_selected function
tree.bind("<<TreeviewSelect>>", on_item_selected)

# Buttons for the operations
button_frame = ttk.Frame(root, padding="10")
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

ttk.Button(button_frame, text="Add Expense", command=add_expense).pack(side=tk.LEFT, padx=5, pady=5)
ttk.Button(button_frame, text="Update Expense", command=update_expense).pack(side=tk.LEFT, padx=5, pady=5)
ttk.Button(button_frame, text="Delete Expense", command=delete_expense).pack(side=tk.LEFT, padx=5, pady=5)
ttk.Button(button_frame, text="Clear Inputs", command=clear_inputs).pack(side=tk.LEFT, padx=5, pady=5)
ttk.Button(button_frame, text="View All Expenses", command=display_expenses).pack(side=tk.LEFT, padx=5, pady=5)

# Display existing expenses when the app starts
display_expenses()

# Run the application
if __name__ == "__main__":
    root.mainloop()
