import os
from dotenv import load_dotenv

load_dotenv()

PAN_VERIFY_URL = os.getenv("PAN_VERIFY_URL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOGGER_MAX_LENGTH = int(os.getenv("LOGGER_MAX_LENGTH", 15000))
BANK_VERIFY_MOCK_URL = os.getenv('BANK_VERIFY_MOCK_URL')
BANK_VERIFY_URL = os.getenv('BANK_VERIFY_URL')
CLIENTSECRET_API_KEY = os.getenv('CLIENTSECRET_API_KEY')
