from typing import Dict, Any

from monitoring_server.SQL_generator.SQL_generator import map_type


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
