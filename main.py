from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import auth, sensors, readings, aggregates

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Air Quality Monitoring System - Almaty")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(sensors.router)
app.include_router(readings.router)
app.include_router(aggregates.router)

@app.get("/")
def root():
    return {"message": "Air Quality Monitoring System с H3 индексацией запущен!"}