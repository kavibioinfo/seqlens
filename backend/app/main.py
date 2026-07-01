"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .config import APP_NAME, APP_VERSION

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="""
    SeqLens - Genomic Variant Annotation & Pathogenicity Prediction API
    
    ## Features
    - Upload VCF files
    - Automatic variant annotation
    - ML-based pathogenicity prediction
    - ACMG classification
    - PDF report generation
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS - Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://seqlens.ayushnexa.com",
        "https://seqlens.onrender.com",
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to SeqLens API",
        "version": APP_VERSION,
        "docs": "/docs"
    }