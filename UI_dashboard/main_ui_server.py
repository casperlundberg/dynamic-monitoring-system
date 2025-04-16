import asyncio
import threading
import uvicorn
import definitions

from packages.recieve_spec_package.update import OpenAPIHandlerAPI
from UI_dashboard.desktop_ui import MonitoringUIDesktop

ui_handler = OpenAPIHandlerAPI()
ui_app = MonitoringUIDesktop(ui_handler)


def start_ui_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    config = uvicorn.Config(ui_handler.app, host="0.0.0.0",
                            port=definitions.UI_PORT)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


def start_ui_in_background():
    thread = threading.Thread(target=start_ui_server, daemon=True)
    thread.start()
