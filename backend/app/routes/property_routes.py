from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.property import Property
from app.models.user import User

router = APIRouter(prefix="/properties", tags=["Properties"])

import json
def parse_property(p):
    return {
        "id": p.id,
        "property_id": p.property_id,
        "owner_id": p.owner_id,
        "title": p.title,
        "location": p.location,
        "price": p.price,
        "bhk": p.bhk,
        "sqft": p.sqft,
        "furnishing": p.furnishing,
        "image": p.image,
        "quality_score": p.quality_score,
        "room_type": p.room_type,
        "ai_verified": p.ai_verified,
        "tags": json.loads(p.tags) if p.tags else [],
        "detections": json.loads(p.detections) if p.detections else [],
        "raw_quality": json.loads(p.raw_quality) if p.raw_quality else {}
    }

@router.get("/")
def get_properties(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Return property listings for the current user."""
    query = db.query(Property)
    if current_user.role == 'seller':
        query = query.filter(Property.owner_id == current_user.id)
    
    properties = query.all()
    parsed = [parse_property(p) for p in properties]
    return {"properties": parsed, "total": len(parsed)}

from pydantic import BaseModel
from typing import List, Optional

class PropertyCreate(BaseModel):
    title: str
    location: str
    price: str
    bhk: str
    furnishing: str
    image: str
    quality_score: float
    room_type: str
    tags: List[str] = []

@router.post("/")
def create_property(prop_in: PropertyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new property listing."""
    import datetime
    pid = f"PRO-{int(datetime.datetime.now().timestamp())}"
    
    new_prop = Property(
        property_id=pid,
        owner_id=current_user.id,
        title=prop_in.title,
        location=prop_in.location,
        price=prop_in.price,
        bhk=prop_in.bhk,
        furnishing=prop_in.furnishing,
        image=prop_in.image,
        quality_score=prop_in.quality_score,
        room_type=prop_in.room_type,
        tags=json.dumps(prop_in.tags),
        detections=json.dumps(prop_in.tags), # Save detections for insight engine later
        ai_verified=True
    )
    db.add(new_prop)
    db.commit()
    db.refresh(new_prop)
    return parse_property(new_prop)

@router.get("/{property_id}")
def get_property(property_id: str, db: Session = Depends(get_db)):
    """Return a single property by property_id string (e.g., CHN-VEL-849)."""
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        # Try numeric ID if not found by property_id string
        try:
            prop = db.query(Property).filter(Property.id == int(property_id)).first()
        except ValueError:
            pass
            
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return parse_property(prop)

