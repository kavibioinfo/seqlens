"""
FastAPI routes for SeqLens.
"""

import uuid
import time
from pathlib import Path
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from ..models.schemas import (
    VCFUploadResponse, AnalysisResult, Variant
)
from ..core.vcf_parser import VCFParser
from ..core.predictor import PathogenicityPredictor
from ..services.report_generator import ReportGenerator
from ..config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE

router = APIRouter(prefix="/api/v1", tags=["seqlens"])

# In-memory job storage
job_store = {}

# Initialize predictor
predictor = PathogenicityPredictor()


def _get_clinical_significance(acmg_class):
    """Map ACMG class to clinical description."""
    if acmg_class is None:
        return 'Unknown'
    mapping = {
        'Pathogenic': 'Known to cause disease',
        'Likely Pathogenic': 'Probably causes disease',
        'Uncertain Significance': 'Unknown clinical impact',
        'Likely Benign': 'Probably not disease-causing',
        'Benign': 'Not disease-causing'
    }
    return mapping.get(acmg_class.value, 'Unknown')


@router.post("/upload", response_model=VCFUploadResponse)
async def upload_vcf(file: UploadFile = File(...)):
    """Upload a VCF file for analysis."""
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS and not file.filename.endswith('.vcf.gz'):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}"
        )
    
    job_id = str(uuid.uuid4())[:8]
    file_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
    
    try:
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        with open(file_path, 'wb') as f:
            f.write(contents)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    
    parser = VCFParser(file_path)
    total_variants = parser.count_variants()
    
    job_store[job_id] = {
        'file_path': str(file_path),
        'filename': file.filename,
        'total_variants': total_variants,
        'status': 'uploaded',
        'results': None
    }
    
    return VCFUploadResponse(
        job_id=job_id,
        filename=file.filename,
        total_variants=total_variants,
        message="File uploaded successfully. Use /analyze/{job_id} to start analysis.",
        timestamp=__import__('datetime').datetime.now()
    )


@router.post("/analyze/{job_id}", response_model=AnalysisResult)
async def analyze_vcf(job_id: str, background_tasks: BackgroundTasks = None):
    """Analyze uploaded VCF file and predict pathogenicity."""
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = job_store[job_id]
    
    if job['status'] == 'analyzing':
        raise HTTPException(status_code=400, detail="Analysis already in progress")
    
    if job['status'] == 'completed':
        return job['results']
    
    job['status'] = 'analyzing'
    start_time = time.time()
    
    try:
        parser = VCFParser(Path(job['file_path']))
        variants = list(parser.parse_variants())
        
        analyzed_variants = []
        counts = {
            'Pathogenic': 0,
            'Likely Pathogenic': 0,
            'Uncertain Significance': 0,
            'Likely Benign': 0,
            'Benign': 0
        }
        
        for variant in variants:
            prediction = predictor.predict(variant)
            
            variant.pathogenicity_score = prediction['pathogenicity_score']
            variant.acmg_classification = prediction['acmg_classification']
            variant.clinical_significance = _get_clinical_significance(
                prediction['acmg_classification']
            )
            
            counts[prediction['acmg_classification'].value] += 1
            analyzed_variants.append(variant)
        
        processing_time = time.time() - start_time
        
        result = AnalysisResult(
            job_id=job_id,
            filename=job['filename'],
            total_variants=len(analyzed_variants),
            pathogenic_count=counts['Pathogenic'],
            likely_pathogenic_count=counts['Likely Pathogenic'],
            uncertain_count=counts['Uncertain Significance'],
            likely_benign_count=counts['Likely Benign'],
            benign_count=counts['Benign'],
            variants=analyzed_variants,
            processing_time_seconds=round(processing_time, 2),
            generated_at=__import__('datetime').datetime.now()
        )
        
        job['status'] = 'completed'
        job['results'] = result
        
        return result
        
    except Exception as e:
        job['status'] = 'failed'
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/results/{job_id}", response_model=AnalysisResult)
async def get_results(job_id: str):
    """Get analysis results for a completed job."""
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = job_store[job_id]
    
    if job['status'] != 'completed':
        raise HTTPException(
            status_code=400,
            detail=f"Job status: {job['status']}. Please wait or check /status/{job_id}"
        )
    
    return job['results']


@router.get("/status/{job_id}")
async def get_status(job_id: str):
    """Check analysis status."""
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = job_store[job_id]
    return {
        'job_id': job_id,
        'status': job['status'],
        'filename': job['filename'],
        'total_variants': job['total_variants']
    }


@router.get("/report/{job_id}")
async def generate_report(job_id: str):
    """Generate PDF report for analyzed variants."""
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = job_store[job_id]
    
    if job['status'] != 'completed':
        raise HTTPException(status_code=400, detail="Analysis not completed yet")
    
    try:
        generator = ReportGenerator()
        report_path = generator.generate(job['results'])
        
        return FileResponse(
            report_path,
            media_type='application/pdf',
            filename=f"seqlens_report_{job_id}.pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "SeqLens",
        "version": "1.0.0",
        "model_loaded": predictor.is_trained
    }