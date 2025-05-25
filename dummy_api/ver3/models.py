import datetime

from pydantic import BaseModel


# IoT Sensor Data Models
class EnvironmentTemperature(BaseModel):
    temp_c: float


class InternalTemperature(BaseModel):
    temp_c: float


class TemperatureReading(BaseModel):
    device_id: str
    timestamp: datetime.datetime
    environment: EnvironmentTemperature
    internal: InternalTemperature


class EnergyReading(BaseModel):
    device_id: str
    timestamp: datetime.datetime
    power_kw: float
    energy_kwh: float
