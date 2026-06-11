import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO users
(username, email, password, first_name, last_name, is_admin)
VALUES (?, ?, ?, ?, ?, ?)
""",
(
    "admin",
    "admin@gmail.com",
    "admin123",
    "Admin",
    "User",
    1
))

conn.commit()
conn.close()

print("✅ Admin created")