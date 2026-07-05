<div align="center">
🧬 SeqLens — Genomic Variant Annotator
AI-Powered Pathogenicity Prediction & ACMG Classification Platform
🔗 Live Demo  |  🐙 GitHub
</div>
🎯 What is SeqLens?
SeqLens is a full-stack genomic variant annotation platform that enables researchers, clinicians, and bioinformatics professionals to upload VCF (Variant Call Format) files and instantly receive:
🤖 AI-Powered Pathogenicity Predictions using ensemble Machine Learning (Random Forest + Gradient Boosting)
📊 ACMG-Compliant Classifications (Pathogenic → Benign)
📈 Interactive Visual Dashboard with real-time statistics
📄 Professional PDF Reports for clinical documentation
✨ Key Features
Table
Feature	Description	Technology
📤 VCF Upload	Drag-and-drop upload for .vcf and .vcf.gz files	React + FastAPI
🤖 ML Prediction	Ensemble model (RF + GB) predicts pathogenicity scores	scikit-learn
📊 ACMG Classification	Standard 5-tier clinical classification system	Custom Logic
📈 Data Visualization	Interactive bar charts and stat cards	CSS + React
📄 PDF Reports	Auto-generated professional clinical reports	ReportLab
⚡ Fast Processing	Sub-second analysis for typical VCF files	FastAPI + Async
📱 Responsive Design	Works on desktop, tablet, and mobile	Tailwind CSS
🔒 HTTPS Secured	SSL-enabled custom domain deployment	Vercel + Let's Encrypt
🏗️ Architecture
plain
┌─────────────────────────────────────────────────────────────┐
│                    REACT FRONTEND                            │
│  (Vercel CDN | Tailwind CSS | Lucide Icons)                │
│  • Upload Interface  • Results Dashboard  • PDF Download    │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS / REST API
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              FASTAPI BACKEND (Python)                        │
│  • VCF Parser (BioPython)                                  │
│  • ML Predictor (scikit-learn: RF + GradientBoosting)      │
│  • ACMG Classifier                                         │
│  • PDF Generator (ReportLab)                               │
└─────────────────────────────────────────────────────────────┘
🛠️ Tech Stack
Backend
Table
Technology	Purpose
FastAPI	High-performance Python web framework
Pydantic	Data validation and serialization
scikit-learn	Machine Learning (Random Forest + Gradient Boosting)
BioPython	Biological sequence and VCF parsing
ReportLab	PDF report generation
pandas / numpy	Data processing and numerical computation
Frontend
Table
Technology	Purpose
React 18	Component-based UI library
Tailwind CSS	Utility-first CSS framework
Lucide React	Modern icon library
Create React App	Build tooling and development server
DevOps & Deployment
Table
Technology	Purpose
Git + GitHub	Version control and source code hosting
Vercel	Frontend deployment with global CDN
Custom Domain	seqlens.ayushnexa.com
🚀 Quick Start
Prerequisites
Python 3.12+
Node.js 18+
Git
1. Clone the Repository
bash
git clone https://github.com/kavibioinfo/seqlens.git
cd seqlens
2. Start the Backend
bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
The API will be available at http://localhost:8000
Interactive API docs at http://localhost:8000/docs
3. Start the Frontend
bash
cd frontend
npm install
npm start
The application will open at http://localhost:3000
📖 API Endpoints
Table
Method	Endpoint	Description
POST	/api/v1/upload	Upload VCF file
POST	/api/v1/analyze/{job_id}	Analyze uploaded variants
GET	/api/v1/results/{job_id}	Get analysis results
GET	/api/v1/status/{job_id}	Check job status
GET	/api/v1/report/{job_id}	Download PDF report
GET	/api/v1/health	Health check
🧬 Machine Learning Model
Feature Engineering
The ensemble model uses 6 bioinformatics features:
Table
Feature	Source	Weight
CADD Score	Combined Annotation Dependent Depletion	High
SIFT Score (inverted)	Sorting Intolerant From Tolerant	Medium
PolyPhen Score	Polymorphism Phenotyping	High
Conservation Score	PhyloP / GERP	Medium
Allele Frequency (inverted)	gnomAD / ExAC	High
Variant Type	Structural classification	Low
Ensemble Strategy
plain
Final Score = 0.4 × RandomForest + 0.6 × GradientBoosting
ACMG Classification Mapping
Table
Score Range	Classification
≥ 0.90	🔴 Pathogenic
0.70 – 0.89	🟠 Likely Pathogenic
0.30 – 0.69	🟡 Uncertain Significance
0.10 – 0.29	🟢 Likely Benign
< 0.10	🟢 Benign
📁 Project Structure
plain
seqlens/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py              # REST API endpoints
│   │   ├── core/
│   │   │   ├── vcf_parser.py         # VCF file parser
│   │   │   └── predictor.py          # ML pathogenicity predictor
│   │   ├── models/
│   │   │   └── schemas.py            # Pydantic data models
│   │   ├── services/
│   │   │   └── report_generator.py   # PDF report generator
│   │   ├── utils/
│   │   │   └── helpers.py            # Utility functions
│   │   ├── config.py                 # Configuration settings
│   │   └── main.py                   # FastAPI entry point
│   ├── data/
│   │   ├── uploads/                  # Uploaded VCF files
│   │   ├── models/                   # Trained ML models
│   │   └── reference/                # Reference data
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadForm.jsx        # File upload component
│   │   │   └── ResultsDashboard.jsx  # Results display
│   │   ├── services/
│   │   │   └── api.js                # API communication layer
│   │   ├── App.js                    # Main application
│   │   └── index.css                 # Tailwind CSS imports
│   ├── public/
│   ├── package.json
│   └── tailwind.config.js
│
├── screenshots/                      # Add your screenshots here
├── docs/
├── README.md
├── .gitignore
└── LICENSE
🧪 Sample Data
A sample VCF file is included for testing:
plain
backend/data/reference/sample_test.vcf
This file contains 7 variants across BRCA1, BRCA2, and CFTR genes with pre-calculated CADD, SIFT, and PolyPhen scores.
🗺️ Roadmap
Phase 1 — Completed ✅
[x] VCF upload and parsing
[x] ML pathogenicity prediction
[x] ACMG classification
[x] Interactive dashboard
[x] PDF report generation
[x] Deployment to custom domain
Phase 2 — In Progress 🔄
[ ] ClinVar database integration
[ ] gnomAD allele frequency lookup
[ ] User authentication & saved history
[ ] Batch file processing
Phase 3 — Planned 📋
[ ] Deep learning model (PyTorch / ESM-2)
[ ] Protein structure impact (AlphaFold)
[ ] Single-cell RNA-seq support
[ ] Multi-omics integration
[ ] Clinical-grade compliance (HIPAA)
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
📄 License
This project is licensed under the MIT License — see the LICENSE file for details.
🙏 Acknowledgments
FastAPI — for the incredible Python web framework
React — for the frontend library
Tailwind CSS — for the utility-first CSS framework
scikit-learn — for the machine learning toolkit
ACMG Guidelines — for the clinical classification standards
<div align="center">
Built with ❤️ by Avinash Kumar
Bioinformatics | Data Science | AI/ML
🔗 Portfolio  |  💼 LinkedIn  |  🐦 Twitter
</div>