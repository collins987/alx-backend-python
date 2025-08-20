#!/usr/bin/env python3
import sqlite3


class DatabaseConnection:
    """
    A context manager to handle database connections automatically
    """

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Open the database connection and return the cursor"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the cursor and connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Example usage: select all users
    with DatabaseConnection("mydatabase.db") as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
