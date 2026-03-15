// RoomViewer - 360° Room Viewer using Three.js
class RoomViewer {
    constructor(containerId, roomImageUrl) {
        this.container = document.getElementById(containerId);
        this.roomImageUrl = roomImageUrl;
        this.isInteracting = false;
        this.autoRotateSpeed = 0.005; // Slow rotation

        this.init();
    }

    init() {
        // Scene setup
        this.scene = new THREE.Scene();

        // Camera setup
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.camera.position.set(0, 0, 0.1);

        // Renderer setup
        this.renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('viewer-canvas'), antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);

        // Load texture
        const textureLoader = new THREE.TextureLoader();
        textureLoader.load(
            this.roomImageUrl,
            (texture) => {
                this.createSphere(texture);
                this.setupControls();
                this.animate();
            },
            undefined,
            (error) => {
                console.error('Error loading texture:', error);
            }
        );

        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
    }

    createSphere(texture) {
        // Create giant sphere geometry
        const geometry = new THREE.SphereGeometry(500, 60, 40);

        // Create material with inside texture
        const material = new THREE.MeshBasicMaterial({
            map: texture,
            side: THREE.BackSide // Render inside of sphere
        });

        // Create mesh
        this.sphere = new THREE.Mesh(geometry, material);
        this.scene.add(this.sphere);
    }

    setupControls() {
        // OrbitControls for mouse interaction
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableZoom = false;
        this.controls.enablePan = false;
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;

        // Auto-rotation setup
        this.controls.autoRotate = true;
        this.controls.autoRotateSpeed = this.autoRotateSpeed * 60; // Convert to degrees per frame

        // Pause auto-rotation on interaction
        this.controls.addEventListener('start', () => {
            this.isInteracting = true;
            this.controls.autoRotate = false;
        });

        this.controls.addEventListener('end', () => {
            this.isInteracting = false;
            // Resume auto-rotation after a short delay
            setTimeout(() => {
                if (!this.isInteracting) {
                    this.controls.autoRotate = true;
                }
            }, 1000);
        });
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        // Update controls
        this.controls.update();

        // Render scene
        this.renderer.render(this.scene, this.camera);
    }

    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

// Initialize the viewer when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // You can pass the room image URL here - for now using a placeholder
    const roomImageUrl = 'https://example.com/360-room-image.jpg'; // Replace with actual image URL
    const viewer = new RoomViewer('viewer-container', roomImageUrl);
});