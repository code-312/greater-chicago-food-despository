from dotenv import load_dotenv
import os

load_dotenv()

CENSUS_KEY = os.getenv("CENSUS_KEY")
FIREBASE_SERVICE_KEY = os.getenv("FIREBASE_SERVICE_KEY")
# This variable gets set to True by memory profiling scripts.
USE_MEMORY_PROFILING = bool(os.getenv("USE_MEMORY_PROFILING", False))
