import tkinter as tk
from tkinter import ttk, messagebox
import os

class LabelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Label Printing Automation Tool")
        
        # Combobox for selecting customer
        tk.Label(root, text="Select Customer:").grid(row=0, column=0)
        self.customer_var = tk.StringVar(root)
        self.customer_dropdown = ttk.Combobox(root, textvariable=self.customer_var)
        self.customer_dropdown.grid(row=0, column=1)
        self.customer_dropdown.bind('<<ComboboxSelected>>', self.update_label_sizes)
        self.customer_dropdown.bind('<MouseWheel>', self.on_mouse_wheel)

        # Combobox for selecting label size
        tk.Label(root, text="Select Label Size:").grid(row=1, column=0)
        self.label_size_var = tk.StringVar(root)
        self.label_size_dropdown = ttk.Combobox(root, textvariable=self.label_size_var)
        self.label_size_dropdown.grid(row=1, column=1)
        self.label_size_dropdown.bind('<MouseWheel>', self.on_mouse_wheel)

        # Entry for Job Ticket Number
        tk.Label(root, text="Job Ticket Number:").grid(row=2, column=0)
        self.job_ticket_entry = tk.Entry(root)
        self.job_ticket_entry.grid(row=2, column=1)

        # Entry for UPC Number
        tk.Label(root, text="UPC Number:").grid(row=3, column=0)
        self.upc_entry = tk.Entry(root)
        self.upc_entry.grid(row=3, column=1)

        # Button to execute tasks
        self.execute_button = tk.Button(root, text="Execute", command=self.find_folder)
        self.execute_button.grid(row=4, column=1, sticky=tk.W+tk.E)

        # Initialize the dropdown menus
        self.init_dropdowns()

    def init_dropdowns(self):
        # List directories at a given path for customers
        self.customer_dropdown['values'] = self.get_customers()

    def get_customers(self):
        base_path = "Z:\\3 Encoding and Printing Files\\Customers Encoding Files"
        try:
            return [dir for dir in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, dir))]
        except Exception as e:
            print(f"Error accessing customer directories: {str(e)}")
            return []

    def update_label_sizes(self, event=None):
        # Update label sizes based on selected customer
        customer = self.customer_var.get()
        base_path = f"Z:\\3 Encoding and Printing Files\\Customers Encoding Files\\{customer}"
        if customer:
            try:
                self.label_size_dropdown['values'] = [dir for dir in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, dir))]
                self.label_size_dropdown.set('')
            except Exception as e:
                print(f"Error accessing label size directories for {customer}: {str(e)}")
                self.label_size_dropdown['values'] = []
        else:
            self.label_size_dropdown['values'] = []

    def on_mouse_wheel(self, event):
        # Mouse wheel event for scrolling through Combobox options
        return "break"  # Prevents default Tkinter text scrolling behavior

    def find_folder(self):
        customer = self.customer_var.get()
        label_size = self.label_size_var.get()
        job_ticket_number = self.job_ticket_entry.get()
        base_path = f"Z:\\3 Encoding and Printing Files\\Customers Encoding Files\\{customer}\\{label_size}"
        try:
            folders = os.listdir(base_path)
            for folder in folders:
                # The job ticket number is the last part after the last dash '-'
                if folder.split('-')[-1].strip() == job_ticket_number:
                    messagebox.showinfo("Result", "Folder found: " + folder)
                    return
            messagebox.showinfo("Result", "Folder not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search directories: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LabelApp(root)
    root.mainloop()
