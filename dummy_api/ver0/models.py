import datetime

from pydantic import BaseModel


# IoT Sensor Data Models
class TemperatureReading(BaseModel):
    device_id: str
    timestamp: datetime.datetime
    temperature_celsius: float


class EnergyReading(BaseModel):
    device_id: str
    timestamp: datetime.datetime
    power_kw: float
    energy_kwh: float
