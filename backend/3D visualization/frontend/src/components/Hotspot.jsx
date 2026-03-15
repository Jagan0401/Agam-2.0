import React from 'react';

const Hotspot = ({ onClick, label }) => {
  return (
    <div
      className="hotspot"
      onClick={onClick}
      title={`Go to ${label}`}
    >
      →
    </div>
  );
};

export default Hotspot;