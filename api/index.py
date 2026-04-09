import os
import sys

# Add the project root to the python path so 'backend' can be imported correctly
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if path not in sys.path:
    sys.path.insert(0, path)

try:
    from backend.main import app
except ImportError as e:
    print(f"Import Error in api/index.py: {e}")
    # Fallback for different directory structures in serverless environments
    try:
        from main import app
    except ImportError:
        raise e
