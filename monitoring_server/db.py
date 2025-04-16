# db.py

import os
import psycopg2
from psycopg2 import pool

# Update this if you use dotenv or other config
PG_CONNECTION = os.getenv("PG_CONNECTION")


class Database:
    def __init__(self):
        self.pool = None

    def connect(self, minconn=1, maxconn=10):
        if self.pool is None:
            self.pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn,
                                                           dsn=PG_CONNECTION)
            print("[DB] Connection pool created")

    def get_conn(self):
        if self.pool is None:
            raise RuntimeError("Connection pool is not initialized")
        return self.pool.getconn()

    def release_conn(self, conn):
        if self.pool:
            self.pool.putconn(conn)

    def close_all(self):
        if self.pool:
            self.pool.closeall()
            print("[DB] All connections closed")


# Export a global instance
db = Database()
