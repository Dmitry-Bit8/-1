import tkinter as tk
from tkinter import ttk, messagebox


class ContactDialog:
    def __init__(self, parent, title="Добавить контакт", contact_data=None):
        self.parent = parent
        self.result = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("420x460")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # 1) Сначала кнопки — фиксируются внизу
        self.create_buttons()
        # 2) Затем поля ввода
        self.create_fields(contact_data)

        # Центрирование над родителем
        self.dialog.update_idletasks()
        px = parent.winfo_rootx() + (parent.winfo_width() // 2) - 210
        py = parent.winfo_rooty() + (parent.winfo_height() // 2) - 230
        self.dialog.geometry(f"+{px}+{py}")

        self.dialog.wait_window()

    def create_buttons(self):
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        ttk.Button(button_frame, text="Сохранить",
                   command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена",
                   command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def create_fields(self, contact_data):
        fields_frame = ttk.Frame(self.dialog, padding=10)
        fields_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        ttk.Label(fields_frame, text="Фамилия:").grid(
            row=0, column=0, sticky=tk.W, pady=4)
        self.last_name_entry = ttk.Entry(fields_frame, width=30)
        self.last_name_entry.grid(row=0, column=1, pady=4)

        ttk.Label(fields_frame, text="Имя:").grid(
            row=1, column=0, sticky=tk.W, pady=4)
        self.first_name_entry = ttk.Entry(fields_frame, width=30)
        self.first_name_entry.grid(row=1, column=1, pady=4)

        ttk.Label(fields_frame, text="Телефон:").grid(
            row=2, column=0, sticky=tk.W, pady=4)
        self.phone_entry = ttk.Entry(fields_frame, width=30)
        self.phone_entry.grid(row=2, column=1, pady=4)

        ttk.Label(fields_frame, text="Email:").grid(
            row=3, column=0, sticky=tk.W, pady=4)
        self.email_entry = ttk.Entry(fields_frame, width=30)
        self.email_entry.grid(row=3, column=1, pady=4)

        ttk.Label(fields_frame, text="Адрес:").grid(
            row=4, column=0, sticky=tk.W, pady=4)
        self.address_entry = ttk.Entry(fields_frame, width=30)
        self.address_entry.grid(row=4, column=1, pady=4)

        ttk.Label(fields_frame, text="Заметки:").grid(
            row=5, column=0, sticky=tk.NW, pady=4)
        self.notes_text = tk.Text(fields_frame, width=30, height=6)
        self.notes_text.grid(row=5, column=1, pady=4)

        if contact_data is not None:
            self.last_name_entry.insert(0, contact_data.get('last_name', ''))
            self.first_name_entry.insert(0, contact_data.get('first_name', ''))
            self.phone_entry.insert(0, contact_data.get('phone', ''))
            self.email_entry.insert(0, contact_data.get('email', ''))
            self.address_entry.insert(0, contact_data.get('address', ''))
            self.notes_text.delete('1.0', tk.END)
            self.notes_text.insert('1.0', contact_data.get('notes', ''))

    def save(self):
        last_name = self.last_name_entry.get().strip()
        first_name = self.first_name_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not last_name or not first_name or not phone:
            messagebox.showerror(
                "Ошибка",
                "Заполните обязательные поля: Фамилия, Имя, Телефон"
            )
            return

        self.result = {
            'last_name': last_name,
            'first_name': first_name,
            'phone': phone,
            'email': self.email_entry.get().strip(),
            'address': self.address_entry.get().strip(),
            'notes': self.notes_text.get('1.0', tk.END).strip(),
        }
        self.dialog.destroy()
