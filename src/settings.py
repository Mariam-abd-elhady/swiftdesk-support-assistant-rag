import os
from dotenv import load_dotenv

load_dotenv()

MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "support_tickets"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MODEL_NAME = "gemini-3.6-flash"