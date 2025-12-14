"""
Main FastAPI application entry point.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import initialize_database
from app.routes.authentication_routes import router as auth_router
from app.routes.sweets_routes import router as sweets_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler - runs on startup and shutdown."""
    # Startup
    initialize_database()
    yield
    # Shutdown (cleanup if needed)


app = FastAPI(
    title="Sweet Shop Management System",
    description="API for managing a sweet shop inventory and orders",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(sweets_router)


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {"message": "Sweet Shop API is live"}