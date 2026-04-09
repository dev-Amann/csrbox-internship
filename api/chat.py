import os
import sys

# Add the project root to the python path so 'backend' can be imported correctly
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if path not in sys.path:
    sys.path.insert(0, path)

from backend.main import app
