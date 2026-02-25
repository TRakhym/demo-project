from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class SensorCreate(BaseModel):
    name: str
    lat: float
    lng: float

class ReadingCreate(BaseModel):
    sensor_id: int
    pm25: float
    pm10: float
    lat: float
    lng: float

class ReadingResponse(BaseModel):
    id: int
    sensor_id: int
    timestamp: datetime
    pm25: float
    pm10: float
    h3_index: str

class AggregateResponse(BaseModel):
    h3_index: str
    date: str
    avg_pm25: float
    avg_pm10: float
    reading_count: int