from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.property_routes import router as property_router
from app.config import CORS_ORIGINS

app = FastAPI(title="AI Real Estate Virtual Tour Backend", version="1.0.0")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(property_router, prefix="/api", tags=["property"])

@app.get("/")
async def root():
    return {"message": "AI Real Estate Virtual Tour Backend API"}