# main.py

from monitoring_server.main_ms_server import run_monitoring_backend
from UI_dashboard.main_ui_server import run_monitoring_ui

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    run_monitoring_backend()
    run_monitoring_ui()
    # ui_app.run()

    print(
        "[Main] SQL/Endpoint server + Flask + UI server are running in background.")

    try:
        while True:
            cmd = input(">> ")
            if cmd.strip() == "exit":
                break
    except KeyboardInterrupt:
        print("Shutdown requested.")
