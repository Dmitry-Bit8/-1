import tkinter as tk
from tkinter import ttk, messagebox

from database import Database
from contact_dialog import ContactDialog


class PhoneBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Телефонный справочник")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        self.db = Database('phonebook.db')

        self.create_widgets()
        self.load_contacts()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Блок поиска
        search_frame = ttk.LabelFrame(self.root, text="Поиск", padding=10)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(search_frame, text="Поиск:").grid(row=0, column=0, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_contacts())
        self.search_entry.bind('<KP_Enter>', lambda e: self.search_contacts())

        ttk.Button(search_frame, text="Найти",
                   command=self.search_contacts).grid(row=0, column=2, padx=5)
        ttk.Button(search_frame, text="Сбросить",
                   command=self.reset_search).grid(row=0, column=3, padx=5)

        # Таблица контактов
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("id", "last_name", "first_name", "phone", "email")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("last_name", text="Фамилия")
        self.tree.heading("first_name", text="Имя")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="Email")

        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("last_name", width=150)
        self.tree.column("first_name", width=150)
        self.tree.column("phone", width=150)
        self.tree.column("email", width=200)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL,
                                  command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set) # type: ignore

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", lambda e: self.edit_contact())

        # Блок кнопок управления
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(button_frame, text="Добавить",
                   command=self.add_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Редактировать",
                   command=self.edit_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить",
                   command=self.delete_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Выход",
                   command=self.on_close).pack(side=tk.RIGHT, padx=5)

    # ---------- загрузка ----------

    def load_contacts(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for contact in self.db.get_all_contacts():
            self.tree.insert('', tk.END, values=contact)

    # ---------- добавление ----------

    def add_contact(self):
        dialog = ContactDialog(self.root, title="Добавить контакт")
        if dialog.result:
            self.db.add_contact(
                dialog.result['last_name'],
                dialog.result['first_name'],
                dialog.result['phone'],
                dialog.result['email'],
                dialog.result['address'],
                dialog.result['notes'],
            )
            self.load_contacts()
            messagebox.showinfo("Успех", "Контакт успешно добавлен")

    # ---------- редактирование ----------

    def edit_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Предупреждение",
                "Выберите контакт для редактирования"
            )
            return

        contact_id = self.tree.item(selected[0])['values'][0]
        row = self.db.get_contact_by_id(contact_id)

        contact_dict = {
            'last_name':  row[1],
            'first_name': row[2],
            'phone':      row[3],
            'email':      row[4] or '',
            'address':    row[5] or '',
            'notes':      row[6] or '',
        }

        dialog = ContactDialog(self.root, title="Редактировать контакт",
                               contact_data=contact_dict)
        if dialog.result:
            self.db.update_contact(
                contact_id,
                dialog.result['last_name'],
                dialog.result['first_name'],
                dialog.result['phone'],
                dialog.result['email'],
                dialog.result['address'],
                dialog.result['notes'],
            )
            self.load_contacts()
            messagebox.showinfo("Успех", "Контакт успешно обновлён")

    # ---------- удаление ----------

    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Предупреждение",
                "Выберите контакт для удаления"
            )
            return

        values = self.tree.item(selected[0])['values']
        contact_id, last_name, first_name = values[0], values[1], values[2]

        confirm = messagebox.askyesno(
            "Подтверждение",
            f"Удалить контакт {last_name} {first_name}?"
        )
        if confirm:
            self.db.delete_contact(contact_id)
            self.load_contacts()
            messagebox.showinfo("Успех", "Контакт успешно удалён")

    # ---------- поиск ----------

    def search_contacts(self):
        text = self.search_entry.get().strip()
        if not text:
            messagebox.showwarning(
                "Предупреждение",
                "Введите текст для поиска"
            )
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        contacts = self.db.search_contacts(text)
        for contact in contacts:
            self.tree.insert('', tk.END, values=contact)

        if not contacts:
            messagebox.showinfo("Информация", "Контакты не найдены")

    def reset_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_contacts()

    # ---------- закрытие ----------

    def on_close(self):
        self.db.close()
        self.root.destroy()
