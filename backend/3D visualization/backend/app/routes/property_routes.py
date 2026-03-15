from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from app.services.image_service import ImageService

router = APIRouter()
image_service = ImageService()

@router.get("/virtual-tour")
async def get_virtual_tour():
    """
    Get virtual tour data with room images.
    Currently returns sample images - will be enhanced with ML classification.
    """
    try:
        tour_data = image_service.get_virtual_tour_data()
        return JSONResponse(content=tour_data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching virtual tour data: {str(e)}")

@router.post("/upload-property-images")
async def upload_property_images(files: List[UploadFile] = File(...)):
    """
    Upload property images for classification.
    Currently placeholder - will process images with ML model.
    """
    try:
        # TODO: Process uploaded images with ML classification
        result = image_service.process_uploaded_images(files)
        return JSONResponse(
            content={
                "message": "Images uploaded successfully",
                "classified_rooms": result
            },
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing images: {str(e)}")