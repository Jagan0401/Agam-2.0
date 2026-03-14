from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from app.database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), index=True)
    property_id = Column(String, unique=True, index=True) # e.g. CHN-VEL-849
    title = Column(String)
    location = Column(String)
    price = Column(String)
    bhk = Column(String)
    sqft = Column(String)
    furnishing = Column(String)
    tags = Column(String, default="[]") # Store tags as a JSON string
    image = Column(String)
    quality_score = Column(Float)
    room_type = Column(String)
    detections = Column(String, default="[]") # Objects detected by YOLO
    raw_quality = Column(String, default="{}") # Detailed quality metrics
    ai_verified = Column(Boolean, default=True)
    moderation_status = Column(String, default="approved") # approved, pending, flagged, rejected
    moderation_reason = Column(String, default="")

