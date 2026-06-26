"""
Helper utility functions.
"""

import uuid


def generate_job_id() -> str:
    """Generate a short unique job ID."""
    return str(uuid.uuid4())[:8]