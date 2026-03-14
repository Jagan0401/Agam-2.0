from fastapi import APIRouter, UploadFile, File, Request, Depends
from app.dependencies import get_current_user
from app.models.user import User
import shutil
import os

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/")
async def upload_image(request: Request, file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    """
    Upload a property image.
    Saves the file to /uploads/, runs AI analysis (room classification,
    quality scoring, CLIP tag generation) and returns the results along
    with the public URL of the saved image.
    """
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Build the public URL for the saved image
    base_url = str(request.base_url).rstrip("/")
    image_url = f"{base_url}/uploads/{file.filename}"

    # Run AI analysis
    try:
        from app.services.search_service import analyze_image
        analysis = analyze_image(file_path)
    except Exception as e:
        # Provide detailed error in response if models fail
        analysis = {
            "error": f"AI Engine Exception: {str(e)}",
            "room_type": "unknown",
            "tags": [],
            "quality_score": 0.0
        }

    return {
        "filename": file.filename,
        "image_url": image_url,
        "analysis": analysis,
        "role_verified": current_user.role
    }