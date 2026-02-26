from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Sensor
from schemas import SensorCreate
from auth import get_current_user
from services.h3_service import get_h3_index

router = APIRouter(prefix="/sensors", tags=["sensors"])

@router.post("/", response_model=dict)
def create_sensor(
    sensor: SensorCreate, 
    current_user=Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create sensors")
    
    h3_idx = get_h3_index(sensor.lat, sensor.lng)
    
    db_sensor = Sensor(
        name=sensor.name,
        lat=sensor.lat,
        lng=sensor.lng,
        h3_index=h3_idx
    )
    
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    
    print(f"Sensor created, id={db_sensor.id}, h3={h3_idx}")
    return {
        "id": db_sensor.id,
        "name": db_sensor.name,
        "lat": db_sensor.lat,
        "lng": db_sensor.lng,
        "h3_index": db_sensor.h3_index
    }