import os
import json
import yaml
import sys

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
    ("array", None): "JSONB",  # Could be separate table in advanced version
}


def map_type(oatype, fmt):
    return OPENAPI_TO_PG.get((oatype, fmt)) or OPENAPI_TO_PG.get(
        (oatype, None)) or "TEXT"


def flatten_properties(properties, parent=""):
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


def generate_create_table(schema_name, schema):
    columns = [("timestamp", "TIMESTAMPTZ NOT NULL")]  # Default column
    properties = schema.get("properties", {})
    columns += flatten_properties(properties)
    col_sql = ",\n    ".join(f"{col} {typ}" for col, typ in columns)
    return f"CREATE TABLE IF NOT EXISTS {schema_name.lower()} (\n    {col_sql}\n);"


def load_openapi_file(path):
    with open(path) as f:
        if path.endswith(".yaml") or path.endswith(".yml"):
            return yaml.safe_load(f)
        elif path.endswith(".json"):
            return json.load(f)
        else:
            raise ValueError("Unsupported file type. Use .yaml or .json")


def main(filepath):
    print(f"\n📦 Parsing OpenAPI file: {filepath}\n")
    data = load_openapi_file(filepath)
    schemas = data.get("components", {}).get("schemas", {})
    if not schemas:
        print("⚠️ No schemas found in components.schemas.")
        return

    for name, schema in schemas.items():
        sql = generate_create_table(name, schema)
        print(f"🧱 SQL for `{name}`:\n{sql}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python openapi_to_sql_flat.py path/to/openapi.yaml")
    else:
        main(sys.argv[1])
