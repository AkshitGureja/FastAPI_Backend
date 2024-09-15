from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# MONGO_URL = config("MONGO_URL", default="mongodb://localhost:27017")
MONGO_URL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
db = client.job_database
job_collection = db.get_collection("job_postings")
user_collection = db.get_collection("users")
