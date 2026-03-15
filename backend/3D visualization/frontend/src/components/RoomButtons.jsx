import React from 'react';

const RoomButtons = ({ currentRoom, onRoomChange, availableRooms }) => {
  const formatRoomName = (roomType) => {
    return roomType.split('_').map(word =>
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  return (
    <div className="room-buttons">
      {availableRooms.map((room) => (
        <button
          key={room}
          className={`room-btn ${currentRoom === room ? 'active' : ''}`}
          onClick={() => onRoomChange(room)}
        >
          {formatRoomName(room)}
        </button>
      ))}
    </div>
  );
};

export default RoomButtons;