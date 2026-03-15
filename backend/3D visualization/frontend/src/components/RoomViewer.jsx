import React, { useRef, useState } from 'react';
import { Canvas, useLoader } from '@react-three/fiber';
import { OrbitControls, Sphere } from '@react-three/drei';
import * as THREE from 'three';

const RoomViewer = ({ roomImage }) => {
  const [isInteracting, setIsInteracting] = useState(false);
  const controlsRef = useRef();

  // Load the texture
  const texture = useLoader(THREE.TextureLoader, roomImage);

  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <Canvas camera={{ position: [0, 0, 0.1], fov: 75 }}>
        {/* Giant sphere with inside texture */}
        <Sphere args={[500, 60, 40]}>
          <meshBasicMaterial map={texture} side={THREE.BackSide} />
        </Sphere>

        {/* Orbit controls with auto-rotation */}
        <OrbitControls
          ref={controlsRef}
          enableZoom={false}
          enablePan={false}
          autoRotate={!isInteracting}
          autoRotateSpeed={0.5}
          dampingFactor={0.05}
          enableDamping
          onStart={() => setIsInteracting(true)}
          onEnd={() => setIsInteracting(false)}
        />
      </Canvas>
    </div>
  );
};

export default RoomViewer;