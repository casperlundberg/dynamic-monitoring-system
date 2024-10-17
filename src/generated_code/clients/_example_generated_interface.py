# Imports can be added in __init__.py
# for the generated package folder
import requests

from src.generated_code.models.pet import Pet
from src.core.ui import ui

# server + path + parameters
url = "https://petstore3.swagger.io/api/v3" + "/pet/" + "2"

response = requests.get(url)
body = response.json()

# ensure the response is the expected one
pet = Pet(**body)

# metrics to be collected and monitored
metrics = {
    "response_time": response.elapsed.total_seconds(),
    "status_code": response.status_code,
    "content_type": response.headers["Content-Type"],
    "content_length": response.headers["Content-Length"],
}

# send the data to the ui
ui.update_metrics(metrics)
ui.update_pet(pet)
