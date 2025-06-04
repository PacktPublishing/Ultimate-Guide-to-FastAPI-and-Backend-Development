### Don't try to crack your head over
### the SQL queries if you don't want,
### as we won't write raw sql later on
import sqlite3

# 1. Make connection with database
connection = sqlite3.connect("sqlite.db")
# Get cursor to execute queries and fetch data
cursor = connection.cursor()

# 2. Create a table with columns
cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipment (
        id INTEGER PRIMARY KEY,
        content TEXT,
        weight REAL,
        status TEXT
    )
""")


# 3. Add shipment data
# Insert values in the table
cursor.execute("""
    INSERT INTO shipment
    VALUES (12701, 'metal gears', 12, 'placed')
""")
# Commit the change to the database
connection.commit()


# 4. Read a shipment by id
cursor.execute("""
    SELECT id, status FROM shipment
    WHERE content = 'metal gears'
""")
result = cursor.fetchone()
print(result)


# 5. Update a shipment
cursor.execute("""
    UPDATE shipment SET status = 'in_transit'
    WHERE id = 12701
""")
connection.commit()


# 6. Delete a shipment by id
cursor.execute("""
    DELETE FROM shipment
    WHERE id = 12701
""")
connection.commit()


# Delete table if needed
cursor.execute(" DROP TABLE shipment ")


# Finally, close the connection when done
connection.close()
