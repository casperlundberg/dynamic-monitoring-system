import datetime

from pydantic import BaseModel


# IoT Sensor Data Models
class TemperatureValue(BaseModel):
    unit: str
    value: float


class TemperatureReading(BaseModel):
    device_id: str
    timestamp: datetime.datetime
    temp: TemperatureValue


class EnergyReading(BaseModel):
    device_id: str
    timestamp: datetime.datetime
    power_kw: float
    energy_kwh: float
