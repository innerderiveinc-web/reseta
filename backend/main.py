# RESETA™ Enterprise FastAPI Application Entrypoint
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.config import settings
from backend.database import Base, engine
from backend.seeds import seed_database
from backend.routers import auth, employee, manager, hr, admin, care, integrations, copilot

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield

app = FastAPI(
    title="RESETA™ Enterprise",
    description="B2B Mental Wellness & Stress Recovery Platform API",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(manager.router)
app.include_router(hr.router)
app.include_router(admin.router)
app.include_router(care.router)
app.include_router(integrations.router)
app.include_router(copilot.router)




@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "safety_firewall": "ACTIVE",
        "privacy_wall": "ENFORCED",
        "tele_manas_gateway": "ONLINE"
    }

# Frontend static files mounting
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(frontend_path, "index.html"))
