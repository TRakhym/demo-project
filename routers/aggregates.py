from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from models import AggregatedReading

router = APIRouter(prefix="/aggregates", tags=["aggregates"])

@router.get("/")
def get_aggregates(
    h3_index: str = None, 
    current_user=Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "analyst"]:
        raise HTTPException(
            status_code=403, 
            detail="Only admin and analyst can view H3 zone analytics"
        )
    
    query = db.query(AggregatedReading)
    if h3_index:
        query = query.filter(AggregatedReading.h3_index == h3_index)
    return query.all()