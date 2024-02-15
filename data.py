import sqlite3

conn = sqlite3.connect('clients.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS compte (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        identifiant TEXT NOT NULL,
        mot_de_passe TEXT NOT NULL
    )
''')

cursor.execute("ALTER TABLE compte ADD COLUMN verification_code TEXT;")
cursor.execute("ALTER TABLE compte ADD COLUMN verification_expiry DATETIME;")


conn.commit()
conn.close()
