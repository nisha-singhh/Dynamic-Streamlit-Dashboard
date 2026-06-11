import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Add profile_pic column
try:
    cursor.execute(
        "ALTER TABLE users ADD COLUMN profile_pic BLOB"
    )
    print("✅ profile_pic column added")
except Exception as e:
    print("profile_pic:", e)

# Add is_admin column
try:
    cursor.execute(
        "ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0"
    )
    print("✅ is_admin column added")
except Exception as e:
    print("is_admin:", e)

conn.commit()
conn.close()

print("Done!")
