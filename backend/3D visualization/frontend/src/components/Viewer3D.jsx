import React, { Suspense, useRef, useEffect, useState } from "react";
import { Canvas, useLoader } from "@react-three/fiber";
import { OrbitControls, Html } from "@react-three/drei";
import * as THREE from "three";
import Hotspot from "./Hotspot";

/**
 * IMPORTANT: This virtual tour requires 360-degree panoramic images.
 * Regular photos will appear distorted when wrapped around the sphere.
 * Recommended: Equirectangular projection images (2:1 aspect ratio)
 * Supported formats: JPG, PNG, etc.
 */

// 1. The 360-Degree Environment Component
function ImageSphere({ imageUrl }) {
  const [imageError, setImageError] = React.useState(false);

  const texture = useLoader(THREE.TextureLoader, imageUrl, (loader) => {
    // Handle loading progress
  }, (error) => {
    console.error('Error loading texture:', error);
    setImageError(true);
  });

  // Optimize texture for better performance
  useEffect(() => {
    if (texture && !imageError) {
      texture.generateMipmaps = false;
      texture.minFilter = THREE.LinearFilter;
      texture.magFilter = THREE.LinearFilter;
      texture.needsUpdate = true;
    }
  }, [texture, imageError]);

  if (imageError) {
    return (
      <mesh>
        <sphereGeometry args={[10, 16, 8]} />
        <meshBasicMaterial color="#333333" side={THREE.BackSide} />
      </mesh>
    );
  }

  return (
    <mesh>
      {/* Optimized sphere geometry - smaller radius, fewer segments for better performance */}
      <sphereGeometry args={[10, 32, 16]} />
      {/* Paint the image on the INSIDE of the walls */}
      <meshBasicMaterial map={texture} side={THREE.BackSide} />
    </mesh>
  );
}

// 2. Hotspot layout for each room
const hotspotPositions = {
  living_room: {
    bedroom: { x: 75, y: 40 },
    kitchen: { x: 25, y: 60 }
  },
  bedroom: {
    living_room: { x: 50, y: 50 }
  },
  kitchen: {
    living_room: { x: 75, y: 40 },
    bathroom: { x: 25, y: 60 }
  },
  bathroom: {
    kitchen: { x: 50, y: 50 }
  }
};

// 3. The Main Viewer Component
function Viewer3D({ imageUrl, currentRoom, hotspots = [], onHotspotClick }) {
  const controlsRef = useRef();

  const formatRoomName = (roomType) => {
    return roomType
      .split("_")
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  const handleZoomIn = () => {
    if (controlsRef.current && controlsRef.current.object) {
      const camera = controlsRef.current.object;
      camera.fov = Math.max(30, camera.fov - 10); // Zoom in by reducing FOV
      camera.updateProjectionMatrix();
    }
  };

  const handleZoomOut = () => {
    if (controlsRef.current && controlsRef.current.object) {
      const camera = controlsRef.current.object;
      camera.fov = Math.min(120, camera.fov + 10); // Zoom out by increasing FOV
      camera.updateProjectionMatrix();
    }
  };

  return (
    <div style={{ position: "relative", width: "100%", height: "100vh" }}>
      
      <Canvas
        // Optimized camera position - further from center for better viewing
        camera={{ position: [0, 0, 0.01], fov: 75, near: 0.001, far: 100 }}
        style={{ background: "#000" }}
        gl={{
          antialias: false,
          alpha: false,
          powerPreference: "high-performance",
          stencil: false,
          depth: true
        }} // Performance optimizations
        dpr={[1, 2]} // Adaptive pixel ratio for performance
      >
        <Suspense
          fallback={
            <Html center>
              <p style={{ color: "white", fontSize: "1.2rem", fontFamily: "sans-serif" }}>
                Loading room...
              </p>
            </Html>
          }
        >
          <ImageSphere imageUrl={imageUrl} />
        </Suspense>

        <OrbitControls
          ref={controlsRef}
          enableZoom={true}
          enablePan={false}
          enableDamping
          dampingFactor={0.05}
          rotateSpeed={-0.5} // Negative speed feels better when inside a sphere
          minDistance={0.001}
          maxDistance={5}
          minPolarAngle={0}
          maxPolarAngle={Math.PI}
        />
      </Canvas>

      {/* 4. The Clickable UI Hotspots */}
      {hotspots.map((targetRoom) => {
        const position = hotspotPositions[currentRoom]?.[targetRoom];
        if (!position) return null;

        return (
          <div
            key={targetRoom}
            style={{
              position: "absolute",
              top: `${position.y}%`,
              left: `${position.x}%`,
              transform: "translate(-50%, -50%)",
              zIndex: 10 // Ensures buttons sit on top of the 3D canvas
            }}
          >
            <Hotspot
              label={formatRoomName(targetRoom)}
              onClick={() => onHotspotClick(targetRoom)}
            />
          </div>
        );
      })}

      {/* Zoom Controls */}
      <div style={{
        position: "absolute",
        top: "20px",
        right: "20px",
        zIndex: 20,
        display: "flex",
        flexDirection: "column",
        gap: "10px"
      }}>
        <button
          onClick={handleZoomIn}
          style={{
            width: "40px",
            height: "40px",
            borderRadius: "50%",
            background: "rgba(255,255,255,0.9)",
            border: "2px solid rgba(0,0,0,0.3)",
            cursor: "pointer",
            fontSize: "18px",
            fontWeight: "bold",
            color: "#333",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            transition: "all 0.2s ease"
          }}
          onMouseOver={(e) => e.target.style.background = "rgba(255,255,255,1)"}
          onMouseOut={(e) => e.target.style.background = "rgba(255,255,255,0.9)"}
          title="Zoom In"
        >
          +
        </button>
        <button
          onClick={handleZoomOut}
          style={{
            width: "40px",
            height: "40px",
            borderRadius: "50%",
            background: "rgba(255,255,255,0.9)",
            border: "2px solid rgba(0,0,0,0.3)",
            cursor: "pointer",
            fontSize: "18px",
            fontWeight: "bold",
            color: "#333",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            transition: "all 0.2s ease"
          }}
          onMouseOver={(e) => e.target.style.background = "rgba(255,255,255,1)"}
          onMouseOut={(e) => e.target.style.background = "rgba(255,255,255,0.9)"}
          title="Zoom Out"
        >
          −
        </button>
      </div>
    </div>
  );
}

export default Viewer3D;