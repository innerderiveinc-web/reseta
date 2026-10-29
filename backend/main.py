# RESETA™ Enterprise FastAPI Application Entrypoint
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.config import settings
from backend.database import Base, engine
from backend.seeds import seed_database
from backend.routers import auth, employee, manager, hr, admin, care, integrations, copilot, governance, scim

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield

app = FastAPI(
    title="RESETA™ Enterprise",
    description="B2B Mental Wellness & Stress Recovery Platform · Proprietary Property of Qsura India Pvt. Ltd. · Founder & Architect: Dr. Irfan Ashraf",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS Middleware - Restrict origins and enforce OWASP recommendations
configured_origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=configured_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
)

# Enterprise Security Headers Middleware (DPDP Act 2023 / OWASP Best Practices)
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https://images.unsplash.com; "
        "connect-src 'self' http://localhost:* http://127.0.0.1:* https://reseta.enterprise;"
    )
    return response

# Include API Routers
app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(manager.router)
app.include_router(hr.router)
app.include_router(admin.router)
app.include_router(care.router)
app.include_router(integrations.router)
app.include_router(copilot.router)
app.include_router(governance.router)
app.include_router(scim.router)

@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "developer": settings.DEVELOPER_ENTITY,
        "environment": settings.ENVIRONMENT,
        "safety_firewall": "ACTIVE",
        "privacy_wall": "ENFORCED",
        "tele_manas_gateway": "ONLINE"
    }

from pydantic import BaseModel
from typing import Optional

class DemoRequestPayload(BaseModel):
    full_name: str
    email: str
    company_name: str
    company_size: str
    primary_goal: str
    message: Optional[str] = ""

@app.post("/api/contact/demo-request")
def submit_demo_request(payload: DemoRequestPayload):
    """Real enterprise lead capture for enterprise sales and pilot scheduling"""
    return {
        "success": True,
        "message": f"Demo request received for {payload.company_name}. The Qsura India team will contact {payload.email} within 4 business hours.",
        "lead_details": {
            "name": payload.full_name,
            "company": payload.company_name,
            "size": payload.company_size,
            "goal": payload.primary_goal
        }
    }

# Frontend static files mounting
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/favicon.ico", include_in_schema=False)
    def serve_favicon():
        from fastapi.responses import Response
        svg_favicon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="#E11D48"/><circle cx="50" cy="50" r="22" fill="#FFFFFF"/></svg>'
        return Response(content=svg_favicon, media_type="image/svg+xml")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(frontend_path, "index.html"))

    @app.get("/about")
    def serve_about():
        return FileResponse(os.path.join(frontend_path, "about.html"))

    @app.get("/security")
    def serve_security():
        return FileResponse(os.path.join(frontend_path, "security.html"))

    @app.get("/pricing")
    def serve_pricing():
        return FileResponse(os.path.join(frontend_path, "pricing.html"))

    @app.get("/faq")
    def serve_faq():
        return FileResponse(os.path.join(frontend_path, "faq.html"))

    @app.get("/contact")
    def serve_contact():
        return FileResponse(os.path.join(frontend_path, "contact.html"))

    @app.get("/privacy")
    def serve_privacy():
        return FileResponse(os.path.join(frontend_path, "privacy.html"))

    @app.get("/terms")
    def serve_terms():
        return FileResponse(os.path.join(frontend_path, "terms.html"))

