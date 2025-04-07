import yaml
import json

OPENAPI_TO_PG = {
    ("string", None): "TEXT",
    ("string", "date-time"): "TIMESTAMPTZ",
    ("number", None): "DOUBLE PRECISION",
    ("integer", None): "INTEGER",
    ("boolean", None): "BOOLEAN",
    ("object", None): "JSONB",
    ("array", None): "JSONB"
}


def generate_create_table(schema_name, schema):
    columns = ["timestamp TIMESTAMPTZ NOT NULL"]  # default column
    properties = schema.get("properties", {})

    for prop, prop_schema in properties.items():
        oatype = prop_schema.get("type")
        fmt = prop_schema.get("format")
        pgtype = OPENAPI_TO_PG.get((oatype, fmt)) or OPENAPI_TO_PG.get(
            (oatype, None)) or "TEXT"
        columns.append(f"{prop} {pgtype}")

    cols = ",\n    ".join(columns)
    return f"CREATE TABLE IF NOT EXISTS {schema_name} (\n    {cols}\n);"


def parse_openapi(path):
    with open(path) as f:
        data = yaml.safe_load(f) if path.endswith(".yaml") else json.load(f)
    schemas = data.get("components", {}).get("schemas", {})
    for name, schema in schemas.items():
        print(generate_create_table(name.lower(), schema))
