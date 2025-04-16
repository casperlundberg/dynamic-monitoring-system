# main.py

from monitoring_server.main_ms_server import run_monitoring_backend
from UI_dashboard.main_ui_server import start_ui_in_background

if __name__ == "__main__":
    run_monitoring_backend()
    start_ui_in_background()

    print(
        "[Main] SQL/Endpoint server + Flask + UI server are running in background.")

    try:
        while True:
            cmd = input(">> ")
            if cmd.strip() == "exit":
                break
    except KeyboardInterrupt:
        print("Shutdown requested.")
