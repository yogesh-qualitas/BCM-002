import csv
import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel

class BusinessCardManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Business Card Manager")
        self.filename = "business_cards.csv"
        self.fields = ["Name", "Organization", "Company", "Email", "Phone", "Address", "Image Path"]
        self.load_data()
        self.create_widgets()

    def load_data(self):
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.fields)

    def save_uploaded_image(self, image_path, save_dir="business_cards"): 
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        image_name = os.path.basename(image_path)
        save_path = os.path.join(save_dir, image_name)
        img = Image.open(image_path)
        img.save(save_path)
        return save_path
    
    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.image_path.set(file_path)
    
    def add_card(self):
        card_data = [
            self.name_var.get(),
            self.org_var.get(),
            self.company_var.get(),
            self.email_var.get(),
            self.phone_var.get(),
            self.address_var.get(),
            self.save_uploaded_image(self.image_path.get()) if self.image_path.get() else ""
        ]
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(card_data)
        messagebox.showinfo("Success", "Business card added successfully!")
        self.clear_fields()
    
    def clear_fields(self):
        self.name_var.set("")
        self.org_var.set("")
        self.company_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.address_var.set("")
        self.image_path.set("")
    
    def view_cards(self):
        self.listbox.delete(0, tk.END)
        with open(self.filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            self.cards = list(reader)
            for i, row in enumerate(self.cards):
                self.listbox.insert(tk.END, f"{row[0]} - {row[1]}")
    
    def show_card_details(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            card = self.cards[index]
            
            details_window = Toplevel(self.root)
            details_window.title("Business Card Details")
            
            fields_vars = [tk.StringVar(value=card[i]) for i in range(len(card))]
            entry_fields = []
            
            for i, field in enumerate(self.fields):
                tk.Label(details_window, text=field + ":").grid(row=i, column=0, padx=10, pady=5)
                entry = tk.Entry(details_window, textvariable=fields_vars[i])
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.config(state="readonly")
                entry_fields.append(entry)
            
            if card[6]:
                img = Image.open(card[6])
                img = img.resize((250, 150))
                img = ImageTk.PhotoImage(img)
                panel = tk.Label(details_window, image=img)
                panel.image = img
                panel.grid(row=len(self.fields), column=0, columnspan=2, pady=10)
            
            def enable_edit():
                for entry in entry_fields:
                    entry.config(state="normal")
                edit_button.config(state="disabled")
                save_button.config(state="normal")
            
            def save_changes():
                updated_data = [var.get() for var in fields_vars]
                self.cards[index] = updated_data
                with open(self.filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(self.fields)
                    writer.writerows(self.cards)
                messagebox.showinfo("Success", "Business card updated successfully!")
                details_window.destroy()
                self.view_cards()
            
            edit_button = tk.Button(details_window, text="Edit", command=enable_edit)
            edit_button.grid(row=len(self.fields) + 1, column=0, pady=10)
            
            save_button = tk.Button(details_window, text="Save", command=save_changes, state="disabled")
            save_button.grid(row=len(self.fields) + 1, column=1, pady=10)
    
    def create_widgets(self):
        tk.Label(self.root, text="Saved Business Cards:").grid(row=0, column=0, padx=10, pady=5)
        self.listbox = tk.Listbox(self.root, width=50, height=10)
        self.listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
        self.listbox.bind("<Double-Button-1>", self.show_card_details)
        
        tk.Button(self.root, text="View All Cards", command=self.view_cards).grid(row=2, column=0, columnspan=3, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BusinessCardManager(root)
    root.mainloop()
