"""
Pydantic models for data validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class VariantType(str, Enum):
    """Types of genomic variants."""
    SNV = "SNV"
    INSERTION = "Insertion"
    DELETION = "Deletion"
    INDEL = "Indel"
    CNV = "CNV"


class ACMGClassification(str, Enum):
    """ACMG pathogenicity classifications."""
    PATHOGENIC = "Pathogenic"
    LIKELY_PATHOGENIC = "Likely Pathogenic"
    UNCERTAIN = "Uncertain Significance"
    LIKELY_BENIGN = "Likely Benign"
    BENIGN = "Benign"


class Variant(BaseModel):
    """Represents a single genomic variant."""
    chrom: str = Field(..., description="Chromosome")
    pos: int = Field(..., description="Genomic position")
    ref: str = Field(..., description="Reference allele")
    alt: str = Field(..., description="Alternate allele")
    gene: Optional[str] = Field(None, description="Gene symbol")
    variant_type: VariantType = Field(..., description="Type of variant")
    
    cadd_score: Optional[float] = Field(None, ge=0, le=100)
    sift_score: Optional[float] = Field(None, ge=0, le=1)
    polyphen_score: Optional[float] = Field(None, ge=0, le=1)
    conservation_score: Optional[float] = Field(None, ge=0, le=1)
    allele_frequency: Optional[float] = Field(None, ge=0, le=1)
    
    pathogenicity_score: Optional[float] = Field(None, ge=0, le=1)
    acmg_classification: Optional[ACMGClassification] = None
    clinical_significance: Optional[str] = None


class VCFUploadResponse(BaseModel):
    """Response after uploading a VCF file."""
    job_id: str
    filename: str
    total_variants: int
    message: str
    timestamp: datetime


class AnalysisResult(BaseModel):
    """Complete analysis results for a VCF file."""
    job_id: str
    filename: str
    total_variants: int
    pathogenic_count: int
    likely_pathogenic_count: int
    uncertain_count: int
    likely_benign_count: int
    benign_count: int
    variants: List[Variant]
    processing_time_seconds: float
    generated_at: datetime


class ReportRequest(BaseModel):
    """Request to generate a PDF report."""
    job_id: str
    include_details: bool = True