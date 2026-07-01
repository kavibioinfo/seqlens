"""
Launcher script for Render deployment.
Imports the FastAPI app from backend.app package.
"""

import sys
from pathlib import Path

# Add backend to Python path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

# Import and expose the FastAPI app
from backend.app.main import app