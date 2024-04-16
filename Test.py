import tkinter as tk
from tkinter import ttk, messagebox, font
import os

class LabelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Label Printing Automation Tool")
        self.root.geometry('600x300')  # Sets the initial size of the window

        # Setting a default font for the whole window
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=12)
        self.root.option_add("*Font", default_font)

        # Combobox for selecting customer
        tk.Label(root, text="Select Customer:").grid(row=0, column=0, padx=10, pady=10)
        self.customer_var = tk.StringVar(root)
        self.customer_dropdown = ttk.Combobox(root, textvariable=self.customer_var, width=40)
        self.customer_dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.customer_dropdown.bind('<<ComboboxSelected>>', self.update_label_sizes)
        self.customer_dropdown.bind('<MouseWheel>', self.on_mouse_wheel)

        # Combobox for selecting label size
        tk.Label(root, text="Select Label Size:").grid(row=1, column=0, padx=10, pady=10)
        self.label_size_var = tk.StringVar(root)
        self.label_size_dropdown = ttk.Combobox(root, textvariable=self.label_size_var, width=40)
        self.label_size_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.label_size_dropdown.bind('<MouseWheel>', self.on_mouse_wheel)

        # Entry for Job Ticket Number
        tk.Label(root, text="Job Ticket Number:").grid(row=2, column=0, padx=10, pady=10)
        self.job_ticket_entry = tk.Entry(root, width=43)
        self.job_ticket_entry.grid(row=2, column=1, padx=10, pady=10)

        # Entry for UPC Number
        tk.Label(root, text="UPC Number:").grid(row=3, column=0, padx=10, pady=10)
        self.upc_entry = tk.Entry(root, width=43)
        self.upc_entry.grid(row=3, column=1, padx=10, pady=10)

        # Button to execute tasks
        self.execute_button = tk.Button(root, text="Execute", command=self.find_folder)
        self.execute_button.grid(row=4, column=1, sticky=tk.W+tk.E, padx=10, pady=10)

        # Initialize the dropdown menus
        self.init_dropdowns()

    def init_dropdowns(self):
        self.customer_dropdown['values'] = self.get_customers()

    def get_customers(self):
        base_path = "Z:\\3 Encoding and Printing Files\\Customers Encoding Files"
        try:
            return [dir for dir in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, dir))]
        except Exception as e:
            print(f"Error accessing customer directories: {str(e)}")
            return []

    def update_label_sizes(self, event=None):
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
        return "break"

    def find_folder(self):
        customer = self.customer_var.get()
        label_size = self.label_size_var.get()
        job_ticket_number = self.job_ticket_entry.get()
        upc_number = self.upc_entry.get()
        base_path = f"Z:\\3 Encoding and Printing Files\\Customers Encoding Files\\{customer}\\{label_size}"
        
        try:
            folders = os.listdir(base_path)
            job_folder_found = False
            for folder in folders:
                if folder.split('-')[-1].strip() == job_ticket_number:
                    job_folder_path = os.path.join(base_path, folder)
                    job_folder_found = True
                    break

            if not job_folder_found:
                messagebox.showinfo("Result", "Job ticket folder not found")
                return

            # Search for UPC number within the job ticket folder
            upc_path = self.search_for_upc(job_folder_path, upc_number)
            if upc_path:
                os.startfile(upc_path)
                messagebox.showinfo("Result", f"UPC folder/file opened: {upc_path}")
            else:
                messagebox.showinfo("Result", "UPC folder/file not found")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to search directories: {str(e)}")

    def search_for_upc(self, path, upc_number):
        # Check if a folder or file contains the UPC number
        for name in os.listdir(path):
            if upc_number in name:
                return os.path.join(path, name)
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = LabelApp(root)
    root.mainloop()
