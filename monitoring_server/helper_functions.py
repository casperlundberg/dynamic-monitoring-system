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
        cur.execute(f'SELECT * FROM "{identifier}"')

        def generate():
            for row in cur.fetchall():
                yield json.dumps(row) + '\n'

        return generate()

    except psycopg2.Error as e:
        print("[DB Error]", e)
        if conn:
            conn.rollback()

        def error_stream():
            yield json.dumps({"error": str(e)}) + '\n'

        return error_stream()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
