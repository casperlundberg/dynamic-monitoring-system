import hashlib
import json
from typing import Dict, Any
import instrumentor_config
import utils

from packages.identifier.identfier import create_identifier

# def instrument(method, path, timestamp, body):
#     """ Placeholder for future instrumentation logic (e.g., Kafka integration) """
#     # use hash to create identifier, load spec beforehand
#
#     ident = create_identifier({}, path, method)
#
#     print(f"Instrumenting: {method} {path} - Body: {body}")

from datetime import datetime
from email.utils import parsedate_to_datetime


async def instrument(request):
    try:
        payload = await request.json()
    except Exception:
        raise ValueError("Invalid JSON in request body")

    # Use HTTP Date header if available, else fallback to current UTC time
    date_header = request.headers.get("Date")
    try:
        timestamp = parsedate_to_datetime(
            date_header) if date_header else datetime.now()
    except Exception:
        timestamp = datetime.now()

    # Optionally extract method, path, headers, etc., if needed
    method = request.method
    path = request.url.path
    headers = dict(request.headers)

    # Use the identifier logic to create a unique identifier for this request
    spec = utils.get_spec_from_folder(config.PATH_TO_OPENAPI_SPEC)
    ident = create_identifier(spec, path, method)

    # send ident and payload to kafka
    # Placeholder for Kafka integration
    # send_to_kafka(ident, payload)
    print(f"Instrumenting: {method} {path} - Body: {payload}")
