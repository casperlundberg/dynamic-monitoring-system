def parse_server_variables(servers_obj):
    """
    Parse the server variables from the servers object
    """
    server_variables = []
    for server in servers_obj:
        var = server.get("variables")
        if var is not None:
            server_variables.append(var)
    return server_variables


def replace_server_variables(server_url, server_variables):
    """
    Replace the server variables in the server URL
    """
    for variable in server_variables:
        server_url = server_url.replace(f"{{{variable}}}",
                                        server_variables[variable])
    return server_url


def parse_server_urls(servers_obj):
    """
    Parse the server URLs from the servers object
    """
    server_urls = []
    server_variables = parse_server_variables(servers_obj)
    for server in servers_obj:
        url = server.get("url")

        if not url.startswith("http"):
            raise ValueError(
                "Invalid URL, must be full URL. Current URL: " + url)

        if len(server_variables) > 0:
            parsed_url = replace_server_variables(url, server_variables)
        else:
            parsed_url = url

        server_urls.append(parsed_url)
    return server_urls
