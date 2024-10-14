"""
Parser for the servers keyword in the OpenAPI specification.
"""
from typing import List, Dict, Any

from src.core.generators.openAPI.models.server import Server


def parse_servers(servers: List[Dict[str, Any]]) -> List[Server]:
    """
    Parse the servers keyword in the OpenAPI specification.

    Args: servers: List of servers in the OpenAPI specification.
    Returns: List of Server objects.
    """
    return [Server(**server) for server in servers]
