import sqlite3

conn = sqlite3.connect('./data/instafood.db', check_same_thread=False)
cur = conn.cursor()

class orders():
    def get_all():
        try:
            cur.execute("SELECT * FROM orders ORDER BY id DESC")
            response = cur.fetchall()
            return response
        except:
            return False
    def create(name, address, phonenumber, item_name, quantity, price):
        try:
            cur.execute("INSERT INTO orders (customer_name, customer_address, customer_phonenumber, item_name, quantity, price) VALUES (?, ?, ?, ?, ?, ?)",
            (str(name), str(address), str(phonenumber), str(item_name), int(quantity), int(price)))
            conn.commit()
            return True
        except:
            return False

class products():
    def get_all():
        try:
            cur.execute("SELECT * FROM menu_items")
            response = cur.fetchall()
            return response
        except:
            return False
    def get_by_id(id):
        try:
            cur.execute("SELECT * FROM menu_items WHERE id = ?", (id,))
            response = cur.fetchone()
            return response
        except:
            return False
    def create(item_name, item_category, description, image_url, price):
        cur.execute("INSERT INTO menu_items (item_name, item_category, description, image_url, price) VALUES (?, ?, ?, ?, ?)",
        (str(item_name), str(item_category), str(description), str(image_url), str(price)))
        conn.commit()
        return True
    def delete(id):
        try:
            cur.execute("DELETE FROM menu_items WHERE id = ?", (id,))
            conn.commit()
            return True
        except:
            return False