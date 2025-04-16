import hashlib
import json
from typing import Dict, Any

MAX_IDENTIFIER_LENGTH = 63  # PostgreSQL/TimescaleDB limit


def create_identifier(spec: Dict[str, Any], path: str, method: str) -> str:
    hash_value = generate_hash(spec)
    base = f"{method.lower()}{path.replace('/', '_').replace('{', '').replace('}', '')}"
    identifier = f"{base}_{hash_value}"
    return identifier[:MAX_IDENTIFIER_LENGTH]


def generate_hash(spec: Dict[str, Any]) -> str:
    spec_str = json.dumps(spec, sort_keys=True)
    return hashlib.sha256(spec_str.encode('utf-8')).hexdigest()
