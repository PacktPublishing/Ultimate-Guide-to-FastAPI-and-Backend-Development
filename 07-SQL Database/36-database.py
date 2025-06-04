import sqlite3
from contextlib import contextmanager
from typing import Any

from app.schemas import ShipmentCreate, ShipmentUpdate  # type: ignore


class Database:
    def connect_to_db(self):
        # Make connection with database
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        # Get cursor to execute queries and fetch data
        self.cur = self.conn.cursor()
        print("connected to sqlite.db ...")

    def create_table(self):
        # Create a table with columns
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT
            )
        """)

    def create(self, shipment: ShipmentCreate) -> int:
        # Find a new id
        self.cur.execute("SELECT MAX(id) FROM shipment")
        result = self.cur.fetchone()

        new_id = result[0] + 1

        # Insert values in the table
        self.cur.execute("""
            INSERT INTO shipment
            VALUES (:id, :content, :weight, :status)
        """,
            {
                "id": new_id,
                **shipment.model_dump(),
                "status": "placed",
            }
        )
        # Commit the change to the database
        self.conn.commit()

        return new_id

    def get(self, id: int) -> dict[str, Any] | None:
        self.cur.execute("""
            SELECT * FROM shipment
            WHERE id = ?
        """, (id, ))
        row = self.cur.fetchone()

        return {
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "status": row[3],
        } if row else None
    
    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any]:
        self.cur.execute("""
            UPDATE shipment SET status = :status
            WHERE id = :id
        """, 
            {   
                "id": id,
                **shipment.model_dump()
            }
        )
        self.conn.commit()

        return self.get(id)
    
    def delete(self, id: int):
        self.cur.execute("""
            DELETE FROM shipment
            WHERE id = ?
        """, (id, ))
        self.conn.commit()

    def close(self):
        print("...connection closed")
        self.conn.close()

    def __enter__(self):
        print("enter the context")
        self.connect_to_db()
        self.create_table()
        return self
    
    def __exit__(self, *arg):
        print("exiting the context")
        self.close()


# Usage: Class Methods
with Database() as db:
    print(db.get(12701))
    print(db.get(12702))


# Usage: @contextmanager
@contextmanager
def managed_db():
    db = Database()
    # Setup
    print("enter setup")
    db.connect_to_db()
    db.create_table()

    yield db

    print("exit the context")
    # Dispose
    db.close()


with managed_db() as db:
    print(db.get(12703))
    print(db.get(12704))