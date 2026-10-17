import sys
import os

# Tambahkan direktori backend ke path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app import app

# Vercel WSGI entry point
# Flask app instance
app = app
