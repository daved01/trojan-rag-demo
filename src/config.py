import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "chroma_db"
LOGS_DIR = BASE_DIR / "logs"
PLOTS_DIR = LOGS_DIR / "plots"
QUERIES_FILE = BASE_DIR / "queries.json"

LOGS_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

LLM_MODEL_NAME = "gpt-4.1-mini"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY not found in environment variables. Attack step will fail.")

# Database Settings 
COLLECTION_NAME = "internal_docs"
TOP_K_RETRIEVAL = 10 
TOP_K_CONTEXT = 3

# Silence tokenizer warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"
