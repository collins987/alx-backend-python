#!/usr/bin/env python3
import sqlite3


class ExecuteQuery:
    """
    Context manager that executes a query with parameters
    """

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or []
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open connection, execute query, and fetch results"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close resources"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery("mydatabase.db", query, [25]) as results:
        print(results)
