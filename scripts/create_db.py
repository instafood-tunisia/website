import sqlite3

con = sqlite3.connect("instafood.db")

cur = con.cursor()

query = """
CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_name TEXT,
  customer_address TEXT,
  customer_phonenumber TEXT,
  item_name TEXT,
  quantity INTEGER,
  price REAL,
  order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

cur.execute(query)

query = """
CREATE TABLE menu_items (
  id INTEGER PRIMARY KEY,
  item_name TEXT,
  item_category TEXT,
  description TEXT,
  image_url TEXT,
  price REAL
);
"""

cur.execute(query)

con.commit()

print("Done :)")