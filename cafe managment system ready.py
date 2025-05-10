import tkinter as tk
from tkinter import messagebox, ttk

class CafeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Café Management System")
        self.root.geometry("600x600")  # Increased window size
        self.root.configure(bg="#f4a261")
        
        # Default menu items
        self.menu = {
            'Coffee': 50,
            'Tea': 30,
            'Sandwich': 100,
            'Cake': 80,
            'Juice': 60
        }
        self.order = {}
        
        self.create_widgets()

    def create_widgets(self):
        # Header
        tk.Label(self.root, text="Café Menu", font=("Arial", 18, "bold"), 
                bg="#f4a261", fg="white").pack(pady=10)
        
        # Create a scrollable frame for the menu
        container = tk.Frame(self.root, bg="#f4a261")
        container.pack(fill=tk.BOTH, expand=True, padx=20)
        
        self.canvas = tk.Canvas(container, bg="#e76f51", bd=5, relief=tk.RIDGE)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#e76f51")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.entries = {}
        self.display_menu_items()
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg="#f4a261")
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="Generate Bill", command=self.generate_bill, 
                 font=("Arial", 12, "bold"), bg="#2a9d8f", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Edit Menu", command=self.edit_menu, 
                 font=("Arial", 12, "bold"), bg="#e9c46a", fg="black", padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Clear Order", command=self.clear_order, 
                 font=("Arial", 12, "bold"), bg="#e76f51", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=5)

    def display_menu_items(self):
        # Clear existing menu items
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Display current menu items
        self.entries = {}
        for item, price in self.menu.items():
            row_frame = tk.Frame(self.scrollable_frame, bg="#e76f51")
            row_frame.pack(pady=5, padx=10, fill=tk.X)
            
            tk.Label(row_frame, text=f"{item}: ₹{price}", font=("Arial", 12, "bold"), 
                    bg="#e76f51", fg="white").pack(side=tk.LEFT)
            entry = tk.Entry(row_frame, width=5, font=("Arial", 12))
            entry.pack(side=tk.RIGHT, padx=10)
            self.entries[item] = entry

    def generate_bill(self):
        self.update_order()
        total = 0
        bill_details = "\n---- Bill ----\n"
        
        for item, quantity in self.order.items():
            price = self.menu[item] * quantity
            total += price
            bill_details += f"{item} x{quantity}: ₹{price}\n"
        
        bill_details += "----------------\n"
        bill_details += f"Total Bill: ₹{total}"
        
        if self.order:
            messagebox.showinfo("Bill", bill_details)
        else:
            messagebox.showwarning("No Order", "Please enter at least one item.")

    def edit_menu(self):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Menu")
        edit_window.geometry("500x500")
        edit_window.configure(bg="#f4a261")
        
        # Create a scrollable frame for the edit menu
        edit_container = tk.Frame(edit_window, bg="#f4a261")
        edit_container.pack(fill=tk.BOTH, expand=True, padx=20)
        
        edit_canvas = tk.Canvas(edit_container, bg="#e76f51", bd=5, relief=tk.RIDGE)
        edit_scrollbar = ttk.Scrollbar(edit_container, orient="vertical", command=edit_canvas.yview)
        edit_scrollable_frame = tk.Frame(edit_canvas, bg="#e76f51")
        
        edit_scrollable_frame.bind(
            "<Configure>",
            lambda e: edit_canvas.configure(
                scrollregion=edit_canvas.bbox("all")
            )
        )
        
        edit_canvas.create_window((0, 0), window=edit_scrollable_frame, anchor="nw")
        edit_canvas.configure(yscrollcommand=edit_scrollbar.set)
        
        edit_canvas.pack(side="left", fill="both", expand=True)
        edit_scrollbar.pack(side="right", fill="y")
        
        tk.Label(edit_window, text="Edit Menu Items", font=("Arial", 16, "bold"), 
                bg="#f4a261", fg="white").pack(pady=10)
        
        # Display current menu with remove buttons
        for item, price in self.menu.items():
            item_frame = tk.Frame(edit_scrollable_frame, bg="#e76f51")
            item_frame.pack(pady=5, padx=10, fill=tk.X)
            
            tk.Label(item_frame, text=f"{item}: ₹{price}", font=("Arial", 12), 
                    bg="#e76f51", fg="white").pack(side=tk.LEFT)
            
            tk.Button(item_frame, text="Remove", command=lambda i=item: self.remove_item(i, edit_window), 
                     font=("Arial", 10), bg="#e76f51", fg="white").pack(side=tk.RIGHT)
        
        # Frame for adding new items
        add_frame = tk.Frame(edit_window, bg="#f4a261")
        add_frame.pack(pady=15)
        
        tk.Label(add_frame, text="Add New Item:", font=("Arial", 12), 
                bg="#f4a261", fg="white").pack()
        
        name_frame = tk.Frame(add_frame, bg="#f4a261")
        name_frame.pack(pady=5)
        tk.Label(name_frame, text="Name:", font=("Arial", 10), bg="#f4a261").pack(side=tk.LEFT)
        self.new_item_name = tk.Entry(name_frame, font=("Arial", 10))
        self.new_item_name.pack(side=tk.RIGHT)
        
        price_frame = tk.Frame(add_frame, bg="#f4a261")
        price_frame.pack(pady=5)
        tk.Label(price_frame, text="Price:", font=("Arial", 10), bg="#f4a261").pack(side=tk.LEFT)
        self.new_item_price = tk.Entry(price_frame, font=("Arial", 10))
        self.new_item_price.pack(side=tk.RIGHT)
        
        tk.Button(add_frame, text="Add Item", command=self.add_new_item, 
                 font=("Arial", 10), bg="#2a9d8f", fg="white").pack(pady=10)
        
        tk.Button(edit_window, text="Done", command=edit_window.destroy, 
                 font=("Arial", 12), bg="#2a9d8f", fg="white", padx=10).pack(pady=10)

    def remove_item(self, item, window):
        del self.menu[item]
        self.display_menu_items()  # Refresh the main menu display
        messagebox.showinfo("Removed", f"{item} has been removed from the menu.")
        window.destroy()
        self.edit_menu()  # Reopen the edit window to show updated menu

    def add_new_item(self):
        name = self.new_item_name.get().strip()
        price = self.new_item_price.get().strip()
        
        if not name:
            messagebox.showwarning("Error", "Please enter an item name")
            return
        
        if not price.isdigit() or int(price) <= 0:
            messagebox.showwarning("Error", "Please enter a valid positive price")
            return
        
        self.menu[name] = int(price)
        self.display_menu_items()  # Refresh the main menu display
        self.new_item_name.delete(0, tk.END)
        self.new_item_price.delete(0, tk.END)
        messagebox.showinfo("Added", f"{name} has been added to the menu for ₹{price}")

    def update_order(self):
        self.order.clear()
        for item, entry in self.entries.items():
            quantity = entry.get()
            if quantity.isdigit() and int(quantity) > 0:
                self.order[item] = int(quantity)

    def clear_order(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.order.clear()
        messagebox.showinfo("Order Cleared", "Your order has been reset.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CafeManagementSystem(root)
    root.mainloop()