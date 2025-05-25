from fastapi import FastAPI, Request
import datetime

from dummy_api.ver0.models import TemperatureReading, EnergyReading
from instrumentor.fastAPI_instrumentation import instrument

app = FastAPI()


# Dummy Instrumentation Middleware
@app.middleware("http")
async def instrumentation_middleware(request: Request, call_next):
    # body = await request.json() if request.method in ["POST", "PUT"] else None
    await instrument(request)  # Placeholder function
    response = await call_next(request)
    return response


# IoT API Endpoints
@app.get("/temperature", response_model=TemperatureReading)
async def get_temperature():
    """ Simulated temperature sensor data """
    return {
        "device_id": "sensor-123",
        "timestamp": datetime.datetime.utcnow(),
        "temperature_celsius": 22.5
    }


@app.post("/temperature", response_model=TemperatureReading)
async def post_temperature(data: TemperatureReading):
    """ Simulated sensor sending temperature data """
    return data


@app.get("/energy", response_model=EnergyReading)
async def get_energy():
    """ Simulated energy meter data """
    return {
        "device_id": "meter-456",
        "timestamp": datetime.datetime.now(),
        "power_kw": 1.2,
        "energy_kwh": 500.5
    }


@app.post("/energy", response_model=EnergyReading)
async def post_energy(data: EnergyReading):
    """ Simulated meter sending energy usage data """
    return data
