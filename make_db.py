import sqlite3
class MenuDB:
    def __init__(self, db_path="menu.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL
                )
            ''')
            conn.commit()
        print("🗄️ Menu database initialized.")

    def add_item(self, name, price, stock):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO menu (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
                conn.commit()
                print(f"✅ Added: {name}")
            except sqlite3.IntegrityError:
                print(f"❌ Item '{name}' already exists.")

    def get_all_items(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, price, stock FROM menu")
            return cursor.fetchall()

    def update_stock(self, name, new_stock):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE menu SET stock = ? WHERE name = ?", (new_stock, name))
            conn.commit()

    def get_stock(self, name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT stock FROM menu WHERE name = ?", (name,))
            result = cursor.fetchone()
            return result[0] if result else 0