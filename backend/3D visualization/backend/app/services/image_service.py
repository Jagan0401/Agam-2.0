"""
Image Service - Handles image processing and room classification
"""

from app.models.room_classifier import RoomClassifier
from app.utils.file_handler import get_room_images

class ImageService:
    def __init__(self):
        self.classifier = RoomClassifier()

    def get_virtual_tour_data(self) -> dict:
        """
        Get data for the virtual tour - currently returns sample images.
        Later this will use the ML classifier.

        Returns:
            dict: Room type to image path mapping
        """
        # For now, return sample images
        # TODO: Replace with actual ML classification pipeline
        return get_room_images()

    def process_uploaded_images(self, uploaded_files) -> dict:
        """
        Process uploaded property images and classify rooms.
        Currently placeholder - will be implemented with ML.

        Args:
            uploaded_files: List of uploaded files

        Returns:
            dict: Classified room images
        """
        # TODO: Save files, classify with ML, return organized data
        return self.get_virtual_tour_data()