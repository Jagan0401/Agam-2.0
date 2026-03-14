from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.dependencies import get_db, get_admin_user
from app.models.user import User
from app.models.property import Property
from typing import List, Dict, Any
import json

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/stats")
def get_platform_stats(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Returns platform-wide metrics."""
    total_users = db.query(User).count()
    total_properties = db.query(Property).count()
    
    # Calculate average quality score
    avg_quality = db.query(func.avg(Property.quality_score)).scalar() or 0.0
    
    # Images processed (mocked based on properties, but could be more complex)
    images_processed = total_properties * 5 # avg 5 images per property
    
    return {
        "total_users": total_users,
        "total_properties": total_properties,
        "avg_quality_score": round(float(avg_quality), 1),
        "images_processed": f"{images_processed / 1000:.1f}K" if images_processed > 1000 else str(images_processed),
        "ai_accuracy": "94.2%", # Mocked analytical metric
        "uptime": "99.8%"
    }

@router.get("/users", response_model=List[Dict[str, Any]])
def get_all_users(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Lists all users."""
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "status": u.status
        } for u in users
    ]

@router.post("/users/{user_id}/status")
def toggle_user_status(user_id: int, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Toggles user status between active and suspended."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot suspend yourself")

    user.status = "suspended" if user.status == "active" else "active"
    db.commit()
    return {"status": "success", "new_status": user.status}

@router.get("/moderation")
def get_moderation_queue(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Returns properties flagged or pending moderation."""
    # For now, let's say all properties with moderation_status != 'approved'
    # Or specifically flagged items
    results = db.query(Property).filter(Property.moderation_status != "approved").all()
    
    parsed = []
    for p in results:
        parsed.append({
            "id": p.id,
            "property_id": p.property_id,
            "title": p.title,
            "location": p.location,
            "seller_id": p.owner_id,
            "reason": p.moderation_reason or "AI: Quality Check Required",
            "status": p.moderation_status,
            "submission_date": "Recent" # Could use a created_at field if added
        })
    return parsed

@router.post("/moderation/{prop_id}/action")
def moderate_property(prop_id: int, action: str, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Approve or Reject a property."""
    prop = db.query(Property).filter(Property.id == prop_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    if action == "approve":
        prop.moderation_status = "approved"
        prop.ai_verified = True
    elif action == "reject":
        prop.moderation_status = "rejected"
        prop.ai_verified = False
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
        
    db.commit()
    return {"status": "success", "moderation_status": prop.moderation_status}
