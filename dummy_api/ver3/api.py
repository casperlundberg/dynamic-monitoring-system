import datetime

from fastapi import FastAPI, Request

if __name__ == "__main__":
    from models import TemperatureReading, EnergyReading, \
        EnvironmentTemperature, InternalTemperature
else:
    from dummy_api.ver3.models import TemperatureReading, \
        EnergyReading

from instrumentor.fastAPI_instrumentation import instrument

app = FastAPI()


@app.get("/temperature", response_model=TemperatureReading)
async def get_temperature():
    """ Simulated temperature sensor data with environment and internal temps """
    return {
        "device_id": "sensor-123",
        "timestamp": datetime.datetime.now(),
        "environment": {
            "temp_c": 22.5
        },
        "internal": {
            "temp_c": 45.0
        }
    }


@app.post("/temperature", response_model=TemperatureReading)
async def post_temperature(request: Request):
    """ Simulated sensor sending environment and internal temps """
    await instrument(request)
    return await request.json()


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
async def post_energy(request: Request):
    """ Simulated meter sending energy usage data """
    await instrument(request)
    return await request.json()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("dummy_api.ver3.api:app", host="0.0.0.0", port=8010,
                reload=True)
