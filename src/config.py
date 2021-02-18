from dotenv import load_dotenv
import os

load_dotenv()

CENSUS_KEY = os.getenv("CENSUS_KEY")
FIREBASE_SERVICE_KEY = os.getenv("FIREBASE_SERVICE_KEY")
