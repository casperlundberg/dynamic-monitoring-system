import hashlib
import json
from typing import Dict, Any


def create_identifier(spec: Dict[str, Any], path: str, method: str) -> str:
    hash_value = generate_hash(spec)
    return f"{method.lower()}{path.replace('/', '_').replace('{', '').replace('}', '')}_{hash_value}"[
           0:]


def generate_hash(spec: Dict[str, Any]) -> str:
    spec_str = json.dumps(spec, sort_keys=True)
    return hashlib.sha256(spec_str.encode('utf-8')).hexdigest()
