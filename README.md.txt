# 🧬 SeqLens - Genomic Variant Annotator

AI-powered genomic variant annotation and pathogenicity prediction platform.

## Features

- 📤 VCF file upload and parsing
- 🤖 ML-based pathogenicity prediction
- 📊 ACMG classification
- 📄 PDF report generation
- ⚡ FastAPI backend with React frontend

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload