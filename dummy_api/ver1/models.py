import datetime

from pydantic import BaseModel


# IoT Sensor Data Models
class TemperatureReading(BaseModel):
    device_id: str
    timestamp: datetime.datetime
    temp_c: float  # Renamed from temperature_celsius


class EnergyReading(BaseModel):
    device_id: str
    timestamp: datetime.datetime
    power_kw: float
    energy_kwh: float
