# 🧬 SeqLens

AI-Powered Genomic Variant Annotation Platform

---

## 🚀 Overview

SeqLens is a full-stack genomic variant annotation platform that enables researchers, clinicians and bioinformatics professionals to upload VCF files and obtain instant pathogenicity predictions.

### Features

- VCF Upload Support
- AI-powered Predictions
- ACMG Classification
- Interactive Dashboard
- Clinical PDF Reports
- Real-time Statistics
- Responsive UI

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React |
| Backend | FastAPI |
| ML | Scikit-learn |
| Parsing | BioPython |
| Reports | ReportLab |
| Styling | Tailwind CSS |

---

## 📸 Screenshots
### Landing Page

![Landing Page](screenshots/landing_page.png)

### Results Dashboard

![Dashboard](screenshots/results_dashboard.png)

### Variant Table

![Variant Table](screenshots/variant_table.png)

### PDF Report

![PDF Report](screenshots/pdf_report.png)



---

## Architecture

```text
React Frontend
      │
      ▼
FastAPI Backend
      │
      ▼
Machine Learning
(Random Forest + GB)
      │
      ▼
ACMG Classification
      │
      ▼
PDF Report Generation
```

---

## Installation

```bash
git clone https://github.com/kavibioinfo/seqlens.git

cd seqlens

pip install -r requirements.txt

cd frontend

npm install

npm run dev
```

---

## Project Structure

```text
SeqLens
│
├── backend
├── frontend
├── screenshots
├── notebooks
├── requirements.txt
├── main.py
└── README.md
```

---

## Future Improvements

- Docker Deployment
- Authentication
- Cloud Storage
- API Documentation
- Model Monitoring

---

## Author

Avinash Kumar

Bioinformatics • AI/ML • Data Science

GitHub: https://github.com/kavibioinfo

