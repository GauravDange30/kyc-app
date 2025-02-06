from pymongo import MongoClient
from src.utils.logger.jsonlogger import logger
from datetime import datetime

# Connection string for MongoDB running locally
MONGO_URI = "mongodb://host.docker.internal:27017/"


try:
    # Establish MongoDB connection
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # Timeout after 5s
    db = client["KYC"]
    users_collection = db["Users"]
    kyc_collection = db["kyc_records"]

    # Test the connection by pinging the server
    client.admin.command('ping')

    # Insert a test record into kyc_records
    result = kyc_collection.insert_one({
        "kyc_type": "test",
        "status": "test",
        "timestamp": datetime.now()
    })

    # Log the inserted record ID
    logger.debug(f"Record inserted with ID: {result.inserted_id}")
    logger.debug("✅ MongoDB connected successfully!")
except Exception as e:
    logger.debug(f"❌ MongoDB connection error: {e}")
