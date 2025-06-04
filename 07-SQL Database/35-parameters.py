import sqlite3

connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()

### Parameters
id = 12701
status = "placed"

### 1. Postional Parameters
cursor.execute("""
    UPDATE shipment SET status = ?
    WHERE id = ?
""",
    (status, id),
)

### 2. Parameters with keys
cursor.execute("""
    UPDATE shipment SET status = :status
    WHERE id > :id
""",
    { "status": status, "id": id },
)

connection.commit()


# Close connection
connection.close()