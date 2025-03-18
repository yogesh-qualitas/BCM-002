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
            
            text_info = f"Name: {card[0]}\nOrganization: {card[1]}\nCompany: {card[2]}\nEmail: {card[3]}\nPhone: {card[4]}\nAddress: {card[5]}"
            tk.Label(details_window, text=text_info, justify=tk.LEFT, padx=10, pady=10).pack()
            
            if card[6]:
                img = Image.open(card[6])
                img = img.resize((250, 150))
                img = ImageTk.PhotoImage(img)
                panel = tk.Label(details_window, image=img)
                panel.image = img
                panel.pack()
    
    def create_widgets(self):
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        self.name_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Organization:").grid(row=1, column=0, padx=10, pady=5)
        self.org_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.org_var).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Company:").grid(row=2, column=0, padx=10, pady=5)
        self.company_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.company_var).grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Email:").grid(row=3, column=0, padx=10, pady=5)
        self.email_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.email_var).grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Phone:").grid(row=4, column=0, padx=10, pady=5)
        self.phone_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.phone_var).grid(row=4, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Address:").grid(row=5, column=0, padx=10, pady=5)
        self.address_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.address_var).grid(row=5, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Image:").grid(row=6, column=0, padx=10, pady=5)
        self.image_path = tk.StringVar()
        tk.Entry(self.root, textvariable=self.image_path, state="readonly", width=40).grid(row=6, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_image).grid(row=6, column=2, padx=10, pady=5)
        
        tk.Button(self.root, text="Add Business Card", command=self.add_card).grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Clear Fields", command=self.clear_fields).grid(row=7, column=2, pady=10)
        
        tk.Label(self.root, text="Saved Business Cards:").grid(row=8, column=0, padx=10, pady=5)
        self.listbox = tk.Listbox(self.root, width=50, height=10)
        self.listbox.grid(row=9, column=0, columnspan=3, padx=10, pady=5)
        self.listbox.bind("<Double-Button-1>", self.show_card_details)
        
        tk.Button(self.root, text="View All Cards", command=self.view_cards).grid(row=10, column=0, columnspan=3, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BusinessCardManager(root)
    root.mainloop()
