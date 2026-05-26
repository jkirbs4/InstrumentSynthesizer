import sys
from pathlib import Path

"""
Pytest loads this file before collecting tests.
It adds the project root to Python's import path
so tests in tst can import modules from src.
"""

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
	 sys.path.insert(0, str(PROJECT_ROOT))

