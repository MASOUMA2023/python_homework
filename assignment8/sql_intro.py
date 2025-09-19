import sqlite3
import os

def create_tables(conn):
    conn.execute("PRAGMA foreign_keys = 1")

    conn.execute('''
        CREATE TABLE IF NOT EXISTS publishers(
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS magazines(
            id INTEGER PRIMARY KEY,
            title TEXT UNIQUE NOT NULL,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers(id)
            )''')    

    conn.execute('''
        CREATE TABLE IF NOT EXISTS subscribers(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL )''')


    conn.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions(
            id INTEGER PRIMARY KEY,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id) 
             )''')               
def add_publisher(conn, name):
    try:
        conn.execute("INSERT OR IGNORE INTO publishers (name) VALUES (?)", (name,))
    except sqlite3.Error as e:
        print(f"Error adding publisher '{name}': {e}")

def add_magazine(conn, title, publisher_name):
    try:
        cur = conn.execute("SELECT id FROM publishers WHERE name = ?", (publisher_name,))
        result = cur.fetchone()
        if result:
            publisher_id = result[0]
            conn.execute("INSERT OR IGNORE INTO magazines (title, publisher_id) VALUES (?, ?)", (title, publisher_id))
        else:
            print(f"Publisher '{publisher_name}' not found for magazine '{title}'")
   
    except sqlite3.Error as e:
        print(f"Error adding magazine '{title}': {e}")

def add_subscriber(conn, name, address):
    try: 
        cur = conn.execute("SELECT id FROM subscribers WHERE name = ? AND address = ?", (name, address))
        if cur.fetchone() is None:
            conn.execute("INSERT INTO subscribers (name, address) VALUES (?, ?)", (name, address))
    except sqlite3.Error as e:
        print(f"Error adding subscriber '{name}': {e}")

def add_subscription(conn, subscriber_name, subscriber_address, magazine_title, expiration_date):
    try:
        cur = conn.execute("SELECT id FROM subscribers WHERE name = ? AND address = ?", (subscriber_name, subscriber_address))
        sub_row = cur.fetchone()
        if not sub_row:
            print(f"Subscriber '{subscriber_name}' at '{subscriber_address}' not found.")
            return
        subscriber_id = sub_row[0] 
        cur = conn.execute("SELECT id FROM magazines WHERE title = ?", (magazine_title,))
        mag_row = cur.fetchone()
        if not mag_row:
            print(f"Magazine '{magazine_title}' not found.")
            return
        magazine_id = mag_row[0]
        cur = conn.execute('''
            SELECT id FROM subscriptions 
            WHERE subscriber_id = ? AND magazine_id = ? AND expiration_date = ?
        ''', (subscriber_id, magazine_id, expiration_date))

        if cur.fetchone() is None:
            conn.execute('''
                INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date)
                VALUES (?, ?, ?)
            ''', (subscriber_id, magazine_id, expiration_date))
    except sqlite3.Error as e:
        print(f"Error adding subscription: {e}")

try:
    with sqlite3.connect('../db/magazines.db') as conn:
        print("Connected to database.")
        create_tables(conn)

        add_publisher(conn, "Time Inc.")
        add_publisher(conn, "National Geographic Society")
        add_publisher(conn, "Condé Nast")

        add_magazine(conn, "Time", "Time Inc.")
        add_magazine(conn, "National Geographic", "National Geographic Society")
        add_magazine(conn, "The New Yorker", "Condé Nast")

        add_subscriber(conn, "Alice Johnson", "123 Maple Street")
        add_subscriber(conn, "Bob Smith", "456 Oak Avenue")
        add_subscriber(conn, "Alice Johnson", "123 Maple Street")
        add_subscriber(conn, "Charlie Brown", "789 Pine Road")


        add_subscription(conn, "Alice Johnson", "123 Maple Street", "Time", "2025-12-31")
        add_subscription(conn, "Bob Smith", "456 Oak Avenue", "National Geographic", "2026-06-30")
        add_subscription(conn, "Charlie Brown", "789 Pine Road", "The New Yorker", "2025-11-15")
        add_subscription(conn, "Charlie Brown", "789 Pine Road", "Time", "2025-10-10")


        conn.commit()
        print("All data inserted and committed.")

        print("\n--- All Subscribers ---")
        cur = conn.execute("SELECT * FROM subscribers")
        for row in cur.fetchall():
            print(row)

        print("\n--- All Magazines (Sorted by Title) ---")
        cur = conn.execute("SELECT * FROM magazines ORDER BY title ASC")
        for row in cur.fetchall():
            print(row)

        print("\n--- Magazines Published by 'Time Inc.' ---")
        cur = conn.execute('''
            SELECT magazines.id, magazines.title, publishers.name AS publisher_name
            FROM magazines
            JOIN publishers ON magazines.publisher_id = publishers.id
            WHERE publishers.name = ?
        ''', ('Time Inc.',))
        for row in cur.fetchall():
            print(row)



except sqlite3.Error as e:
    print(f"An error accured!:{e}")


