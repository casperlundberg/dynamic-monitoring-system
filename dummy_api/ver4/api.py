import datetime

from fastapi import FastAPI, Request

if __name__ == "__main__":
    from models import TemperatureReading, EnergyReading, TemperatureValue
else:
    from dummy_api.ver4.models import TemperatureReading, \
        EnergyReading

from instrumentor.fastAPI_instrumentation import instrument

app = FastAPI()


@app.get("/temperature", response_model=TemperatureReading)
async def get_temperature():
    """ Simulated temperature sensor data with unit and value """
    return {
        "device_id": "sensor-123",
        "timestamp": datetime.datetime.now(),
        "temp": {
            "unit": "celsius",
            "value": 22.5
        }
    }


@app.post("/temperature", response_model=TemperatureReading)
async def post_temperature(request: Request):
    """ Simulated sensor sending temperature unit and value """
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

    uvicorn.run("dummy_api.ver4.api:app", host="0.0.0.0", port=8010,
                reload=True)
