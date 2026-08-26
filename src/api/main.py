"""
Main FastAPI REST Application for N100 Financial Intelligence Platform.
Mounts all 8 modular routers with /api/v1 prefix, CORS, and request execution time logging.
"""

import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import (
    health,
    companies,
    screener,
    sectors,
    peers,
    valuation,
    portfolio,
    documents,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI(
    title="N100 Financial Intelligence REST API",
    description="Full-featured REST API for NIFTY 100 Analytics, Screener, Peer Comparisons, and Reports",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/docs/openapi.json",
)

# CORS middleware for internal access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    logger.info(
        f"Method: {request.method} Path: {request.url.path} Status: {response.status_code} Duration: {duration_ms}ms"
    )
    response.headers["X-Process-Time-Ms"] = str(duration_ms)
    return response


# Include all routers with /api/v1 prefix
API_PREFIX = "/api/v1"
app.include_router(health.router, prefix=API_PREFIX)
app.include_router(companies.router, prefix=API_PREFIX)
app.include_router(screener.router, prefix=API_PREFIX)
app.include_router(sectors.router, prefix=API_PREFIX)
app.include_router(peers.router, prefix=API_PREFIX)
app.include_router(valuation.router, prefix=API_PREFIX)
app.include_router(portfolio.router, prefix=API_PREFIX)
app.include_router(documents.router, prefix=API_PREFIX)


@app.get("/")
def root():
    """Root redirect endpoint pointing to API documentation."""
    return {
        "message": "Welcome to N100 Financial Intelligence REST API",
        "docs": "/docs",
        "health": f"{API_PREFIX}/health",
    }
