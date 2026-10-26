import sqlite3


class Database:
    def __init__(self, db_name='phonebook.db'):
        """Инициализация подключения к базе данных."""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()

    def connect(self):
        """Подключение к базе данных."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        """Создание таблицы контактов, если она не существует."""
        assert self.cursor is not None
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_name TEXT NOT NULL,
                first_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        assert self.conn is not None
        self.conn.commit()

    # ---------- CRUD ----------

    def add_contact(self, last_name, first_name, phone,
                    email='', address='', notes=''):
        """Добавление нового контакта. Возвращает id новой записи."""
        assert self.cursor is not None
        self.cursor.execute('''
            INSERT INTO contacts (last_name, first_name, phone, email, address, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (last_name, first_name, phone, email, address, notes))
        assert self.conn is not None
        self.conn.commit()
        assert self.cursor is not None
        return self.cursor.lastrowid

    def get_all_contacts(self):
        """Получение всех контактов (для таблицы)."""
        assert self.cursor is not None
        self.cursor.execute('''
            SELECT id, last_name, first_name, phone, email
            FROM contacts
            ORDER BY last_name, first_name
        ''')
        assert self.cursor is not None
        return self.cursor.fetchall()

    def get_contact_by_id(self, contact_id):
        """Получение полной записи контакта по ID."""
        assert self.cursor is not None
        self.cursor.execute(
            'SELECT * FROM contacts WHERE id = ?', (contact_id,)
        )
        assert self.cursor is not None
        return self.cursor.fetchone()

    def update_contact(self, contact_id, last_name, first_name, phone,
                       email='', address='', notes=''):
        """Обновление контакта."""
        assert self.cursor is not None
        self.cursor.execute('''
            UPDATE contacts
            SET last_name = ?, first_name = ?, phone = ?,
                email = ?, address = ?, notes = ?
            WHERE id = ?
        ''', (last_name, first_name, phone,
              email, address, notes, contact_id))
        assert self.conn is not None
        self.conn.commit()

    def delete_contact(self, contact_id):
        """Удаление контакта."""
        assert self.cursor is not None
        self.cursor.execute(
            'DELETE FROM contacts WHERE id = ?', (contact_id,)
        )
        assert self.conn is not None
        self.conn.commit()

    def search_contacts(self, search_text):
        """Поиск контактов по фамилии, имени или телефону."""
        pattern = f'%{search_text}%'
        assert self.cursor is not None
        self.cursor.execute('''
            SELECT id, last_name, first_name, phone, email
            FROM contacts
            WHERE last_name  LIKE ?
               OR first_name LIKE ?
               OR phone      LIKE ?
            ORDER BY last_name, first_name
        ''', (pattern, pattern, pattern))
        assert self.cursor is not None
        return self.cursor.fetchall()

    # ---------- служебное ----------

    def close(self):
        """Безопасное закрытие соединения (idempotent)."""
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def __del__(self):
        self.close()
