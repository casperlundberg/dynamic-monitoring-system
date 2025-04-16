import asyncio
import os
import psycopg2
import uvicorn

from typing import Dict, Any

import definitions
from packages.recieve_spec_package.update import OpenAPIHandlerAPI
from packages.identifier.identfier import create_identifier

# Maps OpenAPI types + format to PostgreSQL types
OPENAPI_TO_PG = {
    ("string", None): "TEXT",
    ("string", "date-time"): "TIMESTAMPTZ",
    ("number", None): "DOUBLE PRECISION",
    ("integer", None): "INTEGER",
    ("integer", "int32"): "INTEGER",
    ("integer", "int64"): "BIGINT",
    ("boolean", None): "BOOLEAN",
    ("object", None): "JSONB",
    ("array", None): "JSONB",
}


def map_type(oatype: str, fmt: str) -> str:
    return OPENAPI_TO_PG.get((oatype, fmt)) or OPENAPI_TO_PG.get(
        (oatype, None)) or "TEXT"


def flatten_properties(properties: Dict[str, Any], parent: str = ""):
    fields = []
    for name, prop in properties.items():
        full_name = f"{parent}_{name}" if parent else name
        prop_type = prop.get("type")
        if prop_type == "object" and "properties" in prop:
            fields.extend(flatten_properties(prop["properties"], full_name))
        else:
            pg_type = map_type(prop_type, prop.get("format"))
            fields.append((full_name.lower(), pg_type))
    return fields


def generate_create_table(table_name: str, schema: Dict[str, Any]) -> str:
    base_columns = [("timestamp", "TIMESTAMPTZ NOT NULL")]
    properties = schema.get("properties", {})

    # Flatten and combine all columns
    all_columns = base_columns + flatten_properties(properties)

    # Remove duplicates based on column name, preserving first occurrence
    seen = set()
    unique_columns = []
    for name, typ in all_columns:
        if name not in seen:
            unique_columns.append((name, typ))
            seen.add(name)

    col_sql = ",\n    ".join(f"{col} {typ}" for col, typ in unique_columns)
    query = f"CREATE TABLE IF NOT EXISTS {table_name.lower()} (\n    {col_sql}\n);"
    return query


def table_exists(conn, table_name: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = %s
            );
        """, (table_name.lower(),))
        return cur.fetchone()[0]


def create_table_and_hypertable(conn, table_name: str, schema: Dict[str, Any]):
    if table_exists(conn, table_name):
        print(f"Table {table_name} already exists, skipping.")
        return

    with conn.cursor() as cur:
        print(f"Creating table: {table_name}")
        cur.execute(generate_create_table(table_name, schema))
        conn.commit()

        print(f"Creating hypertable for: {table_name}")
        query = f"""
            SELECT create_hypertable(
                '{table_name.lower()}',
                'timestamp',
                create_default_indexes => TRUE
            );
        """

        cur.execute(query)

        conn.commit()


def generate_sql(spec: Dict[str, Any]):
    paths = spec.get("paths", {})

    # if not schemas or not paths:
    #     print("No schemas or paths found in OpenAPI spec.")
    #     return

    conn_str = os.getenv("PG_CONNECTION")
    if not conn_str:
        print("Environment variable PG_CONNECTION is not set.")
        return

    conn = psycopg2.connect(conn_str)

    for path, methods in paths.items():
        for method, operation in methods.items():
            request_body = operation.get("requestBody", {})
            content = request_body.get("content", {})
            json_body = content.get("application/json", {})
            schema = json_body.get("schema")

            if not schema:
                continue

            # Handle dereferenced spec — schema should be the actual object
            if not isinstance(schema, dict) or "properties" not in schema:
                continue

            identifier = create_identifier(spec, path, method)

            create_table_and_hypertable(conn, identifier, schema)

    conn.close()
