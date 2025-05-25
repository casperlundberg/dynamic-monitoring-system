import psycopg2
import psycopg2.extras
from monitoring_server.db_singleton import db


def flatten_body(data: dict, parent_key: str = "", sep: str = "_") -> dict:
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_body(v, new_key, sep=sep).items())
        else:
            items.append((new_key.lower(), v))
    return dict(items)


def insert_into_timescaledb(message: dict):
    identifier = message["identifier"]
    timestamp = message["timestamp"]
    body = message["body"]

    # Flatten the body
    flat_body = flatten_body(body)

    # Combine timestamp and flattened body into one dictionary
    row_data = {
        "timestamp": timestamp,
        **flat_body
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
