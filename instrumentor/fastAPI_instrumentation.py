import json

from kafka import KafkaProducer

from instrumentor import instrumentor_config
from instrumentor import utils
from packages.identifier.identfier import create_identifier
from datetime import datetime
from email.utils import parsedate_to_datetime

from packages.recieve_spec_package import deref_clean


async def instrument(request):
    try:
        body = await request.json()
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
    spec = utils.get_spec_from_file(instrumentor_config.PATH_TO_OPENAPI_SPEC)
    cleaned_spec = deref_clean.clean_dereference(spec)

    ident = create_identifier(cleaned_spec, path, method)

    # send ident and payload to kafka
    # Placeholder for Kafka integration
    # send_to_kafka(ident, payload)
    message = {
        "identifier": ident,
        "body": body,
        "timestamp": timestamp.isoformat()
    }

    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    topic = "event-metrics"

    producer.send(topic, message)
    producer.flush()
    print(f"Sent message to '{topic}':", message)
