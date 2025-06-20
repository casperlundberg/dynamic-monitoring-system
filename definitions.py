import os

ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__))  # This is your Project Root

UI = "UI_dashboard"

GENERATED_CODE_FOLDER = "generated_code"
GENERATED_CODE_CLIENT_FOLDER = "clients"
GENERATED_CODE_MODEL_FOLDER = "models"

SAVED_OBJECTS_FOLDER = "saved_objects"
GENERATED_CODE_SAVED_CLIENTS_FOLDER = "saved_clients"
GENERATED_CODE_SAVED_MODELS_FOLDER = "saved_models"

GENERATED_CODE_UI_FOLDER = "ui"

CODE_GENERATION_FORMATTER = "PEP8"  # NOT IN USE

LEFT_PANEL_WIDTH = 500

SERVER_UPDATE_ENDPOINT_PORT = 8000  # FastAPI Update spec server
UI_PORT = 8002  # Monitoring UI

MS_SERVER_PORT = 8001  # Flask backend, generated endpoints
MS_SERVER_HOST = "http://192.168.1.74"  # Flask backend, generated endpoints
