"""
CDR Analyzer - Main FastAPI Application
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn

from database import init_db, get_db
from models import CallRecord, UploadResponse, CallListResponse, StatsResponse
from processor import process_cdr_file

app = FastAPI(
    title="CDR Analyzer API",
    description="Call Detail Record Analysis System",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "CDR Analyzer API", "status": "running"}

# API Endpoints will be added here
from routes import upload, calls, stats

app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(calls.router, prefix="/api/v1", tags=["calls"])
app.include_router(stats.router, prefix="/api/v1", tags=["stats"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
