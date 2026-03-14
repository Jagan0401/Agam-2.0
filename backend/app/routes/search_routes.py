from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.property import Property

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
def search(
    q: str = Query(None),
    type: str = Query(None),
    semantic: bool = Query(False),
    db: Session = Depends(get_db)
):
    """
    Search properties by keyword, type, or AI-semantic context.
    """
    if semantic and q:
        from app.services.search_service import search_properties_semantic
        # Semantic search gives us IDs or similarity results
        # In this simple implementation, we'll use keyword search as a base 
        # but you could rank by semantic similarity here.
        semantic_results = search_properties_semantic(q)
        # Note: In a production app, you'd fetch properties based on FAISS IDs
        # Here we prioritize semantic keyword filtering
        query = db.query(Property).filter(
            Property.title.contains(q) | 
            Property.location.contains(q) |
            Property.tags.contains(q)
        )
    else:
        query = db.query(Property)
        if q:
            query = query.filter(Property.title.contains(q) | Property.location.contains(q))
        if type:
            query = query.filter(Property.bhk.contains(type))
        
    results = query.all()
    
    # Manually parse JSON strings since we switched to String columns for SQLite compatibility
    import json
    parsed_results = []
    for p in results:
        # Convert SQLAlchemy object to dict to modify it or just parse fields
        p_dict = {
            "id": p.id,
            "property_id": p.property_id,
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
        parsed_results.append(p_dict)
    
    return {
        "query": q,
        "semantic": semantic,
        "results": parsed_results,
        "total": len(parsed_results)
    }