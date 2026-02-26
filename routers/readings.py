from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Reading, AggregatedReading
from schemas import ReadingCreate, ReadingResponse
from auth import get_current_user
from services.h3_service import get_h3_index
from utils.audit import log_action
from datetime import datetime
from database import SessionLocal

router = APIRouter(prefix="/readings", tags=["readings"])

def update_aggregates(h3_index: str):
    db = SessionLocal()
    try:
        today = datetime.utcnow().date().isoformat()
        today_start = datetime.combine(datetime.utcnow().date(), datetime.min.time())
        
        readings = db.query(Reading).filter(
            Reading.h3_index == h3_index,
            Reading.timestamp >= today_start
        ).all()
        
        if not readings:
            return
        
        avg_pm25 = sum(r.pm25 for r in readings) / len(readings)
        avg_pm10 = sum(r.pm10 for r in readings) / len(readings)
        
        agg = db.query(AggregatedReading).filter(
            AggregatedReading.h3_index == h3_index,
            AggregatedReading.date == today
        ).first()
        
        if agg:
            agg.avg_pm25 = avg_pm25
            agg.avg_pm10 = avg_pm10
            agg.reading_count = len(readings)
        else:
            agg = AggregatedReading(
                h3_index=h3_index,
                date=today,
                avg_pm25=avg_pm25,
                avg_pm10=avg_pm10,
                reading_count=len(readings)
            )
            db.add(agg)
        
        db.commit()
        print(f"Aggregates updated for h3={h3_index}")
        
    finally:
        db.close()

@router.post("/", response_model=ReadingResponse)
def create_reading(
    reading: ReadingCreate,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "technician"]:
        raise HTTPException(403)
    
    h3_idx = get_h3_index(reading.lat, reading.lng)
    
    db_reading = Reading(
        sensor_id=reading.sensor_id,
        pm25=reading.pm25,
        pm10=reading.pm10,
        h3_index=h3_idx
    )
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    
    log_action(db, current_user.id, "CREATE_READING", 
               f"sensor={reading.sensor_id}, h3={h3_idx}, pm25={reading.pm25}")
    
    background_tasks.add_task(update_aggregates, h3_idx)
    return db_reading

@router.get("/")
def get_readings(
    h3_index: str = None, 
    current_user=Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "analyst"]:
        raise HTTPException(
            status_code=403, 
            detail="Only admin and analyst can view raw sensor data"
        )
    
    query = db.query(Reading)
    if h3_index:
        query = query.filter(Reading.h3_index == h3_index)
    return query.all()