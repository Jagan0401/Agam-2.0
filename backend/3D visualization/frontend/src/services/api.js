// API service for communicating with the backend

const API_BASE_URL = 'http://localhost:8000/api';

export const apiService = {
  // Fetch virtual tour data
  async getVirtualTour() {
    try {
      const response = await fetch(`${API_BASE_URL}/virtual-tour`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching virtual tour data:', error);
      throw error;
    }
  },

  // Upload property images (for future ML integration)
  async uploadPropertyImages(files) {
    try {
      const formData = new FormData();
      files.forEach((file, index) => {
        formData.append(`files`, file);
      });

      const response = await fetch(`${API_BASE_URL}/upload-property-images`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error uploading property images:', error);
      throw error;
    }
  },
};