import asyncio
import threading

import uvicorn

import definitions
from UI_dashboard.ui import UI
from UI_dashboard.queue import shared_queue, update_event
from packages.recieve_spec_package.update import OpenAPIHandlerAPI

openapi_handler = OpenAPIHandlerAPI()


async def consume_spec():
    while True:
        spec = await openapi_handler.wait_for_spec()
        shared_queue.put(spec)
        update_event.set()


def start_fastapi_server():
    """Run FastAPI + consumer in an asyncio event loop inside a thread."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(consume_spec())
    config = uvicorn.Config(openapi_handler.app, host="0.0.0.0",
                            port=definitions.UI_PORT)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


def start_ui():
    """Starts the UI in a separate thread."""
    ui = UI()
    ui.mainloop()


def run_monitoring_ui():
    """Starts Flask autogenerated API and FastAPI update spec API in background threads."""

    # Start Flask in background thread
    ui_thread = threading.Thread(target=start_ui, daemon=True)
    ui_thread.start()

    # Start FastAPI in background thread with its own asyncio loop
    fastapi_thread = threading.Thread(target=start_fastapi_server, daemon=True)
    fastapi_thread.start()
