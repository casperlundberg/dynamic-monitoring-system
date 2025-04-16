import psycopg2
import psycopg2.extras
from monitoring_server.db_singleton import db


# Does this handle nested data? what about duplicated keys?
def insert_into_timescaledb(message: dict):
    identifier = message["identifier"]
    timestamp = message["timestamp"]
    body = message["body"]

    # Combine timestamp and body into one dictionary
    row_data = {
        "timestamp": timestamp,
        **body
    }

    columns = list(row_data.keys())
    values = list(row_data.values())

    column_sql = ", ".join(f'"{col}"' for col in columns)
    placeholder_sql = ", ".join(["%s"] * len(columns))

    query = f"""
        INSERT INTO "{identifier}" ({column_sql})
        VALUES ({placeholder_sql})
    """

    try:
        conn = db.connect()
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
        print(f"Inserted row into '{identifier}': {row_data}")
    except Exception as e:
        print(f"Failed to insert into '{identifier}': {e}")
    finally:
        if cur:
            cur.close()
