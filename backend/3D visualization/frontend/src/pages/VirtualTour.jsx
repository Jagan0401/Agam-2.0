import React, { useState, useEffect } from 'react';
import Viewer3D from '../components/Viewer3D';
import RoomButtons from '../components/RoomButtons';
import Navbar from '../components/Navbar';
import { apiService } from '../services/api';

const VirtualTour = () => {
  const [tourData, setTourData] = useState(null);
  const [currentRoom, setCurrentRoom] = useState('living_room');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Room navigation configuration
  const roomConnections = {
    living_room: ['bedroom', 'kitchen'],
    bedroom: ['living_room'],
    kitchen: ['living_room', 'bathroom'],
    bathroom: ['kitchen'],
  };

  useEffect(() => {
    fetchTourData();
  }, []);

  const fetchTourData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.getVirtualTour();
      setTourData(data);
    } catch (err) {
      setError('Failed to load virtual tour data. Please try again.');
      console.error('Error fetching tour data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRoomChange = (roomType) => {
    setCurrentRoom(roomType);
  };

  const handleHotspotClick = (targetRoom) => {
    setCurrentRoom(targetRoom);
  };

  if (loading) {
    return (
      <div className="loading">
        Loading Virtual Tour...
      </div>
    );
  }

  if (error) {
    return (
      <div className="error">
        <h2>Oops! Something went wrong</h2>
        <p>{error}</p>
        <button className="retry-btn" onClick={fetchTourData}>
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="app">
      <Navbar />
      <div className="main-content">
        <RoomButtons
          currentRoom={currentRoom}
          onRoomChange={handleRoomChange}
          availableRooms={Object.keys(tourData)}
        />
        <Viewer3D
          imageUrl={tourData[currentRoom]}
          currentRoom={currentRoom}
          hotspots={roomConnections[currentRoom] || []}
          onHotspotClick={handleHotspotClick}
        />
      </div>
    </div>
  );
};

export default VirtualTour;