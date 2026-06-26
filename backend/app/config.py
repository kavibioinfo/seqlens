"""
Configuration settings for SeqLens.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
MODEL_DIR = BASE_DIR / "data" / "models"
REFERENCE_DIR = BASE_DIR / "data" / "reference"

# Create directories if they don't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
REFERENCE_DIR.mkdir(parents=True, exist_ok=True)

# Application settings
APP_NAME = "SeqLens - Genomic Variant Annotator"
APP_VERSION = "1.0.0"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB max upload

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.vcf', '.vcf.gz'}

# ML Model settings
MODEL_PATH = MODEL_DIR / "pathogenicity_model.pkl"
FEATURE_COLUMNS = [
    'cadd_score', 'sift_score', 'polyphen_score',
    'conservation_score', 'allele_frequency', 'variant_type'
]

# ACMG Classification thresholds
ACMG_THRESHOLDS = {
    'pathogenic': 0.9,
    'likely_pathogenic': 0.7,
    'uncertain': 0.3,
    'likely_benign': 0.1,
    'benign': 0.0
}