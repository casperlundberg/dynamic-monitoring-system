# main.py

from monitoring_server.main_ms_server import run_monitoring_backend
from UI_dashboard.main_ui_server import ui_app, start_ui_in_background

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    run_monitoring_backend()
    start_ui_in_background()
    ui_app.run()

    print(
        "[Main] SQL/Endpoint server + Flask + UI server are running in background.")

    try:
        while True:
            cmd = input(">> ")
            if cmd.strip() == "exit":
                break
    except KeyboardInterrupt:
        print("Shutdown requested.")
