# AI Real Estate Virtual Tour

## Image Requirements for Virtual Tour

### ✅ What Works Best
- **360-degree panoramic images** in equirectangular projection
- **Aspect ratio**: 2:1 (width:height) - e.g., 4096x2048, 2048x1024
- **Formats**: JPG, PNG, WebP (optimized for web)
- **File size**: Under 5MB per image for good performance
- **Resolution**: 2048x1024 minimum, 4096x2048 recommended

### ❌ What Won't Work Well
- Regular photos (not 360°)
- Vertical images
- Square images
- Images with extreme aspect ratios

### 📸 How to Create 360° Images
1. **Use a 360° camera** (Ricoh Theta, Insta360, etc.)
2. **Stitch multiple photos** using software like:
   - PTGui
   - Hugin
   - Adobe Photoshop
   - Online stitchers (Google Street View, etc.)
3. **Use smartphone apps** with 360° capture

### 🔧 Technical Optimizations Applied
- **Sphere geometry**: Optimized from radius 500 to 10 for better performance
- **Texture optimization**: Disabled mipmaps, linear filtering
- **Camera settings**: Optimized near/far planes and position
- **WebGL settings**: Disabled antialiasing, optimized for performance
- **Error handling**: Fallback for failed image loads
- **Zoom limits**: Constrained for better UX

### 🚀 Performance Tips
- Compress images before uploading
- Use WebP format when possible
- Keep file sizes under 2MB for mobile devices
- Test on target devices before deployment

### 📁 File Structure
```
backend/images/
├── living_room.jpg    # 360° panoramic image
├── bedroom.jpg       # 360° panoramic image
├── kitchen.jpg       # 360° panoramic image
└── bathroom.jpg      # 360° panoramic image
```