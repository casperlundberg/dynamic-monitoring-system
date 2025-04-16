import os
import psycopg2

PG_CONNECTION = os.getenv("PG_CONNECTION",
                          "postgres://postgres:VOVVE1a2s3d@localhost:5432/postgres")


class DB:
    def __init__(self):
        self.conn = None

    def connect(self):
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(PG_CONNECTION)
        return self.conn

    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()


db = DB()
