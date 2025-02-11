import sqlite3
def init_db():
    conn = sqlite3.connect("menu.db")
    print("🗄️ Database created successfully!")
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
    conn.close()

def add_menu_item(name, price, stock):
    conn = sqlite3.connect("menu.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO menu (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        conn.commit()
        print(f"✅ Added: {name} - ${price} (Stock: {stock})")
    except sqlite3.IntegrityError:
        print(f"❌ Item '{name}' already exists.")
    conn.close()

def update_stock(name, new_stock):
    conn = sqlite3.connect("menu.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE menu SET stock = ? WHERE name = ?", (new_stock, name))
    conn.commit()
    conn.close()
    print(f"🔄 Stock updated for {name}: {new_stock} left.")

def remove_menu_item(name):
    conn = sqlite3.connect("menu.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    print(f"🗑️ Removed: {name}")

def get_menu():
    conn = sqlite3.connect("menu.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, stock FROM menu")
    items = cursor.fetchall()
    conn.close()
    return items

def check_availability(name):
    conn = sqlite3.connect("menu.db")
    cursor = conn.cursor()
    cursor.execute("SELECT stock FROM menu WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0 

init_db()

if __name__ == "__main__":
    add_menu_item("Burger", 5.99, 10)
    add_menu_item("Fries", 2.99, 15)
    add_menu_item("Soda", 1.99, 20)

    print("\n📜 Current Menu:")
    for item in get_menu():
        print(f"{item[0]} - ${item[1]} (Stock: {item[2]})")

    update_stock("Burger", 8)
    remove_menu_item("Soda")

    print("\n📜 Updated Menu:")
    for item in get_menu():
        print(f"{item[0]} - ${item[1]} (Stock: {item[2]})")
