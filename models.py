from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)

class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    lat = Column(Float)
    lng = Column(Float)
    h3_index = Column(String, index=True)
    installed_at = Column(DateTime, default=datetime.utcnow)

class Reading(Base):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    pm25 = Column(Float)
    pm10 = Column(Float)
    h3_index = Column(String, index=True)

class AggregatedReading(Base):
    __tablename__ = "aggregated_readings"
    id = Column(Integer, primary_key=True, index=True)
    h3_index = Column(String, index=True)
    date = Column(String, index=True)
    avg_pm25 = Column(Float)
    avg_pm10 = Column(Float)
    reading_count = Column(Integer)

class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    action = Column(String)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)