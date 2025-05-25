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
