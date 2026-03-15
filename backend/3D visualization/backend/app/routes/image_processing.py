import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path

router = APIRouter()

# Define the images directory
IMAGES_DIR = Path(__file__).parent.parent.parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    Endpoint to upload an image from the frontend and save it to the backend/images/ folder.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # Validate file type (basic check for image files)
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Only image files are allowed.")

    # Generate a unique filename to avoid conflicts
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = IMAGES_DIR / unique_filename

    try:
        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Return the saved file path (relative to backend)
    return JSONResponse(
        content={
            "message": "Image uploaded successfully",
            "filename": unique_filename,
            "path": f"images/{unique_filename}"
        },
        status_code=200
    )