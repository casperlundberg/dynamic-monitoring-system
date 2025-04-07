import hashlib
import json
from typing import Dict, Any

from packages.identifier.identfier import create_identifier


def instrument(method, path, headers, body):
    """ Placeholder for future instrumentation logic (e.g., Kafka integration) """
    # use hash to create identifier, load spec beforehand

    ident = create_identifier({}, path, method)

    print(f"Instrumenting: {method} {path} - Body: {body}")
