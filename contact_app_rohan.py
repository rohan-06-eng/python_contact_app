import tkinter as tk
from tkinter import messagebox, ttk

class ContactBook:
    def __init__(self, filename='contacts.txt'):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    name, phone = line.strip().split(',')
                    self.contacts.append({'name': name, 'phone': phone})
        except FileNotFoundError:
            pass

    def save_contacts(self):
        with open(self.filename, 'w') as file:
            for contact in self.contacts:
                file.write(f"{contact['name']},{contact['phone']}\n")

    def add_contact(self, name, phone):
        name_lower = name.lower()

        # Check for duplicates
        for contact in self.contacts:
            if contact['name'].lower() == name_lower:
                if messagebox.askyesno("Overwrite Contact", f"A contact with the name '{name}' already exists. Do you want to overwrite it?"):
                    contact['name'] = name
                    contact['phone'] = phone
                    self.save_contacts()
                    return True
                else:
                    return False

        self.contacts.append({'name': name, 'phone': phone})
        self.save_contacts()
        return True

    def delete_contact(self, name):
        name_lower = name.lower()
        self.contacts = [contact for contact in self.contacts if contact['name'].lower() != name_lower]
        self.save_contacts()

    def edit_contact(self, old_name, new_name, new_phone):
        old_name_lower = old_name.lower()
        new_name_lower = new_name.lower()

        # Check for duplicates during editing
        for contact in self.contacts:
            if contact['name'].lower() == new_name_lower and old_name_lower != new_name_lower:
                if messagebox.askyesno("Overwrite Contact", f"A contact with the name '{new_name}' already exists. Do you want to overwrite it?"):
                    contact['name'] = new_name
                    contact['phone'] = new_phone
                    self.save_contacts()
                    return True
                else:
                    return False

        for contact in self.contacts:
            if contact['name'].lower() == old_name_lower:
                contact['name'] = new_name
                contact['phone'] = new_phone
                self.save_contacts()
                break
        return True

    def search_contact(self, name):
        name_lower = name.lower()
        return [contact for contact in self.contacts if name_lower in contact['name'].lower()]

    def get_all_contacts(self):
        return self.contacts

class ContactBookApp:
    def __init__(self, root):
        self.contact_book = ContactBook()

        self.root = root
        self.root.title("Enhanced Contact Book")
        self.root.geometry("500x600")
        self.root.configure(bg='#ececec')

        # Title Label
        self.title_label = tk.Label(root, text="Contact Book", font=('Helvetica', 18, 'bold'), bg='#ececec', fg='#333')
        self.title_label.pack(pady=10)

        # Frame for Input Fields
        self.input_frame = tk.Frame(root, bg='#ececec')
        self.input_frame.pack(pady=10)

        # Name Label and Entry
        self.name_label = tk.Label(self.input_frame, text="Name", font=('Helvetica', 12), bg='#ececec', fg='#333')
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.name_entry = tk.Entry(self.input_frame, font=('Helvetica', 12), width=25)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Phone Label and Entry
        self.phone_label = tk.Label(self.input_frame, text="Phone", font=('Helvetica', 12), bg='#ececec', fg='#333')
        self.phone_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.phone_entry = tk.Entry(self.input_frame, font=('Helvetica', 12), width=25)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        # Buttons Frame
        self.button_frame = tk.Frame(root, bg='#ececec')
        self.button_frame.pack(pady=20)

        # Add Contact Button
        self.add_button = tk.Button(self.button_frame, text="Add", font=('Helvetica', 12), bg='#4CAF50', fg='#fff', width=10, command=self.add_contact)
        self.add_button.grid(row=0, column=0, padx=10)

        # Edit Contact Button
        self.edit_button = tk.Button(self.button_frame, text="Edit", font=('Helvetica', 12), bg='#FFC107', fg='#fff', width=10, command=self.edit_contact)
        self.edit_button.grid(row=0, column=1, padx=10)

        # Delete Contact Button
        self.delete_button = tk.Button(self.button_frame, text="Delete", font=('Helvetica', 12), bg='#f44336', fg='#fff', width=10, command=self.delete_contact)
        self.delete_button.grid(row=0, column=2, padx=10)

        # Contacts Table
        self.contacts_tree = ttk.Treeview(root, columns=("Name", "Phone"), show='headings', height=10)
        self.contacts_tree.heading("Name", text="Name")
        self.contacts_tree.heading("Phone", text="Phone")
        self.contacts_tree.column("Name", width=200)
        self.contacts_tree.column("Phone", width=200)
        self.contacts_tree.pack(pady=10)
        self.update_contacts_tree()

        # Bind the select event to update fields when a contact is selected
        self.contacts_tree.bind('<<TreeviewSelect>>', self.on_contact_select)

        # Search Bar
        self.search_frame = tk.Frame(root, bg='#ececec')
        self.search_frame.pack(pady=10)

        self.search_label = tk.Label(self.search_frame, text="Search", font=('Helvetica', 12), bg='#ececec', fg='#333')
        self.search_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.search_entry = tk.Entry(self.search_frame, font=('Helvetica', 12), width=25)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)

        self.search_button = tk.Button(self.search_frame, text="Search", font=('Helvetica', 12), bg='#2196F3', fg='#fff', command=self.search_contact)
        self.search_button.grid(row=0, column=2, padx=10)

        # Display All Contacts Button
        self.display_button = tk.Button(root, text="Display All Contacts", font=('Helvetica', 12), bg='#FF9800', fg='#fff', command=self.display_contacts)
        self.display_button.pack(pady=10)

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        if name and phone:
            if self.contact_book.add_contact(name, phone):
                messagebox.showinfo("Success", f"Contact {name} added successfully.")
                self.name_entry.delete(0, tk.END)
                self.phone_entry.delete(0, tk.END)
                self.update_contacts_tree()
        else:
            messagebox.showwarning("Input Error", "Please enter both name and phone number.")

    def edit_contact(self):
        selected_contact = self.contacts_tree.selection()
        if selected_contact:
            name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            if name and phone:
                old_name = self.contacts_tree.item(selected_contact[0])['values'][0]
                if self.contact_book.edit_contact(old_name, name, phone):
                    messagebox.showinfo("Success", f"Contact {old_name} updated to {name}.")
                    self.update_contacts_tree()
            else:
                messagebox.showwarning("Input Error", "Please enter both name and phone number.")
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to edit.")

    def delete_contact(self):
        selected_contact = self.contacts_tree.selection()
        if selected_contact:
            name = self.contacts_tree.item(selected_contact[0])['values'][0]
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name}?"):
                self.contact_book.delete_contact(name)
                messagebox.showinfo("Success", f"Contact {name} deleted successfully.")
                self.update_contacts_tree()
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")

    def on_contact_select(self, event):
        selected_contact = self.contacts_tree.selection()
        if selected_contact:
            name = self.contacts_tree.item(selected_contact[0])['values'][0]
            phone = self.contacts_tree.item(selected_contact[0])['values'][1]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, name)
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, phone)

    def search_contact(self):
        name = self.search_entry.get().strip()
        if name:
            found_contacts = self.contact_book.search_contact(name)
            self.update_contacts_tree(found_contacts)
        else:
            messagebox.showwarning("Input Error", "Please enter a name to search.")

    def display_contacts(self):
        self.update_contacts_tree()

    def update_contacts_tree(self, contacts=None):
        for i in self.contacts_tree.get_children():
            self.contacts_tree.delete(i)
        if contacts is None:
            contacts = self.contact_book.get_all_contacts()
        for contact in contacts:
            self.contacts_tree.insert("", "end", values=(contact['name'], contact['phone']))

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
