from tkinter import *
from tkinter.ttk import *
from sqlite3 import *
from tkinter import messagebox

class Managecontactsframe(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        s = Style()
        s.configure('TFrame', background = 'white')
        s.configure('TLabel', background = 'white', font = (None, 15))
        s.configure('TButton', font = (None, 15))

        self.pack(fill = BOTH, expand = TRUE)

        self.con = connect('mycontacts.db')
        self.cur = self.con.cursor()

        self.create_view_all_contacts_frame()

    def create_view_all_contacts_frame(self):
        self.view_all_contacts_frame = Frame(self)
        self.view_all_contacts_frame.place(relx = .5, rely = .5, anchor = CENTER)

        add_new_contact_button = Button(self.view_all_contacts_frame,
        text = "Add New Contact", width = 15,
        command = self.add_new_contact_button_click)
        add_new_contact_button.grid(row = 0, column = 0, columnspan = 2, sticky = E, pady = 10)

        name_label = Label(self.view_all_contacts_frame, text = "Name: ")
        name_label.grid(row = 1, column = 0)

        self.name_entry = Entry(self.view_all_contacts_frame, font = (None, 15), width = 42)
        self.name_entry.grid(row = 1, column = 1, pady = 10)
        self.name_entry.bind('<KeyRelease>', self.name_entry_key_release)
        
        self.view_all_contacts_treeview = Treeview(self.view_all_contacts_frame,
        columns = ('c1', 'c2', 'c3', 'c4'), show = 'headings')
        self.view_all_contacts_treeview.grid(row = 2, column = 0, columnspan = 2, pady = 10)
        self.view_all_contacts_treeview.heading('c1', text = "Name", anchor = W)
        self.view_all_contacts_treeview.heading('c2', text = "Phone Number", anchor = W)
        self.view_all_contacts_treeview.heading('c3', text = "Email Id", anchor = W)
        self.view_all_contacts_treeview.heading('c4', text = "City", anchor = W)
        self.view_all_contacts_treeview.column('c1', width = 170)
        self.view_all_contacts_treeview.column('c2', width = 120)
        self.view_all_contacts_treeview.column('c3', width = 150)
        self.view_all_contacts_treeview.column('c4', width = 100)
        self.view_all_contacts_treeview.bind('<<TreeviewSelect>>', self.create_update_delete_contact_frame)

        self.cur.execute("select * from Contact order by Name")
        self.fill_view_all_contacts_treeview()
    
    def fill_view_all_contacts_treeview(self):
        for contact in self.view_all_contacts_treeview.get_children():
            self.view_all_contacts_treeview.delete(contact)
            
        contacts = self.cur.fetchall()
        for contact in contacts:
            self.view_all_contacts_treeview.insert("", END, values = contact)

    def name_entry_key_release(self, event):
        self.cur.execute("select * from Contact where Name like ? order by Name",
        ("%" + self.name_entry.get() + "%",))
        self.fill_view_all_contacts_treeview()

    def add_new_contact_button_click(self):
        self.view_all_contacts_frame.destroy()
        self.add_new_contact_frame = Frame(self)
        self.add_new_contact_frame.place(relx = .5, rely = .5, anchor = CENTER)

        name_label = Label(self.add_new_contact_frame, text = "Name: ")
        name_label.grid(row = 0, column = 0, sticky = W)

        self.name_entry = Entry(self.add_new_contact_frame, width = 25, font = (None, 15))
        self.name_entry.grid(row = 0, column = 1, pady = 5)

        phone_number_label = Label(self.add_new_contact_frame, text = "Phone Number: ")
        phone_number_label.grid(row = 1, column = 0, sticky = W)

        self.phone_number_entry = Entry(self.add_new_contact_frame, width = 25,
        font = (None, 15))
        self.phone_number_entry.grid(row = 1, column = 1, pady = 5)

        email_id_label = Label(self.add_new_contact_frame, text = "Email Id: ")
        email_id_label.grid(row = 2, column = 0, sticky = W)

        self.email_id_entry = Entry(self.add_new_contact_frame, width = 25, font = (None, 15))
        self.email_id_entry.grid(row = 2, column = 1, pady = 5)

        city_label = Label(self.add_new_contact_frame, text = "City: ")
        city_label.grid(row = 3, column = 0, sticky = W)

        self.city_combobox = Combobox(self.add_new_contact_frame, width = 23,
        font = (None, 15), values = ("Greater Noida", "Noida", "Delhi", "Mumbai", "Banglore"))
        self.city_combobox.grid(row = 3, column = 1, pady = 5)

        add_button = Button(self.add_new_contact_frame, text = "Add", width = 25,
        command = self.add_button_click)
        add_button.grid(row = 4, column = 1, pady = 5)

    def add_button_click(self):
        self.cur.execute("select * from Contact where EmailId = ?", (self.email_id_entry.get(),))
        contact = self.cur.fetchone()
        if contact is None:
            self.cur.execute("insert into Contact values(?, ?, ?, ?)", (self.name_entry.get(),
            self.phone_number_entry.get(), self.email_id_entry.get(), self.city_combobox.get()))
            self.con.commit()
            messagebox.showinfo('Success Message', 'Contact details are saved successfully')
            self.add_new_contact_frame.destroy()
            self.create_view_all_contacts_frame()
        else:
            messagebox.showerror('Error Message', 'Contact details are already added')

    def create_update_delete_contact_frame(self, event):
        contact = self.view_all_contacts_treeview.item(self.view_all_contacts_treeview.selection())['values']
        self.view_all_contacts_frame.destroy()

        self.update_delete_contact_frame = Frame(self)
        self.update_delete_contact_frame.place(relx = .5, rely = .5, anchor = CENTER)

        name_label = Label(self.update_delete_contact_frame, text = "Name: ")
        name_label.grid(row = 0, column = 0, sticky = W)

        self.name_entry = Entry(self.update_delete_contact_frame, width = 25, font = (None, 15))
        self.name_entry.grid(row = 0, column = 1, pady = 5)
        self.name_entry.insert(END, contact[0])

        phone_number_label = Label(self.update_delete_contact_frame, text = "Phone Number: ")
        phone_number_label.grid(row = 1, column = 0, sticky = W)

        self.phone_number_entry = Entry(self.update_delete_contact_frame, width = 25,
        font = (None, 15))
        self.phone_number_entry.grid(row = 1, column = 1, pady = 5)
        self.phone_number_entry.insert(END, contact[1])

        email_id_label = Label(self.update_delete_contact_frame, text = "Email Id: ")
        email_id_label.grid(row = 2, column = 0, sticky = W)

        self.email_id_entry = Entry(self.update_delete_contact_frame, width = 25, font = (None, 15))
        self.email_id_entry.grid(row = 2, column = 1, pady = 5)
        self.email_id_entry.insert(END, contact[2])
        self.old_email_id = contact[2]

        city_label = Label(self.update_delete_contact_frame, text = "City: ")
        city_label.grid(row = 3, column = 0, sticky = W)

        self.city_combobox = Combobox(self.update_delete_contact_frame, width = 23,
        font = (None, 15), values = ("Greater Noida", "Noida", "Delhi", "Mumbai", "Banglore"))
        self.city_combobox.grid(row = 3, column = 1, pady = 5)
        self.city_combobox.set(contact[3])

        update_button = Button(self.update_delete_contact_frame, text = "Update", width = 15,
        command = self.update_button_click)
        update_button.grid(row = 4, column = 0, pady = 5, sticky = W)

        delete_button = Button(self.update_delete_contact_frame, text = "Delete", width = 15,
        command = self.delete_button_click)
        delete_button.grid(row = 4, column = 1, pady = 5, sticky = E)
        
    def update_button_click(self):
        self.cur.execute("update Contact set Name = ?, PhoneNumber = ?, EmailId = ?, City = ? where EmailId = ?",
        (self.name_entry.get(), self.phone_number_entry.get(), self.email_id_entry.get(), self.city_combobox.get(),
         self.old_email_id))
        self.con.commit()
        messagebox.showinfo("Success Message", "Contact details are updated successfully")
        self.update_delete_contact_frame.destroy()
        self.create_view_all_contacts_frame()

    def delete_button_click(self):
        if messagebox.askquestion("Confirmation Message", "Are you sure to delete?") == 'yes':
            self.cur.execute("delete from Contact where EmailId = ?", (self.old_email_id, ))
            self.con.commit()
            messagebox.showinfo("Success Message", "Contact details are deleted successfully")
        self.update_delete_contact_frame.destroy()
        self.create_view_all_contacts_frame()
        
        
        

        

        








        
