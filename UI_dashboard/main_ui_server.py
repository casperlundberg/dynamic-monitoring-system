# main_ui_server.py

import asyncio
import threading
import uvicorn
import definitions

from packages.recieve_spec_package.update import OpenAPIHandlerAPI
from UI_dashboard.monitoringUI import MonitoringUI  # adjust if path differs

# Create a NEW OpenAPI handler just for the UI server
ui_handler = OpenAPIHandlerAPI()
ui = MonitoringUI(ui_handler)


def start_ui_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Start the async spec listener properly inside the event loop
    loop.create_task(ui.listen_for_specs())

    config = uvicorn.Config(ui_handler.app, host="0.0.0.0",
                            port=definitions.UI_PORT)
    server = uvicorn.Server(config)

    # Run Uvicorn inside this loop
    loop.run_until_complete(server.serve())


def start_ui_in_background():
    thread = threading.Thread(target=start_ui_server, daemon=True)
    thread.start()
