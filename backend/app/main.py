from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routes import upload_routes, search_routes, property_routes, auth_routes, chat_routes, admin_routes
from app.database import engine, Base
from app.models import user, property # ensure models are imported before creating tables
from app.db_sync import sync_database_schema

# Run schema sync to add missing columns to agam.db
sync_database_schema()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agam AI Property System")

# Allow all frontend origins (file://, localhost, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded images at /uploads/<filename>
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

app.include_router(auth_routes.router)
app.include_router(upload_routes.router)
app.include_router(search_routes.router)
app.include_router(property_routes.router)
app.include_router(chat_routes.router)
app.include_router(admin_routes.router)



from fastapi.responses import FileResponse

# Serve the index.html on the root path
@app.get("/")
def serve_frontend_index():
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Mount the entire frontend folder as static files (for css, js, other html pages)
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")