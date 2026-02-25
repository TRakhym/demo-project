from sqlalchemy.orm import Session
from models import AuditLog
from datetime import datetime

def log_action(db: Session, user_id: int, action: str, details: str):
    log = AuditLog(
        user_id=user_id,
        action=action,
        details=details,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()