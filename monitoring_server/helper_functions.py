import json
import psycopg2
import psycopg2.extras

from monitoring_server.db_singleton import db


def get_response(identifier: str):
    conn = None
    cur = None
    try:
        conn = db.connect()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(f'SELECT * FROM "{identifier}";')
        rows = cur.fetchall()
        return json.dumps(rows, default=str)

    except psycopg2.Error as e:
        print("[DB Error]", e)
        if conn:
            conn.rollback()
        return json.dumps({"error": str(e)})

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
