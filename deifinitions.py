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

SERVER_UPDATE_ENDPOINT_PORT = 8000  # FastAPI for SQL+endpoint
MS_SERVER_PORT = 8001  # Flask backend
UI_PORT = 8002  # Monitoring UI

PG_HOST = "localhost"
PG_CONNECTION = "postgresql+psycopg2://postgres:password@localhost:5432/postgres"
