# backend/conftest.py
import sys
from pathlib import Path

# Add project root to Python path so tests can import app.*
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)