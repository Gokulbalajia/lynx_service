import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from app.main import app
    print("SUCCESS: FastAPI app imported successfully.")
except Exception as e:
    print(f"FAILURE: Failed to import app. Error: {e}")
    import traceback
    traceback.print_exc()
